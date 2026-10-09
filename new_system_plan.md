# Voice Shield AI: Complete Project Brief & PPT Presentation Guide

> **Official Project Repository**: [https://github.com/aayash317-svg/Ai_voice-_cloning](https://github.com/aayash317-svg/Ai_voice-_cloning)  
> **Project Title**: Voice Shield AI — Real-Time Conversational AI Voice Cloning Detection & Call Defense Engine  
> **Core Mission**: Helping protect financial transactions and phone communications against generative AI voice clones (e.g., ElevenLabs, ChatterboxTTS, HiFi-GAN-based vocoders) using real-time conversational diarization, raw-waveform neural filtering, and zero-retention privacy.

---

## Part 1: Visual Working Architecture Diagram

Below is the complete end-to-end working flow of the system (6 processing layers). This diagram can be directly translated into presentation shapes, slides, or graphics:

```
===================================================================================================================
                                       VOICE SHIELD AI: WORKING ARCHITECTURE
===================================================================================================================

  [ USER / LOCAL CALLER ]                                                   [ REMOTE CALLER / FRAUDSTER ]
  (Speaking into Smartphone)                                                (Using Cloned Neural Voice)
             │                                                                           │
             └────────────────────────────────────┬──────────────────────────────────────┘
                                                  ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
  │ 1. REAL-TIME AUDIO INGESTION (CLIENT LAYER)                                                 │
  │ • Browser Web Audio API captures speakerphone microphone or VoIP call tab                   │
  │ • Resampled to standardized 16,000 Hz, 16-bit Mono PCM                                      │
  │ • Inaudible Keep-Alive Loop (gain = 0.00001) helps prevent mobile OS audio suspension       │
  └─────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │ Binary WebSocket Stream (250ms chunks)
                                                 ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
  │ 2. INGESTION & ZERO-RETENTION PRIVACY BUFFER                                                │
  │ • FastAPI High-Performance WebSocket Server (/stream/call)                                  │
  │ • AudioPrivacyBuffer: 3.0-second Ephemeral Circular RAM Ring (48,000 float32 samples)       │
  │ • NO AUDIO WRITTEN TO DISK: audio is processed in RAM only                                  │
  └─────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
  │ 3. REAL-TIME CONVERSATIONAL DIARIZATION ENGINE                                              │
  │ • Voice Activity Detection (VAD): Distinguishes speech from ambient room noise              │
  │ • 40-Dimensional Timbre Embedding: 19 MFCC mean + 19 MFCC std + Spectral Centroid/Rolloff   │
  │ • Adaptive Centroid Clustering: Separates voices using Cosine Distance                      │
  │                                                                                             │
  │   ├─► SPEAKER A : Local Caller (User)       ──► Local reference (first speaker)             │
  │   ├─► SPEAKER B : Remote Claimed Contact    ──► Isolated & Streamed to Forensic ML Engine   │
  │   └─► OVERLAP   : Simultaneous Cross-Talk   ──► Quarantined to prevent false contamination  │
  └─────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │ Clean Isolated Remote Voice Frames
                                                 ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
  │ 4. DUAL-MODEL AI DETECTION ENSEMBLE                                                         │
  │                                                                                             │
  │   [ MODEL 1: SincNet Neural Waveform ]        [ MODEL 2: Calibrated Random Forest ]         │
  │   • 1D Time-Domain Convolutions               • 63 Physics-Informed Acoustic Dimensions     │
  │   • Learnable bandpass sinc filters           • Phase derivative variance (Hilbert trans)   │
  │   • No spectrogram front-end                  • High-frequency cutoff ratio (> 4 kHz)       │
  │   • Captures fine vocoder artifacts           • Glottal pitch micro-jitter & shimmer        │
  │   • Output: P_Neural                          • Output: P_RF (Calibrated, tau* = 0.3985)    │
  │                           \                           /                                     │
  │                            ▼                         ▼                                      │
  │                       [ CONSENSUS LATE FUSION ]                                             │
  │                       P_ensemble = 0.50 * P_RF + 0.50 * P_Neural                            │
  └─────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
  │ 5. DYNAMIC THREAT ENGINE & 3-STAGE PROGRESSIVE EVALUATION                                   │
  │ • Multi-Signal Formula: 50% ML + 20% HF Ratio + 15% Phase Var + 10% Jitter + 5% Consistency │
  │ • Context Sensitivity: +12% for High-Value Wire/Bank Transfer Flags (capped at 100%)        │
  │                                                                                             │
  │ [ PROGRESSIVE TIMELINE CONTROLLER ]                                                         │
  │   ├─► 0.0s – 5.0s  : STAGE 0 (CALIBRATING BASELINE)──► UI Countdown: (Xs / 10s)             │
  │   ├─► 5.0s – 10.0s : STAGE 1 (PRELIM. ROLLING AVG)  ──► Live score (shown from 5s)          │
  │   └─► 10.0s– 12.0s : STAGE 2 (CONSOLIDATED FINAL)   ──► FINAL VERDICT (by 12s)              │
  └─────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
  │ 6. REAL-TIME UI TELEMETRY & CRYPTOGRAPHIC AUDIT                                             │
  │ • SHA-256 AuditChain: Seals final call verdict into a tamper-evident hash-chained block     │
  │ • High-Speed JSON Telemetry to Browser:                                                     │
  │   ├─► Live Threat Gauge: "Final Threat: 5.0% (AUTHENTIC)" vs "CRITICAL CLONE DETECTED"      │
  │   ├─► Dynamic Banner: Color-coded guidance (Green = Safe, Red = Freeze Payments)            │
  │   ├─► Dual Speaker Cards: Turn counts, speech duration, and isolated risk scores            │
  │   └─► 60 FPS Oscilloscope: Real-time waveform canvas showing vocal energy dynamics          │
  └─────────────────────────────────────────────────────────────────────────────────────────────┘
===================================================================================================================
```

---

## Part 2: Machine Learning Concepts & Paradigms Used

Use this section to explain the machine learning innovations clearly in your presentation slides:

| # | ML Concept / Paradigm | How It Works in Voice Shield AI | Why It Was Chosen / Real-World Value |
| :-: | :--- | :--- | :--- |
| **1** | **Raw-Waveform 1D Convolutions (SincNet)** | Convolves raw pressure waves with parameterizable sinc bandpass filters: $g[t, f_1, f_2] = 2f_2 \operatorname{sinc}(2\pi f_2 t) - 2f_1 \operatorname{sinc}(2\pi f_1 t)$. Learns only the filter cutoffs $f_1$ and $f_2$ via backpropagation. | Magnitude/Mel spectrograms discard phase and blur fine time structure. SincNet works directly on the raw time-domain signal, so it can pick up vocoder artifacts that spectrogram front-ends may smooth away. |
| **2** | **Supervised Ensemble Learning (Random Forest)** | 100 decision trees (`max_depth=16`, `class_weight="balanced"`) trained on 63 physical acoustic features. | Reduces the variance of a single decision tree and handles non-linear feature interactions. Speaker-disjoint data splits (see Slide 10) are what guard against memorizing individual speakers. |
| **3** | **Late Consensus Fusion** | Blends neural and tree probabilities: $P_{\text{ensemble}} = 0.50 \cdot P_{\text{RF}} + 0.50 \cdot P_{\text{Neural}}$. | Defense-in-depth: if a cloned voice evades the spectral features, the raw-waveform network may still catch it, and vice versa. This improves robustness but does not make the system immune to adversarial attacks. |
| **4** | **Unsupervised Online Clustering (Diarization)** | Maps speech chunks into a 40-D timbre embedding space (MFCCs, spectral centroid, rolloff). Clusters speakers via Cosine Distance $d(u,v) = 1.0 - \frac{u \cdot v}{\lVert u \rVert \lVert v \rVert}$ with EMA centroid tracking ($\alpha = 0.02$). | Separates the local user's voice from the remote caller in real time without requiring pre-recorded voice enrollment. |
| **5** | **Physics-Informed Feature Engineering** | Computes instantaneous phase derivative variance $\operatorname{Var}(\Delta\phi/\Delta t)$ via Hilbert transform, high-frequency cutoff ratio ($>4$ kHz), and parabolic pitch interpolation ($F_0$). | Generates explainable physical reasons for alerts rather than acting as a pure black box. |
| **6** | **Class Imbalance Mitigation** | Enforces a strict 1:1 balanced working set (3,710 genuine human vs 3,710 synthetic clips) drawn from the 38,239-clip corpus. | Public datasets can be heavily skewed toward fake audio (up to ~85%), which caused unbalanced baselines to flag real human voices far too often. Balancing removes that majority-spoof bias. |
| **7** | **EER Threshold Selection & Probability Calibration** | The Random Forest probabilities are calibrated (Platt scaling), and the decision boundary $\tau^* = 0.3985$ is chosen at the Equal Error Rate (EER) point on the held-out Development set. | Balances false alarms against missed clones, so natural human voices typically fall in the LOW risk zone (e.g., ≈5% threat score). |
| **8** | **Multi-Criteria Threat Fusion** | Fuses model probabilities with physical sub-band anomaly scores and a context multiplier (+12% for flagged financial transfers, capped at 100%). | Prevents single-feature errors and provides context-aware defense for banking and emergency calls. |

---

## Part 3: Ready-to-Use Slide-by-Slide PPT Content

Copy and paste these slide outlines directly into your PowerPoint / Canva presentation deck:

---

### Slide 1: Title Slide
- **Slide Title**: Voice Shield AI
- **Subtitle**: Real-Time AI Voice Cloning Detection & Live Call Protection Engine
- **Bullet Points**:
  - Defending voice communications against generative deepfakes and AI voice clones
  - Powered by SincNet raw-waveform neural filtering and 63-D acoustic physics
  - Real-time conversational diarization with zero-retention privacy
- **Footer**: GitHub Repository: `https://github.com/aayash317-svg/Ai_voice-_cloning`

---

### Slide 2: The Problem — The Weaponization of Generative Voice
- **Slide Title**: The Threat: Generative AI Voice Cloning
- **Bullet Points**:
  - **Seconds to Clone**: Modern neural TTS engines (e.g., ElevenLabs, ChatterboxTTS, VITS) can produce a convincing clone from only a few seconds of reference audio.
  - **Financial Scams & CEO Fraud**: Industry and regulator reports attribute large and growing losses to grandparent emergency scams, authorized push-payment fraud, and fake executive wire instructions. *(Add a cited figure, e.g., from the FTC or FBI IC3, before presenting.)*
  - **The Perceptual Flaw**: Human ears struggle to distinguish neural vocoder speech over compressed telephone networks (VoLTE / VoIP).
  - **Why Existing Tools Fall Short**: Many tools run only post-call forensic analysis, or work on batches of audio with multi-second delays, often without separating the two speakers on a call.

---

### Slide 3: The Solution — Voice Shield AI
- **Slide Title**: Our Solution: Real-Time Conversational Defense
- **Bullet Points**:
  - **Live Call Protection**: Streams and analyzes conversational phone audio in real time over WebSockets (per-chunk processing round-trip < 90 ms).
  - **Conversational Diarization**: Automatically separates the user's voice from the remote caller to reduce false alarms.
  - **Progressive Threat Timeline**:
    - *0–5s*: Baseline room and microphone calibration
    - *5–10s*: Preliminary rolling risk score (first shown at 5s)
    - *10–12s*: Final verdict (always issued by 12s, even with silent pauses)
  - **Zero-Retention Privacy**: Audio exists only in a 3-second RAM ring buffer — no audio is ever written to disk.

---

### Slide 4: System Architecture & 6-Layer Defense
- **Slide Title**: End-to-End System Architecture
- **Bullet Points**:
  - **Layer 1 (Client Ingestion)**: 16 kHz resampler and inaudible mobile keep-alive loop.
  - **Layer 2 (Privacy Buffer)**: FastAPI WebSocket server with an ephemeral 3-second RAM ring buffer.
  - **Layer 3 (Diarization)**: VAD speech filter + 40-D timbre embeddings with adaptive cosine clustering.
  - **Layer 4 (Dual AI Ensemble)**: PyTorch SincNet 1D raw-waveform model + Calibrated Random Forest.
  - **Layer 5 (Risk Engine)**: Multi-signal threat formula with financial context weighting and progressive timeline.
  - **Layer 6 (Audit & UI)**: SHA-256 tamper-evident hash-chained log + live glassmorphic dashboard.
- *(Insert Architecture Diagram from Part 1 here)*

---

### Slide 5: Acoustic Physics: How the Model Catches Clones
- **Slide Title**: Forensic Acoustic Mechanics: Human Vocal Tract vs AI Vocoders
- **Bullet Points**:
  - **Phase Irregularities (Hilbert Transform)**:
    - *Human*: Aerodynamic vocal fold airflow creates smooth, continuous phase transitions.
    - *AI Clone*: Neural vocoders synthesize phase implicitly, which can produce irregular phase derivative variance ($\operatorname{Var}(\Delta\phi/\Delta t)$).
  - **High-Frequency Spectral Cutoffs** *(interpreted relative to the call's channel bandwidth)*:
    - *Human*: Natural consonants radiate energy smoothly up to the channel limit (8 kHz at 16 kHz sampling).
    - *AI Clone*: Some TTS/vocoder pipelines leave abrupt cutoffs or unnatural high-frequency energy voids.
  - **Glottal Micro-Jitter & Shimmer**:
    - *Human*: Involuntary cycle-to-cycle micro-perturbations in pitch and amplitude.
    - *AI Clone*: Often unnaturally smooth (robotic stability) or erratic across phoneme boundaries.

---

### Slide 6: Machine Learning Architecture & Dual Ensemble
- **Slide Title**: Dual-Model Machine Learning Ensemble
- **Bullet Points**:
  - **Model 1: SincNet 1D Raw-Waveform Filter**:
    - Deep convolutional architecture operating directly on raw time-domain audio samples.
    - Learns bandpass filter cutoff frequencies directly via backpropagation.
    - Can detect fine-grained vocoder artifacts that spectrogram front-ends may smooth away.
  - **Model 2: Calibrated Random Forest**:
    - 100 decision trees evaluated across 63 acoustic, spectral, and prosodic dimensions.
    - Balanced class weights handle class imbalance; speaker-disjoint splits prevent speaker memorization.
  - **Consensus Fusion**:
    - $P_{\text{ensemble}} = 0.50 \cdot P_{\text{RF}} + 0.50 \cdot P_{\text{Neural}}$ improves robustness: an attacker must evade both representations at once.

---

### Slide 7: Real-Time Conversational Diarization
- **Slide Title**: Two-Speaker Live Call Diarization
- **Bullet Points**:
  - **The Two-Way Audio Challenge**: Phone calls contain mixed audio of both participants; analyzing both together creates false alarms.
  - **Online Timbre Space**: 40-dimensional feature vector (19 MFCC mean, 19 MFCC std, centroid, rolloff).
  - **Centroid Clustering**:
    - Initializes Centroid A on the first detected speaker, assumed to be the local caller; identifies Centroid B when cosine distance exceeds $0.025$.
    - Dynamic exponential moving average ($\alpha = 0.02$) tracks natural pitch shifts throughout the call.
  - **Cross-Talk Quarantine**: Overlapping speech segments are identified and excluded from threat scoring.

---

### Slide 8: Progressive Threat Scoring (The 10–12s Rule)
- **Slide Title**: Progressive Evaluation Timeline
- **Bullet Points**:
  - **Stage 0 (0.0s – 5.0s | Calibrating Baseline)**:
    - Normalizes ambient room acoustics, phone mic gain, and network compression.
    - Shows an active countdown ticker: `ANALYZING CALL AUDIO — EVALUATING (Xs / 10s)`.
  - **Stage 1 (5.0s – 10.0s | Preliminary Rolling Average)**:
    - Calculates a rolling preliminary risk score, first shown at 5s, to provide early situational awareness.
  - **Stage 2 (10.0s – 12.0s | Consolidated Final Verdict)**:
    - Renders the final verified score (`CALL AUTHENTIC` or `AI CLONE DETECTED`).
    - Even with quiet mobile microphones or silent pauses, the fallback buffer ensures a final verdict is always issued by 12s.

---

### Slide 9: Privacy-First Design & Cryptographic Audit
- **Slide Title**: Zero-Retention Privacy & Tamper-Evident Ledger
- **Bullet Points**:
  - **Zero-Retention Design**:
    - Audio is buffered strictly in a transient 3.0-second RAM ring array.
    - Never written to hard drives or cloud storage, which is designed to support GDPR, CCPA, and banking privacy requirements. *(Formal compliance still requires a legal review.)*
  - **SHA-256 Hash-Chained Audit Log (`AuditChain`)**:
    - Every completed call inspection appends a block to a local, tamper-evident hash chain.
    - Block includes: Timestamp, Event Type, Non-Biometric Metadata, Payload Hash, and Previous Hash.
    - Built-in `/audit/verify` endpoint verifies chain integrity for compliance disputes.

---

### Slide 10: Training Methodology & Dataset Universe
- **Slide Title**: Dataset Universe & Scientific Anti-Leakage Training
- **Bullet Points**:
  - **38,239 Audio Clips Corpus**:
    - *LibriSpeech (test-clean)*: 2,620 clean human speech samples
    - *ASVspoof 2019 LA (Bonafide)*: 2,680 genuine clean studio-quality recordings (VCTK-based)
    - *ASVspoof 2019 LA (Spoofs A07–A19)*: 15,399 synthetic clips across 13 attack systems (A16 and A19 reuse the algorithms of A04 and A06)
    - *PhonemeDF (ChatterboxTTS)*: 17,540 modern neural TTS synthetic voices
  - **Strict Anti-Leakage Splitting**:
    - 70% Train / 15% Dev / 15% Test with zero speaker overlap between splits.
  - **1:1 Controlled Balancing**:
    - Balanced working set of 3,710 genuine vs 3,710 synthetic clips (7,420 total), removing majority-spoof bias.
  - **Note**: Genuine speech comes from read/studio recordings, not live phone calls; see Known Limitations (Part 5).

---

### Slide 11: Performance Benchmarks & Results
- **Slide Title**: Validated Performance Benchmarks
- **Bullet Points**:
  - **ROC-AUC**: **0.9882** on the held-out multi-generator test set.
  - **Equal Error Rate (EER)**: **6.12%** across diverse acoustic conditions.
  - **Human False Alarm Rate**: **5.53%** (vs. 79–88% for the earlier unbalanced baseline).
  - **Modern Neural TTS Detection**: **300 / 300 (100%)** held-out ChatterboxTTS samples flagged (small sample; 95% confidence lower bound ≈ 98.8%). ElevenLabs validation is planned future work.
  - **Inference Speed**: Feature extraction < 45 ms; WebSocket round-trip < 90 ms per chunk (the final verdict is issued at 10–12s).

---

### Slide 12: Real-World Testing & Cross-Platform UI
- **Slide Title**: User Interface & Mobile Phone Testing
- **Bullet Points**:
  - **Glassmorphic Cyber Dashboard**: Real-time oscilloscope, dynamic speaker ribbons, per-speaker forensic cards, and color-coded alert banners.
  - **Mobile Keep-Alive Architecture**: Inaudible gain feedback loop (`0.00001`) helps prevent Android Chrome and iOS Safari from suspending the audio context.
  - **Live Mobile Testing via Cloudflare Tunnel (demo only)**:
    - Run `cloudflared.exe tunnel --url http://127.0.0.1:8050` to test live phone calls from any smartphone browser. Audio passes through the tunnel but is never stored.
    - Speakerphone tip: put the call on speakerphone so the browser microphone captures both voices. Mobile browsers cannot capture call audio directly.

---

### Slide 13: Competitive Advantage Matrix
- **Slide Title**: Competitive Advantage Matrix
- **Table**:
  | Capability | Traditional Biometrics | Cloud Voice APIs | **Voice Shield AI** |
  | :--- | :--- | :--- | :--- |
  | **Live Call Diarization** | ❌ None | ❌ Mixed audio only | ✅ **Two-Speaker Timbre Clustering** |
  | **Detection Speed** | ❌ Post-call only | ⚠️ Multi-second batch / near-real-time (varies) | ✅ **Progressive: preliminary at 5s, final by 12s** |
  | **Waveform Processing** | ❌ STFT only | ❌ Spectrograms | ✅ **SincNet 1D Raw Waveform Convolutions** |
  | **Audio Privacy** | ⚠️ Saved to cloud | ⚠️ Often retained (varies by vendor) | ✅ **Zero-Retention Ephemeral RAM** |
  | **Acoustic Physics** | ❌ Black-box | ❌ Black-box | ✅ **Phase Derivative, HF Cutoff, Jitter** |
  | **Auditability** | ❌ Plain text logs | ❌ Proprietary DB | ✅ **SHA-256 Hash-Chained Audit Log** |

---

### Slide 14: Conclusion & Future Roadmap
- **Slide Title**: Project Conclusion & Future Roadmap
- **Bullet Points**:
  - **Accomplishments**:
    - Delivered a real-time anti-spoofing defense engine with sub-90 ms per-chunk processing.
    - Reduced false alarms and mobile mic freezing through balanced training data and progressive evaluation.
    - Built from a 38,239-clip corpus (7,420-clip balanced working set), reaching 0.9882 ROC-AUC on the held-out test split.
  - **Future Roadmap**:
    - Native mobile app with on-device inference (Android restricts third-party access to call audio, so this needs speakerphone capture or an OEM/carrier partnership; `CallScreeningService` exposes call metadata only).
    - Hardware-accelerated SIP trunk inspection for corporate banking call centers.
    - Real-time multilingual keyword spotting for fraud phrases ("wire transfer", "OTP").
    - Validation on live telephony audio (narrowband/wideband codecs) and on additional generators such as ElevenLabs.
- **Footer**: Open for Questions & Discussion!

---

## Part 4: Frequently Asked Questions & Defense Points for Presentation

1. **Why does the model issue the final verdict at 10–12 seconds instead of immediately?**
   - *Answer*: Instantaneous 1-second audio slices can be distorted by network packet jitter, hardware AGC, or coughs. Waiting 5 seconds allows the model to compute a stable preliminary average, and 10–12 seconds provides enough speech frames for a reliable final verdict. (The 0.9882 ROC-AUC measures overall separability on the test set, not per-call accuracy.)
2. **How does the system protect caller privacy?**
   - *Answer*: Audio is held only in a 3.0-second circular RAM ring buffer. As new speech arrives, old speech is overwritten in memory. When the call ends, the buffer is zeroed out. No audio files are saved to the server disk.
3. **How does the model handle phone calls where both people talk?**
   - *Answer*: The online diarizer extracts 40-D timbre embeddings and clusters the voices into Speaker A (local user) and Speaker B (remote contact). If both speak simultaneously, the segment is tagged as `OVERLAP` and quarantined so cross-talk does not contaminate the threat score.
4. **Why combine SincNet with Random Forest?**
   - *Answer*: SincNet learns directly on the raw time-domain waveform to catch fine vocoder artifacts, while the Random Forest evaluates 63 physical acoustic features (phase, jitter, shimmer, high-frequency ratio). Blending both (50/50) means an attacker has to evade both representations at once.
5. **How do you handle real phone-line bandwidth limits?**
   - *Answer*: Phone channels are band-limited (about 3.4 kHz narrowband, about 7 kHz wideband). High-frequency features must be interpreted relative to the call's effective bandwidth, and validating this on live telephony audio is a stated roadmap item.

---

## Part 5: Known Limitations (Be Ready to Discuss)

- **Domain gap**: Genuine training speech is studio/read speech (LibriSpeech, VCTK-based ASVspoof), not live compressed phone audio.
- **Codec sensitivity**: The >4 kHz high-frequency ratio carries a 20% weight in the threat score. Narrowband calls have no energy there, so this feature needs bandwidth-aware handling.
- **Small test sets**: The balanced working set is 7,420 clips, so each held-out split has roughly 1,100 clips; the 300-sample ChatterboxTTS result is a small sample.
- **Generator coverage**: ElevenLabs and other commercial generators have not been validated in the reported benchmarks.
- **Diarization assumption**: Speaker A is assumed to be the first detected speaker. If the remote caller speaks first, labels may swap.
- **Speakerphone dependency**: Browser-based capture needs speakerphone mode to hear both sides of a cellular call.
- **Adversarial robustness**: Ensemble fusion raises the bar for evasion but does not guarantee resistance to adaptive attacks.

---

## Part 6: Items to Verify Against Your Code and Results Before Presenting

1. Confirm the 300 ChatterboxTTS clips were excluded from training.
2. Confirm which score the threshold $\tau^* = 0.3985$ applies to (P_RF only, or P_ensemble), and state it consistently.
3. Confirm the human false alarm figures (5.53% now vs. the 79–88% earlier baseline) and that the ROC-AUC/EER are computed on the held-out test split.
4. Confirm the countdown text `(Xs / 10s)` matches the UI, and that the UI shows the preliminary score at 5s.
5. Confirm the GitHub repository URL spelling (`Ai_voice-_cloning`).
6. Add a cited source for fraud-loss statistics on Slide 2.
7. Confirm whether diarization embeddings are held only in memory for the call duration.