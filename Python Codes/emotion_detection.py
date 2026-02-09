import mediapipe as mp
import cv2
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

# Observed min/max values for scaling (adjust if needed)
EYE_MIN, EYE_MAX = 0.015, 0.065
MOUTH_MIN, MOUTH_MAX = 0.010, 0.060
BROW_MIN, BROW_MAX = -0.030, 0.050

def scale(value, min_val, max_val):
    """Scale a value to 50-100% proportionally."""
    value = np.clip(value, min_val, max_val)
    return int(50 + 50 * (value - min_val) / (max_val - min_val))

def detect_emotion(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True
    ) as face_mesh:

        results = face_mesh.process(rgb)
        if not results.multi_face_landmarks:
            return "No Face", 0

        lm = results.multi_face_landmarks[0].landmark

        # -------------------------------------
        # Facial metrics
        # -------------------------------------
        mouth_open = abs(lm[13].y - lm[14].y)
        brow_left = lm[70].y - lm[63].y
        brow_right = lm[300].y - lm[293].y
        avg_brow = (brow_left + brow_right) / 2
        left_eye = abs(lm[159].y - lm[145].y)
        right_eye = abs(lm[386].y - lm[374].y)
        avg_eye = (left_eye + right_eye) / 2

        # -------------------------------------
        # EMOTION RULES (dynamic confidence)
        # -------------------------------------
        # Surprise: wide eyes + open mouth
        if avg_eye > 0.045 and mouth_open > 0.040:
            conf_eye = scale(avg_eye, 0.045, EYE_MAX)
            conf_mouth = scale(mouth_open, 0.040, MOUTH_MAX)
            return "Surprised", min(conf_eye, conf_mouth)

        # Happy: smile (mouth slightly open)
        if mouth_open > 0.020:
            conf_mouth = scale(mouth_open, 0.020, 0.045)
            return "Happy", conf_mouth

        # Angry: eyebrows down + frown
        if avg_brow < -0.010:
            conf_brow = scale(abs(avg_brow), 0.010, 0.030)
            return "Angry", conf_brow

        # Sad: eyebrows up + small mouth
        if avg_brow > 0.020 and mouth_open < 0.015:
            conf_brow = scale(avg_brow, 0.020, BROW_MAX)
            conf_mouth = scale(0.015 - mouth_open, 0.0, 0.015)
            return "Sad", min(conf_brow, conf_mouth)

        # Disgust: uneven eyebrows
        if brow_left > 0.025 and brow_right < -0.010:
            conf_brow = scale(brow_left, 0.025, BROW_MAX)
            return "Disgust", conf_brow

        # Fear: wide eyes + raised eyebrows
        if avg_eye > 0.050 and avg_brow > 0.015:
            conf_eye = scale(avg_eye, 0.050, EYE_MAX)
            conf_brow = scale(avg_brow, 0.015, BROW_MAX)
            return "Fear", min(conf_eye, conf_brow)

        # Sleepy: eyes almost closed
        if avg_eye < 0.018:
            conf_eye = scale(0.018 - avg_eye, 0.0, 0.018)
            return "Sleepy", conf_eye

        # Tired: semi-closed eyes + relaxed mouth
        if avg_eye < 0.028 and mouth_open < 0.015:
            conf_eye = scale(0.028 - avg_eye, 0.0, 0.028)
            conf_mouth = scale(0.015 - mouth_open, 0.0, 0.015)
            return "Tired", min(conf_eye, conf_mouth)

        # Stress: raised eyebrows + tight mouth
        if avg_brow > 0.010 and 0.015 < mouth_open < 0.030:
            conf_brow = scale(avg_brow, 0.010, BROW_MAX)
            conf_mouth = scale(0.030 - mouth_open, 0.0, 0.015)
            return "Stress", min(conf_brow, conf_mouth)

        # Neutral fallback
        return "Neutral", 50

# -----------------------------
# Test with webcam
# -----------------------------
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        emotion, confidence = detect_emotion(frame)
        cv2.putText(frame, f"{emotion} ({confidence}%)", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Emotion Detection", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break
    cap.release()
    cv2.destroyAllWindows()
