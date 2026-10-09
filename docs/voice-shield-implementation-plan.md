# Voice Shield AI: Full-Stack Implementation Plan

**System Name:** Voice Shield AI  
**Repository:** [https://github.com/aayash317-svg/hack.git](https://github.com/aayash317-svg/hack.git) / [https://github.com/aayash317-svg/Ai_voice-_cloning](https://github.com/aayash317-svg/Ai_voice-_cloning)  
**Document Version:** 1.0  
**Target Architecture:** FastAPI WebSocket Streaming + PyTorch SincNet + Scikit-Learn Random Forest + Zero-Retention RAM Buffer + Vanilla JS Cyber Dashboard  

---

## 1. System Overview & Technical Objectives

Voice Shield AI is a real-time conversational voice cloning detection and phone call defense engine. It protects financial transactions and phone calls from generative AI deepfake audio (ElevenLabs, ChatterboxTTS, HiFi-GAN) by processing live audio over WebSockets with:
1. **Zero-Retention Privacy:** No audio is written to disk; audio lives exclusively in a 3.0-second circular RAM ring buffer.
2. **Real-Time Conversational Diarization:** Isolates the local user (Speaker A) from the remote contact (Speaker B) without pre-enrollment.
3. **Dual-Model Ensemble:** Combines a 1D raw-waveform SincNet convolutional model with a 63-dimensional physics-informed acoustic Random Forest.
4. **Progressive Evaluation Timeline (10–12s Rule):** Baseline room calibration (0–5s), preliminary rolling score (5–10s), and immutable final consolidated verdict (10–12s).
5. **Cryptographic AuditChain:** Tamper-evident SHA-256 block ledger recording call inspection metadata without raw biometrics.

---

## 2. Target Technology Stack

| Layer | Component | Technologies |
| :--- | :--- | :--- |
| **Frontend** | Live Cyber Dashboard | HTML5, CSS3, Vanilla JS, Web Audio API, Canvas 2D (60 FPS Oscilloscope) |
| **Networking** | Real-Time Transport | Native WebSockets (Binary 16 kHz PCM upstream, JSON telemetry downstream) |
| **Backend Core**| Streaming Application | Python 3.11, FastAPI, Uvicorn, WebSockets, asyncio |
| **Signal Processing** | Audio DSP & Diarization | NumPy, SciPy (Hilbert transform, signal filtering), Librosa (MFCCs, spectral features) |
| **Deep Learning** | Raw Waveform Model | PyTorch (1D SincNet Convolutions with learnable bandpass sinc filters) |
| **Classical ML** | Acoustic Feature Model | Scikit-learn (Random Forest, Platt probability calibration, joblib) |
| **Security & Audit** | Cryptographic Ledger | Python `hashlib` (SHA-256 Hash Chain), Ephemeral RAM Array |
| **Testing** | Automated Test Suite | pytest, pytest-asyncio, FastAPI TestClient, NumPy testing |

---

## 3. Proposed Directory Structure

```text
/Users/manoranjankumar.s/Documents/new hack/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI server & WebSocket /stream/call endpoint
│   │   ├── core/
│   │   │   ├── config.py            # Audio sample rate (16kHz), buffer size, threshold configs
│   │   │   └── audit_chain.py       # SHA-256 tamper-evident hash-chained block ledger
│   │   ├── audio/
│   │   │   ├── __init__.py
│   │   │   ├── buffer.py            # AudioPrivacyBuffer: 3.0s ephemeral circular RAM ring
│   │   │   ├── vad.py               # Energy & zero-crossing Voice Activity Detector
│   │   │   └── diarizer.py          # 40-D Timbre embedding & adaptive cosine centroid clustering
│   │   ├── features/
│   │   │   ├── __init__.py
│   │   │   ├── acoustic_extractor.py# 63-D physics extractor (phase variance, HF ratio, jitter)
│   │   │   └── hilbert_phase.py     # Instantaneous phase derivative variance calculator
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── sincnet.py           # PyTorch SincNet 1D raw-waveform neural architecture
│   │   │   ├── random_forest.py     # 63-D Random Forest loader & Platt probability calibrator
│   │   │   └── ensemble.py          # Consensus late fusion (0.50 P_RF + 0.50 P_Neural)
│   │   ├── engine/
│   │   │   ├── __init__.py
│   │   │   ├── threat_engine.py     # Multi-signal scoring formula & context multipliers
│   │   │   └── timeline.py          # 3-Stage Progressive Evaluation Controller (0-5s, 5-10s, 10-12s)
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── stream.py            # WebSocket handler & audio packet dispatcher
│   │       └── audit.py             # GET /audit/verify & GET /audit/blocks endpoints
│   ├── tests/
│   │   ├── test_buffer.py           # Verification of RAM ring, zero disk writes, overwrite logic
│   │   ├── test_diarization.py      # Speaker A vs Speaker B separation & overlap quarantine
│   │   ├── test_features.py         # Hilbert phase, HF cutoff, and pitch micro-jitter calculations
│   │   ├── test_ensemble.py         # SincNet + RF late fusion and threshold validation
│   │   ├── test_timeline.py         # 10–12s rule & progressive score escalation
│   │   └── test_audit_chain.py      # SHA-256 block hash integrity & tamper detection
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html                   # Glassmorphic Cyber Security Dashboard
│   ├── css/
│   │   ├── variables.css            # Dark mode tokens (#121212, #1E1E1E, #38B6FF, #FF5A5F)
│   │   ├── base.css                 # Layout resets and typography
│   │   └── dashboard.css            # Live gauge, speaker ribbons, oscilloscope styling
│   └── js/
│       ├── audio_streamer.js        # Web Audio API 16 kHz resampler + keep-alive loop
│       ├── websocket_client.js      # Binary chunk transmission & JSON telemetry listener
│       ├── oscilloscope.js          # 60 FPS Canvas 2D raw vocal waveform visualization
│       ├── ui_controller.js         # Threat gauge updates, countdown timer, speaker cards
│       └── audit_viewer.js          # Tamper-evident ledger inspector modal
├── docs/
│   ├── voice-shield-implementation-plan.md
│   ├── ui-ux-design-specification.md
│   └── campus-safety-system-design.md
├── new_system_plan.md
├── .gitignore
└── README.md
```

---

## 4. Phase-by-Phase Implementation Roadmap

### Phase 1: Environment & Core Audio Ingestion Pipeline
1. Set up Python virtual environment (`backend/.venv`) and install dependencies:
   - `fastapi`, `uvicorn[standard]`, `websockets`, `numpy`, `scipy`, `torch`, `scikit-learn`, `librosa`, `pytest`.
2. Implement **`AudioPrivacyBuffer`**:
   - Fixed-size NumPy `float32` array of length 48,000 (3 seconds at 16,000 Hz).
   - Write pointer tracking with circular overwrite.
   - Zero-fill wipe method on stream termination.
   - Strict unit test verifying no file handles or disk caching exist.
3. Build FastAPI WebSocket server (`/stream/call`):
   - Accepts binary chunks (`Int16` PCM, 250ms duration = 4,000 samples).
   - Converts to normalized `float32` [-1.0, 1.0] and pushes into `AudioPrivacyBuffer`.

### Phase 2: Real-Time Conversational Diarization Engine
1. Implement **Voice Activity Detector (VAD)**:
   - Root-mean-square (RMS) energy threshold + Zero-Crossing Rate (ZCR) gating to filter background room noise.
2. Implement **40-D Timbre Feature Extractor**:
   - 19 MFCC mean values + 19 MFCC standard deviations + Spectral Centroid + Spectral Rolloff.
3. Implement **Adaptive Cosine Centroid Clustering**:
   - Centroid A initialized on first valid speech segment (local user).
   - Centroid B created when cosine distance $d(u, v) = 1.0 - \frac{u \cdot v}{\|u\| \|v\|} > 0.025$.
   - Exponential Moving Average ($\alpha = 0.02$) adapts to pitch variations throughout call.
   - Segments matching both or exceeding overlap threshold are flagged `OVERLAP` and quarantined from threat scoring.

### Phase 3: Forensic Feature Engineering & ML Detection Ensemble
1. Implement **Physics-Informed Acoustic Features (63 Dimensions)**:
   - **Phase Derivative Variance**: Hilbert transform analytic signal $\Delta\phi/\Delta t$ variance.
   - **High-Frequency Spectral Cutoff Ratio**: Energy ratio above 4,000 Hz relative to total bandwidth.
   - **Glottal Pitch Micro-Jitter & Shimmer**: Parabolic pitch interpolation measuring cycle-to-cycle perturbation.
2. Implement **SincNet 1D Raw Waveform Neural Network**:
   - PyTorch module utilizing parameterized bandpass sinc filters directly on raw waveform slices.
   - Outputs neural clone probability $P_{\text{Neural}}$.
3. Implement **Calibrated Random Forest & Consensus Fusion**:
   - 100-tree Random Forest accepting 63 acoustic features with Platt scaling calibration.
   - Fusion layer: $P_{\text{ensemble}} = 0.50 \cdot P_{\text{RF}} + 0.50 \cdot P_{\text{Neural}}$.
   - Calibrated decision threshold $\tau^* = 0.3985$.

### Phase 4: Dynamic Threat Engine & 3-Stage Progressive Evaluation
1. Implement **Multi-Signal Threat Engine**:
   - Fuses ensemble score with physical sub-band anomalies (50% ML + 20% HF + 15% Phase + 10% Jitter + 5% Stability).
   - Context multiplier: adds +12% risk if financial transfer / OTP keywords are flagged.
2. Implement **Progressive Evaluation Timeline**:
   - `0.0s – 5.0s (Stage 0)`: Baseline room calibration; returns live countdown ticker `(Xs / 10s)`.
   - `5.0s – 10.0s (Stage 1)`: Preliminary rolling score providing immediate situational awareness.
   - `10.0s – 12.0s (Stage 2)`: Consolidated final verdict (`CALL AUTHENTIC` or `CRITICAL CLONE DETECTED`). Guarantees verdict by 12s even during silent pauses.

### Phase 5: SHA-256 AuditChain & Telemetry Dispatcher
1. Implement **`AuditChain`**:
   - Immutable in-memory block chain storing call ID, timestamp, verdict, speaker turn counts, and previous block hash.
   - Expose `/audit/verify` endpoint to mathematically validate ledger integrity.
2. Build WebSocket telemetry serializer:
   - Emits 10 Hz JSON telemetry packets:
     ```json
     {
       "call_time_seconds": 6.25,
       "stage": "STAGE_1_PRELIMINARY",
       "countdown_seconds": 3.75,
       "threat_score": 14.2,
       "verdict": "ANALYZING",
       "active_speaker": "SPEAKER_B",
       "speaker_a_risk": 4.1,
       "speaker_b_risk": 18.5,
       "metrics": {
         "phase_variance": 0.082,
         "hf_cutoff_ratio": 0.124,
         "jitter_pct": 0.42
       }
     }
     ```

### Phase 6: Glassmorphic Cyber Dashboard (Frontend)
1. Build `index.html` with the `#121212` / `#1E1E1E` / `#38B6FF` / `#FF5A5F` theme.
2. Implement **Web Audio Ingestion**:
   - Browser `navigator.mediaDevices.getUserMedia` captures mic / speakerphone audio.
   - AudioWorklet / ScriptProcessor downsamples to 16 kHz Mono PCM.
   - Mobile keep-alive loop (`gain = 0.00001`).
3. Implement **60 FPS Real-Time Oscilloscope**:
   - HTML5 Canvas rendering time-domain audio energy waveforms with color transitions (cyan $\rightarrow$ amber $\rightarrow$ coral red).
4. Implement **Dynamic Threat Gauge & Action Banners**:
   - Radial / linear threat gauge with color transitions.
   - Dynamic recommendation banners:
     - *Green (< 20%)*: "Call Authentic — Secure to proceed"
     - *Yellow (20–40%)*: "Caution — High pitch variance detected"
     - *Red (> 40%)*: "CRITICAL CLONE DETECTED — FREEZE FINANCIAL TRANSFERS"
5. Add Dual-Speaker Turn Cards & Cryptographic Audit Modal.

---

## 5. Verification & Testing Milestones

| Milestone | Target Test Cases | Success Criteria |
| :--- | :--- | :--- |
| **M1: Zero-Retention RAM Buffer** | `test_buffer.py` | Overwrites oldest frames after 3s; wipes cleanly on close; 0 bytes written to disk. |
| **M2: Diarization & Separation** | `test_diarization.py` | Cleanly distinguishes 2 synthetic speaker timbres; tags simultaneous speech as `OVERLAP`. |
| **M3: Acoustic Feature Engine** | `test_features.py` | Accurately extracts phase variance, HF ratio, and glottal jitter within known tolerances. |
| **M4: Consensus ML & Calibration** | `test_ensemble.py` | $P_{\text{ensemble}}$ computed within [0, 1]; calibrated threshold $\tau^* = 0.3985$ correctly classifies sample clones. |
| **M5: 10–12s Progressive Timeline**| `test_timeline.py` | Stage 0 holds preliminary score; Stage 1 outputs rolling score at 5s; Stage 2 guarantees verdict by 12s. |
| **M6: AuditChain Hash Integrity** | `test_audit_chain.py`| Appends blocks; tampering any block causes `/audit/verify` to fail. |
| **M7: Live End-to-End WebSocket** | `test_stream_e2e.py` | Audio chunk ingestion to telemetry dispatch round-trip < 90 ms. |

---

## 6. Execution Priority

1. **Step 1:** Initialize repository structure (`backend/` and `frontend/`) and requirements.
2. **Step 2:** Build core audio processing (`AudioPrivacyBuffer`, VAD, Diarizer).
3. **Step 3:** Implement acoustic feature extraction & dual ensemble engine.
4. **Step 4:** Build the progressive threat engine & AuditChain.
5. **Step 5:** Create the WebSocket endpoint and live Cyber Dashboard.
6. **Step 6:** Run test suite and demonstrate end-to-end live detection.
