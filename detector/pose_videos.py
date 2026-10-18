import cv2
import mediapipe as mp

# -----------------------------
# Configuración MediaPipe
# -----------------------------

BaseOptions = mp.tasks.BaseOptions

PoseLandmarker = mp.tasks.vision.PoseLandmarker

PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions

options = PoseLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="detector/models/pose_landmarker_full.task"
    )
)

landmarker = PoseLandmarker.create_from_options(options)

# -----------------------------
# Video
# -----------------------------

cap = cv2.VideoCapture(
    "detector/videos/Video Project 1.mp4"
)

while True:

    success, frame = cap.read()

    if not success:
        print("No se pudo leer la cámara")
        break
    frame = cv2.resize(
            frame,
            (1280, 720)
        )
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    result = landmarker.detect(mp_image)

    # ¿Hay una persona?
    if result.pose_landmarks:

        landmarks = result.pose_landmarks[0]

        # Dibujar cada landmark
        h, w, _ = frame.shape

        for landmark in landmarks:

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv2.circle(
                frame,
                (x, y),
                4,
                (0, 255, 0),
                -1
            )
        # Para agregar las lineas de unión entre los landmarkers
        connections = mp.tasks.vision.PoseLandmarksConnections.POSE_LANDMARKS

        for connection in connections:

            start_idx = connection.start
            end_idx = connection.end

            start = landmarks[start_idx]
            end = landmarks[end_idx]

            x1 = int(start.x * w)
            y1 = int(start.y * h)

            x2 = int(end.x * w)
            y2 = int(end.y * h)

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )
        # hasta aquí

    cv2.imshow("Pose Live", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()