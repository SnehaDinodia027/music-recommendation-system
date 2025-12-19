import cv2

# Simple face-based dummy emotion detector
# (Major project ke liye acceptable + stable)

def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5
    )

    if len(faces) > 0:
        # Face detected → assume Happy (demo logic)
        return "Happy"
    else:
        return "Neutral"
