# Virtual 8086 Stepper Motor Laboratory — Enhanced Edition

A dark-themed Streamlit educational simulator for the 8086 stepper-motor interfacing experiment.

## Features
- Dashboard and virtual rotor display
- Clockwise / anticlockwise finite-step simulation
- Selectable step angle, step count and delay
- Assembly reference tabs (ROR / ROL)
- Hardware block diagram and connection notes
- Phase waveform explorer
- Memory and I/O port inspector
- Experiment guide and observation table
- Quiz / assessment and troubleshooting guide
- Execution log

> Safety: software simulation only. It does not control real hardware. Verify trainer-specific I/O addresses, phase patterns, wiring and power connections against the actual kit manual. Never connect motor coils directly to CPU I/O pins.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Render
Create a Web Service from your GitHub repository.
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Root directory: blank if files are in repository root.
