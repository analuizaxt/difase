# DIFASE · v0.6

**Diffusion Interface for Analysis, Synthesis & Exploration**

A scientific research showcase of neural signals, probabilistic diffusion and the methodology of Vetter, Macke & Gao (2024). Its frontend is in English and does not require model weights, a GPU or an application server.

## Run locally

1. Extract `DIFASE-frontend-v0.6.zip`.
2. Open a terminal inside `DIFASE-v0.7/`.
3. Start a local HTTP server:

   ```bash
   python -m http.server 8000
   ```

4. Open **http://localhost:8000** in a browser. The home page, three interactive modules, diagrams, institutional logos, author credits, and reference EEG will be accessible. You may also double-click `index.html` and open it directly as a local file. For that case, the EEG Explorer uses the bundled `data/recording-inline.js` fallback because browsers normally prevent direct `fetch()` access to local binary files. The fallback is an identical copy of the signal, not a synthetic alternative.

There are **no npm dependencies**. Fonts used by the original branding — Codec Pro and Helveticish — are referenced as locally installed fonts; system fallbacks are used if they are not installed. No font files are redistributed.

## Included EEG specimen

The selected exemplar was supplied by the researcher and derived from the **Temple University Hospital EEG Epilepsy Corpus v3.0.0**. Data in the public-facing app are derived from the supplied `aaaaajqo_s011_t000_full.npz` and `aaaaajqo_s011_t000_meta.json`. The original NPZ/JSON are not required to run the delivered site because the complete waveform was exported to a directly readable format.

| Attribute | Value |
|---|---|
| Channels | 19 |
| Sampling frequency | 256 Hz |
| Complete recording | 158,976 time samples, 620.996 s (~10m21s) |
| Original processing | 60 Hz notch, FIR 0.5–45 Hz bandpass, global channel-wise z-score, AR/REF reference preserved, screened channels |
| Amplitude units | z-score, **not µV** |
| Dataset seizure annotation | 300.0469–370.8438 seconds (05:00–06:11 approx.) |
| Pre-onset highlight | 2 minutes preceding annotated seizure onset, **an exploratory visualization convention; not a separate clinical label** |

The delivered `data/recording.f32` stores **all 158,976 × 19 values** in little-endian, sample-major float32 format. `data/recording.json` contains anonymized display metadata, verified channel labels, event timing and per-channel real Welch PSD, mean, standard deviation, RMS and bandpower. The browser loads these files automatically, without an upload interface. The full waveform is kept, while zoom and timeline selection modify only the portion currently drawn to screen. To see all of it at once, select **Full** or inspect the recording overview bar.

The frequency-band waveforms are exploratory display filters performed in the browser; Welch PSD and bandpower are computed offline from the whole recording. Numerical results should always be cited with their actual preprocessing and statistical definitions.

## Architecture Explorer

Open **Architecture Explorer** from the module index. The unified model diagram is based on the published approach:

