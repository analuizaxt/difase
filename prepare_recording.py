#!/usr/bin/env python3
"""Package ONE continuous TUH EEG recording for the static DIFASE showcase.

Prefer the already processed *_full.npz + *_meta.json described by the research README.
An EDF input is supported for inspection but is NOT represented as preprocessed.
Never uploads data; generates a float32 binary and public-safe metadata locally.
"""
import argparse, json, math, re
from pathlib import Path
import numpy as np
from scipy.signal import welch

BANDS = {'delta': (0.5, 4), 'theta': (4, 8), 'alpha': (8, 13), 'beta': (13, 30), 'low_gamma': (30, 45)}


def get_annotations(meta):
    out = []
    for a in meta.get('annotations', []):
        label = str(a.get('description', a.get('label', ''))).lower().strip()
        if label not in ('seiz', 'seizure', 'sz', 'ictal'):
            continue
        start = float(a.get('onset_s', a.get('onset', 0)))
        if 'duration_s' in a: end = start + float(a['duration_s'])
        elif 'duration' in a: end = start + float(a['duration'])
        elif 'offset_s' in a: end = float(a['offset_s'])
        else: continue
        if math.isfinite(start) and math.isfinite(end) and end > start:
            out.append({'type':'ictal','start_s':start,'end_s':end,'source':'TUH annotation'})
    return sorted(out,key=lambda x:x['start_s'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    source=p.add_mutually_exclusive_group(required=True)
    source.add_argument('--npz',type=Path,help='Processed *_full.npz (recommended)')
    source.add_argument('--edf',type=Path,help='Original EDF (raw; no preprocessing implied)')
    p.add_argument('--meta',type=Path,help='Corresponding TUH *_meta.json with annotations')
    p.add_argument('--out',type=Path,default=Path('data'))
    p.add_argument('--preictal-minutes',type=float,default=30,help='Operational display interval, NOT a source annotation')
    args=p.parse_args()
    meta = json.loads(args.meta.read_text(encoding='utf-8')) if args.meta else {}
    if args.npz:
        with np.load(args.npz, allow_pickle=False) as b:
            data = np.asarray(b['data'],dtype=np.float32)
            channels = [str(ch) for ch in b['channels'].tolist()]
            fs = float(b['sfreq_hz'])
            bad = [str(ch) for ch in b['bad_channels'].tolist()] if 'bad_channels' in b else []
        origin='tuh_processed_npz'
        unit='z-score'
        preprocess=['Original TUH AR/REF reference preserved','Resampled to 256 Hz','60 Hz notch','0.5–45 Hz FIR band-pass','Screened: bad channels excluded','Global channel-wise z-score','Full continuous recording; no epoching']
        processed=True
    else:
        import mne
        raw=mne.io.read_raw_edf(args.edf,preload=True,verbose='ERROR')
        raw.pick_types(eeg=True)
        fs=float(raw.info['sfreq'])
        channels=list(raw.ch_names)
        data=np.ascontiguousarray(raw.get_data().T*1e6,dtype=np.float32) # EDF via MNE is volts
        bad=[]
        if not meta.get('annotations') and raw.annotations:
            meta['annotations']=[{'onset_s':float(on), 'duration_s':float(dur),'description':str(label)} for on,dur,label in zip(raw.annotations.onset,raw.annotations.duration,raw.annotations.description)]
        origin='edf_original'
        unit='µV'
        preprocess=['Original EDF loaded without DIFASE preprocessing','Signal is not equivalent to the TUH processed NPZ']
        processed=False
    if data.ndim!=2 or not len(channels) or data.shape[1]!=len(channels) or fs<=0:
        raise ValueError('Expected nonempty (n_samples, n_channels) array, matching channels and valid sfreq')
    data=np.nan_to_num(data,nan=0,posinf=0,neginf=0).astype('<f4',copy=False)
    n,c=data.shape
    duration=n/fs
    events=[e for e in get_annotations(meta) if e['start_s'] < duration and e['end_s']>0]
    for e in events:
        e['start_s']=max(0,e['start_s']);e['end_s']=min(duration,e['end_s'])
    pre=[]
    prev_end=0.
    for e in events:
        if args.preictal_minutes>0:
            a=max(prev_end,e['start_s']-60*args.preictal_minutes)
            if e['start_s']>a:pre.append({'type':'preictal','start_s':a,'end_s':e['start_s'],'source':f'Operational {args.preictal_minutes:g}-minute interval; not a TUH annotation'})
        prev_end=max(prev_end,e['end_s'])
    target=args.out;target.mkdir(parents=True,exist_ok=True)
    data.tofile(target/'recording.f32')
    spectra={};stats={}
    nper=min(n,4096)
    for j,ch in enumerate(channels):
        sig=np.asarray(data[:,j],dtype=np.float64)
        f,pxx=welch(sig,fs=fs,nperseg=nper,noverlap=nper//2,scaling='density')
        keep=f<=min(60.,fs/2.)
        freqs=f[keep];powers=pxx[keep]
        bands={}
        for band,(lo,hi) in BANDS.items():
            mask=(f>=lo)&(f<hi)&(f<=fs/2.)
            bands[band]=round(float(np.trapezoid(pxx[mask],f[mask])) if mask.sum()>1 else 0,8)
        spectra[ch]={'freqs_hz':freqs.round(4).tolist(),'psd':powers.astype('float32').tolist()}
        stats[ch]={'mean':round(float(np.mean(sig)),5),'std':round(float(np.std(sig)),5),'rms':round(float(np.sqrt(np.mean(sig*sig))),5),'bandpowers':bands}
    # No names, ages, source paths, or clinical free-text notes in the public metadata.
    manifest={
        'schema_version':1,'title':'TUH EEG reference recording' if processed else 'EDF reference recording',
        'source_dataset':'TUH EEG Epilepsy Corpus v3.0.0' if processed else 'EDF recording (verify source and license)',
        'origin_format':origin,'processed':processed,'preprocessing':preprocess,
        'sample_rate_hz':fs,'n_samples':n,'n_channels':c,'duration_s':duration,
        'channels':channels,'bad_channels':bad,'unit':unit,
        'data_file':'recording.f32','storage':'float32_le_interleaved_samples_x_channels',
        'events':events,'preictal_regions':pre,'preictal_definition':f'{args.preictal_minutes:g} min before seizure onset; for visualization only; no clinical assertion',
        'statistics':stats,'spectra':spectra,
        'dataset_note':'Preprocessed full-length TUH recording, not split into 30-second epochs.' if processed else 'Original EDF; not the processed TUH signal. No preprocessing claimed.',
    }
    (target/'recording.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(f'Created {target}/recording.f32 ({n} samples × {c} channels, {fs:g} Hz, {duration:g} s)')
    print(f'Created {target}/recording.json ({len(events)} seizure annotations, {len(pre)} operational preictal regions)')
    if not events:print('CAUTION: no seizure annotations found. Add *_meta.json or the correct source annotations.')
    if not processed:print('CAUTION: EDF raw; this has NOT undergone the provided TUH preprocessing protocol.')

if __name__=='__main__': main()
