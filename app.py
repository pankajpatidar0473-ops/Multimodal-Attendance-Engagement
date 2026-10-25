import io
import sqlite3
from datetime import datetime, date, time
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "attendance.db"

st.set_page_config(page_title="Multimodal Attendance & Engagement Agent", page_icon="🎓", layout="wide")

def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_code TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        class_name TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        session_date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        notes TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'Present',
        check_in TEXT,
        check_out TEXT,
        reviewed INTEGER NOT NULL DEFAULT 0,
        UNIQUE(session_id, student_id),
        FOREIGN KEY(session_id) REFERENCES sessions(id),
        FOREIGN KEY(student_id) REFERENCES students(id)
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS engagement (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        interval_label TEXT NOT NULL,
        movement_score REAL NOT NULL,
        audio_activity_score REAL NOT NULL,
        head_pose_score REAL NOT NULL,
        note TEXT DEFAULT ''
    )""")
    conn.commit()
    return conn

conn = connect()

def read_df(query, params=()):
    return pd.read_sql_query(query, conn, params=params)

def seed_demo():
    if conn.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
        conn.executemany("INSERT INTO students(student_code, full_name, class_name) VALUES(?,?,?)", [
            ("STU001", "Aarav Sharma", "Cyber Security - III"),
            ("STU002", "Diya Patel", "Cyber Security - III"),
            ("STU003", "Kabir Verma", "Cyber Security - III"),
            ("STU004", "Ananya Singh", "Cyber Security - III"),
            ("STU005", "Ishaan Gupta", "Cyber Security - III"),
        ])
    if conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0] == 0:
        today = date.today().isoformat()
        conn.execute("INSERT INTO sessions(title, session_date, start_time, end_time, notes) VALUES(?,?,?,?,?)",
                     ("Introduction to Network Security (Demo)", today, "10:00", "11:00", "Synthetic demonstration data"))
        sid = conn.execute("SELECT id FROM sessions ORDER BY id DESC LIMIT 1").fetchone()[0]
        students = conn.execute("SELECT id FROM students").fetchall()
        statuses = ["Present", "Present", "Present", "Absent", "Present"]
        for (student_id,), status in zip(students, statuses):
            conn.execute("INSERT OR IGNORE INTO attendance(session_id, student_id, status, check_in, check_out, reviewed) VALUES(?,?,?,?,?,?)",
                         (sid, student_id, status, "10:02" if status == "Present" else None, "10:58" if status == "Present" else None, 1))
        for label, m, a, h, note in [
            ("00–10 min", 0.62, 0.30, 0.74, "Opening explanation"),
            ("10–20 min", 0.78, 0.66, 0.70, "Question and answer"),
            ("20–30 min", 0.48, 0.22, 0.55, "Long explanation segment"),
            ("30–40 min", 0.72, 0.71, 0.76, "Small-group discussion"),
            ("40–50 min", 0.58, 0.40, 0.62, "Revision"),
        ]:
            conn.execute("INSERT INTO engagement(session_id, interval_label, movement_score, audio_activity_score, head_pose_score, note) VALUES(?,?,?,?,?,?)",
                         (sid, label, m, a, h, note))
    conn.commit()

seed_demo()

st.title("🎓 Multimodal Attendance & Engagement Agent")
st.caption("Offline-first classroom analytics • Demo data is synthetic • Engagement indicators are estimates, not judgments of learning.")

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Open section", ["Overview", "Students", "Sessions & Attendance", "Engagement Analysis", "Video Analyzer", "Project Guide"])
    st.divider()
    st.caption("Privacy-first prototype")
    st.caption("Student identity and attendance should be reviewed by a human before official use.")

if page == "Overview":
    students = read_df("SELECT * FROM students")
    sessions = read_df("SELECT * FROM sessions")
    att = read_df("""SELECT a.*, s.title, s.session_date, st.full_name, st.student_code
                     FROM attendance a JOIN sessions s ON s.id=a.session_id
                     JOIN students st ON st.id=a.student_id""")
    eng = read_df("SELECT * FROM engagement")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registered students", len(students))
    c2.metric("Sessions recorded", len(sessions))
    present = int((att["status"] == "Present").sum()) if not att.empty else 0
    c3.metric("Present records", present)
    avg = round(float(eng[["movement_score","audio_activity_score","head_pose_score"]].mean().mean())*100) if not eng.empty else 0
    c4.metric("Average activity indicators", f"{avg}%")
    st.subheader("Recent sessions")
    if sessions.empty:
        st.info("Create a session in Sessions & Attendance.")
    else:
        st.dataframe(sessions.sort_values("id", ascending=False), use_container_width=True, hide_index=True)
    st.subheader("Engagement trend (demo or recorded measurements)")
    if not eng.empty:
        chart = eng[["interval_label","movement_score","audio_activity_score","head_pose_score"]].set_index("interval_label")
        st.line_chart(chart, y=["movement_score","audio_activity_score","head_pose_score"])
    st.info("The starter app includes synthetic sample records so the dashboard is demonstrable immediately. Replace them with consented, reviewed data.")

elif page == "Students":
    st.subheader("Student register")
    with st.form("add_student", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        code = col1.text_input("Student ID / code", placeholder="STU006")
        name = col2.text_input("Full name")
        cls = col3.text_input("Class / cohort", value="Cyber Security - III")
        submitted = st.form_submit_button("Add student")
        if submitted:
            if not code.strip() or not name.strip():
                st.error("Student code and name are required.")
            else:
                try:
                    conn.execute("INSERT INTO students(student_code, full_name, class_name) VALUES(?,?,?)",
                                 (code.strip(), name.strip(), cls.strip()))
                    conn.commit()
                    st.success("Student added.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("That student code already exists.")
    df = read_df("SELECT student_code AS 'Student ID', full_name AS 'Full name', class_name AS 'Class' FROM students ORDER BY full_name")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("Download student register CSV", df.to_csv(index=False).encode("utf-8"), "students.csv", "text/csv")

elif page == "Sessions & Attendance":
    st.subheader("Create a session")
    with st.form("new_session", clear_on_submit=True):
        title = st.text_input("Session title", placeholder="Introduction to Network Security")
        c1, c2, c3 = st.columns(3)
        session_date = c1.date_input("Date", value=date.today())
        start = c2.time_input("Start time", value=time(10, 0))
        end = c3.time_input("End time", value=time(11, 0))
        notes = st.text_input("Notes (optional)")
        create = st.form_submit_button("Create session")
        if create:
            if not title.strip():
                st.error("Enter a session title.")
            else:
                cur = conn.execute("INSERT INTO sessions(title, session_date, start_time, end_time, notes) VALUES(?,?,?,?,?)",
                                   (title.strip(), session_date.isoformat(), start.strftime("%H:%M"), end.strftime("%H:%M"), notes.strip()))
                sid = cur.lastrowid
                conn.executemany("INSERT OR IGNORE INTO attendance(session_id, student_id, status, reviewed) VALUES(?,?,?,0)",
                                 [(sid, row[0], "Unmarked") for row in conn.execute("SELECT id FROM students").fetchall()])
                conn.commit()
                st.success("Session created and attendance initialized as Unmarked.")
                st.rerun()
    sessions = read_df("SELECT id, title, session_date, start_time, end_time FROM sessions ORDER BY session_date DESC, id DESC")
    if sessions.empty:
        st.info("Create a session to begin.")
    else:
        st.subheader("Select session")
        options = {f"#{r.id} — {r.title} ({r.session_date})": int(r.id) for r in sessions.itertuples()}
        selected_label = st.selectbox("Session", list(options.keys()))
        sid = options[selected_label]
        attendance_df = read_df("""SELECT a.id, st.student_code AS 'Student ID', st.full_name AS 'Full name',
                                   a.status AS Status, COALESCE(a.check_in,'') AS 'Check-in',
                                   COALESCE(a.check_out,'') AS 'Check-out', a.reviewed AS Reviewed
                                   FROM attendance a JOIN students st ON st.id=a.student_id
                                   WHERE a.session_id=? ORDER BY st.full_name""", (sid,))
        edited = st.data_editor(attendance_df, use_container_width=True, hide_index=True,
                                column_config={"Status": st.column_config.SelectboxColumn(options=["Present","Absent","Late","Unmarked"]),
                                               "Reviewed": st.column_config.CheckboxColumn()},
                                disabled=["id","Student ID","Full name"], key=f"attendance_{sid}")
        if st.button("Save attendance changes"):
            for row in edited.itertuples(index=False):
                conn.execute("UPDATE attendance SET status=?, check_in=?, check_out=?, reviewed=? WHERE id=?",
                             (row.Status, row._4 or None, row._5 or None, int(bool(row.Reviewed)), int(row.id)))
            conn.commit()
            st.success("Attendance changes saved.")
            st.rerun()
        csv_df = read_df("""SELECT s.title AS Session, s.session_date AS Date, st.student_code AS 'Student ID',
                            st.full_name AS Student, a.status AS Status, a.check_in AS 'Check-in',
                            a.check_out AS 'Check-out', a.reviewed AS 'Human reviewed'
                            FROM attendance a JOIN students st ON st.id=a.student_id
                            JOIN sessions s ON s.id=a.session_id WHERE a.session_id=? ORDER BY st.full_name""", (sid,))
        st.download_button("Export selected session CSV", csv_df.to_csv(index=False).encode("utf-8"),
                           f"attendance_session_{sid}.csv", "text/csv")
        st.caption("Tip: leave automated detections as Unmarked until a responsible person verifies them.")

elif page == "Engagement Analysis":
    st.subheader("Session engagement indicators")
    sessions = read_df("SELECT id, title, session_date FROM sessions ORDER BY id DESC")
    if sessions.empty:
        st.info("Create a session first.")
    else:
        options = {f"#{r.id} — {r.title} ({r.session_date})": int(r.id) for r in sessions.itertuples()}
        selected = st.selectbox("Session to analyze", list(options.keys()))
        sid = options[selected]
        with st.form("add_engagement"):
            st.write("Add interval measurements (0.0–1.0). Use these for manually reviewed observations or output from a signal-processing module.")
            label = st.text_input("Interval label", placeholder="50–60 min")
            c1, c2, c3 = st.columns(3)
            movement = c1.slider("Movement activity", 0.0, 1.0, 0.5, 0.05)
            audio = c2.slider("Audio activity", 0.0, 1.0, 0.4, 0.05)
            pose = c3.slider("Head-pose / forward-facing estimate", 0.0, 1.0, 0.6, 0.05)
            note = st.text_input("Context note")
            add = st.form_submit_button("Save interval")
            if add:
                if not label.strip():
                    st.error("Enter an interval label.")
                else:
                    conn.execute("INSERT INTO engagement(session_id, interval_label, movement_score, audio_activity_score, head_pose_score, note) VALUES(?,?,?,?,?,?)",
                                 (sid, label.strip(), movement, audio, pose, note.strip()))
                    conn.commit()
                    st.success("Interval saved.")
                    st.rerun()
        eng = read_df("SELECT interval_label AS Interval, movement_score AS Movement, audio_activity_score AS 'Audio activity', head_pose_score AS 'Head pose', note AS Context FROM engagement WHERE session_id=? ORDER BY id", (sid,))
        if not eng.empty:
            st.line_chart(eng.set_index("Interval")[["Movement","Audio activity","Head pose"]])
            st.dataframe(eng, use_container_width=True, hide_index=True)
            avg = eng[["Movement","Audio activity","Head pose"]].mean()
            st.subheader("Agent suggestions")
            if avg["Audio activity"] < 0.35 and avg["Movement"] < 0.45:
                st.warning("Low observed activity in this sample. Consider asking a short comprehension question or adding a brief pair discussion; verify the classroom context first.")
            elif avg["Audio activity"] > 0.65:
                st.info("Audio activity is elevated. It may indicate discussion, questions, or background noise. Check the context before interpreting it.")
            else:
                st.success("Signals are mixed or moderate. Consider alternating explanation with a quick knowledge check and compare trends across sessions.")
            st.caption("Suggestions are rule-based decision support, not an assessment of individual students.")
            st.download_button("Export engagement CSV", eng.to_csv(index=False).encode("utf-8"), f"engagement_{sid}.csv", "text/csv")
        else:
            st.info("No intervals yet. Add one above, or use the demo session already included.")

elif page == "Video Analyzer":
    st.subheader("Offline video signal analyzer")
    st.write("Upload a short video file to estimate coarse frame-to-frame movement. The prototype does not identify people or infer mental states.")
    uploaded = st.file_uploader("Upload a video", type=["mp4","mov","avi","mkv"])
    if uploaded:
        try:
            import cv2
            import tempfile
            import numpy as np
            suffix = Path(uploaded.name).suffix or ".mp4"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded.getbuffer())
                tmp_path = tmp.name
            cap = cv2.VideoCapture(tmp_path)
            if not cap.isOpened():
                st.error("Could not open this video. Try MP4 encoded with H.264.")
            else:
                fps = cap.get(cv2.CAP_PROP_FPS) or 25
                frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
                duration = frames / fps if fps else 0
                st.metric("Approximate duration", f"{duration:.1f} seconds")
                st.caption("Processing is sampled to limit CPU use. Only aggregate motion scores are shown.")
                prev = None
                scores = []
                idx = 0
                while True:
                    ok, frame = cap.read()
                    if not ok:
                        break
                    if idx % max(1, int(fps)) == 0:
                        small = cv2.resize(frame, (320, 180))
                        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
                        gray = cv2.GaussianBlur(gray, (5,5), 0)
                        if prev is not None:
                            diff = cv2.absdiff(prev, gray)
                            scores.append(float(np.mean(diff) / 255.0))
                        prev = gray
                    idx += 1
                    if idx > int(fps * 180):
                        break
                cap.release()
                if scores:
                    results = pd.DataFrame({"Sample": list(range(1, len(scores)+1)), "Motion score": scores})
                    st.line_chart(results.set_index("Sample"))
                    st.metric("Mean frame-difference score", f"{sum(scores)/len(scores):.3f}")
                    st.info("Motion can come from camera movement, lighting, or any scene change. This is not a student-level engagement score.")
                else:
                    st.warning("Not enough frames were available to calculate motion.")
        except ImportError:
            st.error("OpenCV is not installed. Run: pip install opencv-python-headless")
        except Exception as exc:
            st.error(f"Video processing failed: {exc}")
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
    else:
        st.info("For your first demo, use the Overview and Engagement Analysis pages with synthetic data. Video analysis is optional.")

elif page == "Project Guide":
    st.subheader("Project architecture")
    st.code("""Video/audio input (local)
       ↓