- Vetter, J., Macke, J. H. & Gao, R. (2024). *Generating realistic neurophysiological time series with denoising diffusion probabilistic models*. *Patterns* 5, 101047. [DOI](https://doi.org/10.1016/j.patter.2024.101047)
- Original [mackelab/neural_timeseries_diffusion](https://github.com/mackelab/neural_timeseries_diffusion) repository.

Each of its 15 selectable stops zooms to the relevant component and opens a teaching panel with: explanation, why it matters, and a concept illustration. The Vetter-specific adaptation panel is shown **only** on the highlighted methodological adaptations, rather than on every standard DDPM step. Use **Next / Previous**, arrow keys, **Fit**, or **Start guided exploration** to move through the diagram. Mouse-wheel zoom has been removed: the map stays fitted until a step is selected; zoom occurs only when focusing a step. The mouse wheel scrolls the page normally. Blue highlights indicate methodological adaptations/choices (such as OU-correlated noise, efficient long convolutions, sparse channel mixing, covariance-weighted loss). The basic DDPM Markov chain and the paper's custom denoiser are distinguished. Diffusion index **t** and the research variable **τ** (time to seizure) are different; the paper is **not** claimed to have trained on τ.

This diagram is an **educational interpretation** of the published architecture, not a layer-by-layer computational graph exported from trained weights. DIFASE does not run a trained model. The home page advertises **only the three functioning interactive modules**. A discreet expandable “More modules in development” note acknowledges ongoing work without listing placeholder modules or invented results.

## Institutional credits

The institution logos appear as a small centered sign-off without an extra partners heading. A subtle footer button, **Author & scientific coordination**, opens a collapsible panel showing Ana Luiza S. Tavares as the author and M.Sc. student leading this ongoing thesis project, under scientific coordination by Professor Bruno Duarte Gomes, PhD and Professor Eduardo Coelho Cerqueira, PhD.

## Structure

```text
DIFASE-v0.7/
├── index.html              # home and three active module routes
├── app.js                  # navigation, EEG visualization, diagram interactions
├── styles.css              # dark responsive design, transitions, animation
├── architecture-diagram.svg # standalone v0.3 explanatory vector diagram (reference)
├── data/
│   ├── recording.json      # event metadata, spectral estimates, channel statistics
│   ├── recording.f32       # full real EEG, float32 interleaved (12 MB)
│   └── recording-inline.js # same EEG as base64, for file:// offline use
├── imagens/
│   ├── logos-institucionais.png
│   ├── difase-branco*.png, difase-preto*.png
│   └── Elemento.png
├── prepare_recording.py    # optional local exporter for future specimen replacements
└── README.md
```

## Responsible sharing of clinical signals

**Before publishing this website on a public server, or committing the ZIP or data files to a public repository, verify the TUH corpus data use agreement, redistribution rights and any applicable institutional ethics rules.** Note that `recording-inline.js` contains the *same entire human EEG recording* as `recording.f32` and must be subject to the same restrictions. Removing patient identifiers from the metadata does **not** guarantee that exporting a complete human EEG record is allowed. For public deployment, use a permitted recording, an authorized restricted-access deployment, or a legally approved synthetic demonstrator. The included waveform is delivered as requested for local project development and review; its inclusion in this ZIP does not assert public redistribution permission.

To deploy the website without the patient waveform, omit `data/recording.f32` and `data/recording.json` **and replace the public viewer with an approved example** (otherwise it will display an unavailable state).

## v0.6 revisions

- Replaced text-only DIFASE logos in the header and footer with the supplied white logo, precisely cropped to visible content. The full hero logo with subtitle is unchanged.
- Simplified desktop and mobile navigation to About and Modules only.
- Author description updated exactly as supplied.
- Removed the architecture mouse-wheel zoom and manual +/- zoom controls; clicking steps and guided exploration remain the only ways to zoom.
- Removed the internal-sounding architecture callout.
- Corrected the EEG Explorer when opened directly with a browser from an extracted ZIP by adding an offline-script fallback with the complete, unchanged reference recording.

## v0.7 — Hero waveform interaction

The home hero waveform reacts to mouse/stylus position by smoothly increasing the local signal amplitude around the pointer (Gaussian spatial envelope). Baselines remain fixed; no vertical or horizontal translation is applied. The effect fades when the pointer leaves and respects reduced-motion accessibility settings.


## DIFASE v0.9 · interaction changes

- EEG Explorer: continuous TUH EEG retained; scalp spectral topography replaces whole-recording mean/SD/RMS statistics (these are constrained by per-channel z-score normalization). The map is computed client-side from each channel's recorded Welch power spectrum. Selecting a frequency band updates the map to **relative band power (%)**; broadband displays **mean spectral frequency (Hz)**. Click an electrode to select the channel displayed in the PSD. This interpolated *sensor-space* visualization is not source localization.
- Diffusion Playground: the Play button animates forward diffusion from the current diffusion step through step 1000, then loops until paused. The slider remains manually adjustable.
- Architecture: links to the other interactive modules.
- Home: a more restrained pointer-amplitude response and a circular animated scroll-arrow; the hero CTA was removed.

The example EEG and precomputed spectra are carried over from v0.7 without changes.


### Visual updates in v0.9

- The Diffusion Playground plays from the currently selected timestep on the first pass, then replays from `t = 0` for subsequent loops. The Play/Pause control still stops the animation.
- The top-left identity uses the blue particle icon on the home hero, switching to the DIFASE wordmark when the page is scrolled or a module is open.
- The “Explore what comes next” label has been removed from the development accordion.
- Author and scientific coordination names link to the corresponding Scholar/ResearchGate profiles and highlight blue on hover/focus.
