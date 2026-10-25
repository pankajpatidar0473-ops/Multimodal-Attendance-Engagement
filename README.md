<<<<<<< HEAD
# Multimodal Attendance & Engagement Agent

An offline-first educational analytics prototype built with Python, Streamlit, SQLite, Pandas, and OpenCV.

## Features

- Student register
- Session creation and attendance register
- Human-reviewed attendance status
- CSV export for student register and attendance
- Session-level movement, audio-activity, and head-pose indicator charts
- Transparent, rule-based teaching suggestions
- Optional coarse motion analysis from an uploaded video
- SQLite storage on the local machine
- Synthetic sample records for an immediate demo

## Quick start

Python 3.10–3.12 is recommended.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

## First demo walkthrough

1. Open **Overview** and show the synthetic sample dashboard.
2. Open **Students** and add a sample student.
3. Open **Sessions & Attendance**, create a session, mark statuses, and save.
4. Export the attendance CSV.
5. Open **Engagement Analysis**, add a time interval and show the chart and suggestions.
6. Optionally open **Video Analyzer** and upload a short, non-sensitive test clip.

## Project structure

```text
multimodal-attendance-agent/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

The SQLite database is created automatically on first run and is intentionally excluded from Git.

## Architecture

Local video/audio input → signal processing → aggregate time-window features → attendance candidates and engagement trends → human review and suggestions → dashboard and CSV exports.

## Privacy, safety, and limitations

- Sample records are synthetic and intended for demonstration.
- Get informed consent before processing real classroom video or audio.
- Do not commit identifiable student information, database files, recordings, or secrets to GitHub.
- Motion, audio activity, and head-pose indicators are noisy proxies. They do not prove attention, comprehension, or learning.
- Attendance results should be verified by an authorized human before being used for official records.
- The current video module calculates coarse frame differences only; it does not perform face recognition, identity matching, or student-level tracking.
- The suggestion engine is rule-based rather than a generative AI model. It is deliberately transparent and can be extended after the MVP is stable.

## Deployment

For a public demo, use synthetic data only. Streamlit Community Cloud can host the interface, but the current SQLite file is local to the running instance and may not be persistent across restarts or replicas. Do not deploy identifiable student data to a public demo. The app is designed to run locally for offline use.

## Future improvements

- Optional MediaPipe pose extraction
- Voice activity detection with no speech transcription by default
- Explicit consent and retention/deletion controls
- Tests for database operations and attendance calculations
- Session report PDF
- Authentication and role-based access
- Pluggable local language model for explanations and suggestions

## License

MIT License. See `LICENSE`.
=======
<<<<<<< HEAD
# Multimodal Attendance & Engagement Agent

An offline-first educational analytics prototype built with Python, Streamlit, SQLite, Pandas, and OpenCV.

## Features

- Student register
- Session creation and attendance register
- Human-reviewed attendance status
- CSV export for student register and attendance
- Session-level movement, audio-activity, and head-pose indicator charts
- Transparent, rule-based teaching suggestions
- Optional coarse motion analysis from an uploaded video
- SQLite storage on the local machine
- Synthetic sample records for an immediate demo

## Quick start

Python 3.10–3.12 is recommended.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

## First demo walkthrough

1. Open **Overview** and show the synthetic sample dashboard.
2. Open **Students** and add a sample student.
3. Open **Sessions & Attendance**, create a session, mark statuses, and save.
4. Export the attendance CSV.
5. Open **Engagement Analysis**, add a time interval and show the chart and suggestions.
6. Optionally open **Video Analyzer** and upload a short, non-sensitive test clip.

## Project structure

```text
multimodal-attendance-agent/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

The SQLite database is created automatically on first run and is intentionally excluded from Git.

## Architecture

Local video/audio input → signal processing → aggregate time-window features → attendance candidates and engagement trends → human review and suggestions → dashboard and CSV exports.

## Privacy, safety, and limitations

- Sample records are synthetic and intended for demonstration.
- Get informed consent before processing real classroom video or audio.
- Do not commit identifiable student information, database files, recordings, or secrets to GitHub.
- Motion, audio activity, and head-pose indicators are noisy proxies. They do not prove attention, comprehension, or learning.
- Attendance results should be verified by an authorized human before being used for official records.
- The current video module calculates coarse frame differences only; it does not perform face recognition, identity matching, or student-level tracking.
- The suggestion engine is rule-based rather than a generative AI model. It is deliberately transparent and can be extended after the MVP is stable.

## Deployment

For a public demo, use synthetic data only. Streamlit Community Cloud can host the interface, but the current SQLite file is local to the running instance and may not be persistent across restarts or replicas. Do not deploy identifiable student data to a public demo. The app is designed to run locally for offline use.

## Future improvements

- Optional MediaPipe pose extraction
- Voice activity detection with no speech transcription by default
- Explicit consent and retention/deletion controls
- Tests for database operations and attendance calculations
- Session report PDF
- Authentication and role-based access
- Pluggable local language model for explanations and suggestions

## License

MIT License. See `LICENSE`.
=======
# Multimodal-Attendance-Engagement
>>>>>>> fccb810cbaa1cce90f28ec5663f382b79896ee1e
>>>>>>> e74e55c982eb71349e95ed051d889cfa22280ad7
