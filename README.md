<p align="center">
  <picture>
    <img src="imagens/difase-branco-trim.png" alt="DIFASE — Diffusion Interface for Analysis, Synthesis & Exploration" width="440">
  </picture>
</p>

<p align="center">
  An interactive scientific showcase for probabilistic modeling of neural signals.
</p>

---

## About DIFASE

**DIFASE** is an interactive platform developed as part of an **ongoing master's research project in Electrical Engineering** by **Ana Luiza S. Tavares**.

The research investigates how **diffusion-based probabilistic models** can characterize changes in electroencephalographic (EEG) activity preceding epileptic seizures. The platform serves as a digital showcase for the project's scientific questions, methodological foundations, research data and findings as they become available.

Rather than acting as a clinical application or a portal for running a trained diffusion network, DIFASE emphasizes **accessible, interactive explanations of the research process**, from exploring electrophysiological recordings to understanding generative diffusion models and their architecture.

> **Research in progress.** The platform presents implemented educational demonstrations and data-exploration features alongside methods being investigated. It does not claim completed experiments, validated seizure predictions or clinical diagnostic capability.

## Research focus

EEG recordings are commonly discussed in terms of interictal, pre-ictal and ictal states. This project investigates a more continuous description: whether the statistical distribution of EEG signals changes in a structured, reproducible way as seizure onset approaches.

A central modeling objective is the family of conditional distributions

$$
p_{\theta}(x\mid\tau),
$$

where $x$ is a multichannel EEG segment, $\tau$ is the time remaining until seizure onset, and $p_{\theta}$ denotes the distribution approximated by a generative diffusion model.

The research explores whether this framework can help characterize pre-ictal dynamics, compare real and generated signal properties, and investigate time-conditioned generative decoding. These are **research objectives**, not claims that a trained or clinically validated model is already available on this website.

The methodological starting point is the work of **Vetter, Macke and Gao (2024)** on denoising diffusion probabilistic models for neurophysiological time series.

## Explore the platform

DIFASE currently includes **three interactive modules**:

| Module | What you can explore |
| --- | --- |
| **EEG Data Explorer** | Navigate a continuous EEG recording, inspect seizure annotations, select channels and frequency bands, examine power spectral density (PSD), and explore a frequency-specific scalp map. |
| **Diffusion Playground** | Interactively examine the forward diffusion process, control diffusion timesteps and noise settings, and animate the progressive corruption of a signal. |
| **Architecture Explorer** | Follow an interactive DDPM architecture diagram, zoom into individual stages, take a guided tour, and understand which modeling choices distinguish the approach described by Vetter et al. from a conventional DDPM. |

The website is deliberately a **scientific communication and visualization platform**, not an inference service. The diffusion animations illustrate model principles; the Architecture Explorer is an educational interpretation of the published methodology, not a computational graph exported from a trained project model.

Additional research-oriented modules will be introduced as the project develops and experimental evidence becomes available.

## EEG reference recording

The EEG Data Explorer currently uses a single preprocessed recording derived from the **Temple University Hospital (TUH) EEG Epilepsy Corpus, version 3.0.0**.

The reference recording contains:

- **19 EEG channels**, sampled at **256 Hz**;
- approximately **10 minutes and 21 seconds** of continuous data;
- an annotated seizure beginning at approximately **05:00**;
- preprocessing that includes filtering, channel screening and per-channel normalization.

The viewer supports full-recording navigation, with visual emphasis on the annotated seizure and an exploratory period preceding its onset. This pre-onset highlight is an **interface convention**, not an independently supplied clinical annotation. Display amplitudes are normalized; the scalp map visualizes sensor-level spectral measures and **does not perform cortical source localization**.

**Data provenance:** [TUH EEG Corpus](https://isip.piconepress.com/projects/tuh_eeg/).

## Scientific foundation

The following publication is the principal architectural reference for the diffusion-model explanation:

> Vetter, J., Macke, J. H., & Gao, R. (2024). *Generating realistic neurophysiological time series with denoising diffusion probabilistic models.* **Patterns, 5**, 101047. https://doi.org/10.1016/j.patter.2024.101047

- **Paper:** [Patterns — Vetter et al. (2024)](https://doi.org/10.1016/j.patter.2024.101047)
- **Original implementation:** [mackelab/neural_timeseries_diffusion](https://github.com/mackelab/neural_timeseries_diffusion)

DIFASE highlights the distinctions between standard DDPM components and methodological choices discussed by Vetter et al., including correlated noise based on an Ornstein–Uhlenbeck process, structured long-range convolutions, and channel-mixing strategies. **The model in the reference paper should not be confused with a trained, seizure-conditioned model from the ongoing thesis.**

## Research directions

The ongoing study is organized around connected methodological questions:

1. **Characterizing pre-ictal EEG:** investigate temporal, spectral and multichannel features as seizure onset approaches.
2. **Probabilistic generative modeling:** study diffusion-based representations of EEG distributions conditioned on time to seizure.
3. **Model evaluation and interpretation:** compare real and synthetic data, assess time-related structure, and examine controlled surrogate-data analyses.
4. **Scientific communication:** publish reproducible visualizations and research findings through DIFASE as they are established.

The scope, implementation and reported evidence will evolve as the master's research progresses.

## Technology

The current website is a static frontend developed with **HTML, CSS and JavaScript**, with interactive visualizations, scroll-based motion and responsive layouts. It does not require a deployed Python backend, a GPU or trained model weights for its existing modules.

### Run locally

Clone the repository and serve the directory containing `index.html`:

```bash
git clone https://github.com/YOUR-USERNAME/difase.git
cd difase
python -m http.server 8000
```

Then open **http://localhost:8000**.

Replace `YOUR-USERNAME` with your GitHub username. The website can also be deployed through **GitHub Pages** using the repository's root directory as the publication source. Confirm all data are eligible for public distribution **before** enabling a public deployment.

The Codec Pro and Helveticish font families are used when available, with system-font fallbacks. No proprietary font files are included.

## Author & scientific coordination

**Author**  
**[Ana Luiza S. Tavares](https://scholar.google.com/citations?user=ErRINMEAAAAJ&hl=pt-BR)**  
*M.Sc. student in Electrical Engineering | B.Sc. in Biotechnology*


**Scientific coordination**

- **[Professor Bruno Duarte Gomes, PhD](https://www.researchgate.net/profile/Bruno-Gomes-30)**
- **[Professor Eduardo Coelho Cerqueira, PhD](https://scholar.google.com/citations?user=6Oexn7IAAAAJ&hl=pt-BR&oi=ao)**

## Institutional context

<p align="center">
  <img src="/imagens/logos-institucionais.png" alt="Institutional logos associated with the DIFASE research project" width="880">
</p>

---

<p align="center"><sub>DIFASE · Ongoing scientific research · 2026</sub></p>