Signal extraction (OpenCV / optional VAD)
       ↓
Aggregate time-window features
       ↓
Attendance candidates + engagement trends
       ↓
Human review + rule-based teaching suggestions
       ↓
Streamlit dashboard + SQLite + CSV reports""", language="text")
    st.subheader("Milestones")
    st.markdown("""
1. **MVP:** student register, sessions, manual attendance, SQLite, CSV export.
2. **Analytics:** interval-level activity indicators, charts, rule-based suggestions.
3. **Video prototype:** coarse frame-difference motion score.
4. **Advanced modules:** consent-based participant tracking, pose estimation, voice activity detection.
5. **Delivery:** README, screenshots, tests, GitHub repository, and hosted demo or demo recording.
""")
    st.subheader("Privacy and limitations")
    st.markdown("""
- Process recordings locally and obtain consent before recording.
- Avoid uploading raw student video/audio to public repositories or hosting services.
- Do not use facial expression or head direction as a definitive measure of attention.
- Keep a human in the loop for attendance corrections.
- Use synthetic data in screenshots and demo deployments.
- Provide retention and deletion controls before real classroom use.
""")
    st.subheader("Run locally")
    st.code("python -m venv .venv\n# Windows PowerShell\n.\\.venv\\Scripts\\Activate.ps1\npip install -r requirements.txt\nstreamlit run app.py", language="powershell")

