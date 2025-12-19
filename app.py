from flask import Flask, render_template, request, redirect, url_for, session, Response
import sqlite3
import cv2
from utils.music_mapper import get_music_links   # ✅ FIX
from utils.emotion import detect_emotion

app = Flask(__name__)
app.secret_key = "music_secret_key"

# ================= DATABASE =================
def get_db():
    return sqlite3.connect("database.db")

# ================= HOME =================
@app.route("/")
def index():
    return render_template("index.html")

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users (username,email,password) VALUES (?,?,?)",
            (username, email, password),
        )
        con.commit()
        con.close()
        return redirect(url_for("login"))

    return render_template("register.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password),
        )
        user = cur.fetchone()
        con.close()

        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

# ================= TEXT MOOD =================
@app.route("/text", methods=["GET", "POST"])
def text():
    if request.method == "POST":
        mood = request.form["mood"]
        return redirect(url_for("result", mood=mood))
    return render_template("text.html")

# ================= RESULT =================
@app.route("/result/<mood>")
def result(mood):
    links = get_music_links(mood)   # ✅ FIXED
    return render_template(
        "result.html",
        mood=mood.capitalize(),
        youtube=links["youtube"],
        spotify=links["spotify"],
    )

# ================= CAMERA PAGE =================
@app.route("/camera")
def camera():
    return render_template("camera.html")

# ================= CAMERA FEED =================
def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        emotion = detect_emotion(frame)
        cv2.putText(
            frame,
            f"Emotion: {emotion}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ================= RUN =================
if __name__ == "__main__":
    import socket

    sock = socket.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()

    print(f"✅ Server running on http://127.0.0.1:{port}")
    app.run(debug=True, port=port)
