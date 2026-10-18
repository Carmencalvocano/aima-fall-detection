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
# Cámara
# -----------------------------
# cap = cv2.VideoCapture("http://192.168.1.42:4747/video")
cap = cv2.VideoCapture(0)

# Diccionario con los landmarks más importantes
IMPORTANT_LANDMARKS = {
    0: "Nariz",
    11: "Hombro Izq",
    12: "Hombro Der",
    23: "Cadera Izq",
    24: "Cadera Der",
    27: "Tobillo Izq",
    28: "Tobillo Der"
}

while True:

    success, frame = cap.read()

    if not success:
        print("No se pudo leer la cámara")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    result = landmarker.detect(mp_image)

    # ¿Hay una persona?
    if result.pose_landmarks:

        landmarks = result.pose_landmarks[0]

        # Para observar como cambian los parámetros en la nariz
        nose = landmarks[0]

        print(
            f"Nariz -> "
            f"x={nose.x:.2f} "
            f"y={nose.y:.2f} "
            f"visibility={nose.visibility:.2f}"
        )
        # hasta aquí

        # Para dibujar circulos a los landmarkers
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
        # hasta aquí

        # Para agregar nombres a los landmarkers
        for idx, name in IMPORTANT_LANDMARKS.items():

            landmark = landmarks[idx]

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv2.putText(
                frame,
                name,
                (x + 10, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 255, 255),
                1
            )
        # hasta aquí

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