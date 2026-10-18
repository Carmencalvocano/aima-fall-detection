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
cap = cv2.VideoCapture("detector/videos/Video Project 3.mp4")

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
    # Que el video sea más grande
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
        
        # REGLA
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        shoulder_x = (
            left_shoulder.x +
            right_shoulder.x
        ) / 2

        shoulder_y = (
            left_shoulder.y +
            right_shoulder.y
        ) / 2

        left_hip = landmarks[23]
        right_hip = landmarks[24]

        hip_x = (
            left_hip.x +
            right_hip.x
        ) / 2

        hip_y = (
            left_hip.y +
            right_hip.y
        ) / 2

        vertical_distance = abs(
            hip_y - shoulder_y
        )

        horizontal_distance = abs(
            hip_x - shoulder_x
        )

        print(
            f"SV={vertical_distance:.2f} "
            f"SH={horizontal_distance:.2f}"
        )

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
        cv2.putText(
            frame,
            f"SV: {vertical_distance:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"SH: {horizontal_distance:.2f}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
    cv2.imshow("Pose Live", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()