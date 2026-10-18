import cv2
import mediapipe as mp
import requests

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

FALL_FRAME_THRESHOLD = 5

USE_CAMERA = False
VIDEO_PATH = "detector/videos/fall-03-cam0.mp4"


def create_landmarker():
    options = mp.tasks.vision.PoseLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path="detector/models/pose_landmarker_full.task"
        )
    )
    return mp.tasks.vision.PoseLandmarker.create_from_options(options)


def calculate_distances(landmarks):
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    shoulder_x = (left_shoulder.x + right_shoulder.x) / 2
    shoulder_y = (left_shoulder.y + right_shoulder.y) / 2

    left_hip = landmarks[23]
    right_hip = landmarks[24]
    hip_x = (left_hip.x + right_hip.x) / 2
    hip_y = (left_hip.y + right_hip.y) / 2

    vertical_distance = abs(hip_y - shoulder_y)
    horizontal_distance = abs(hip_x - shoulder_x)

    return vertical_distance, horizontal_distance


def draw_pose(
    frame,
    landmarks,
    vertical_distance,
    horizontal_distance,
    fall_frames,
    fall_detected,
):
    height, width, _ = frame.shape

    for landmark in landmarks:
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

    for index, name in IMPORTANT_LANDMARKS.items():
        landmark = landmarks[index]
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        cv2.putText(
            frame,
            name,
            (x + 10, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 255, 255),
            1,
        )

    connections = mp.tasks.vision.PoseLandmarksConnections.POSE_LANDMARKS
    for connection in connections:
        start = landmarks[connection.start]
        end = landmarks[connection.end]
        cv2.line(
            frame,
            (int(start.x * width), int(start.y * height)),
            (int(end.x * width), int(end.y * height)),
            (255, 0, 0),
            2,
        )

    cv2.putText(
        frame,
        f"SV: {vertical_distance:.2f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
    cv2.putText(
        frame,
        f"SH: {horizontal_distance:.2f}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
    cv2.putText(
        frame,
        f"Frames: {fall_frames}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2,
    )

    if fall_detected:
        cv2.putText(
            frame,
            "FALL DETECTED",
            (350, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 255),
            4,
        )


def update_detection_state(
    vertical_distance,
    horizontal_distance,
    fall_frames,
):
    if vertical_distance < 0.05 and horizontal_distance > 0.10:
        fall_frames += 1
    else:
        fall_frames = 0

    fall_detected = fall_frames >= FALL_FRAME_THRESHOLD

    recovered = (
        vertical_distance > 0.10
        and horizontal_distance < 0.08
    )

    return fall_frames, fall_detected, recovered


def calculate_confidence(vertical_distance, horizontal_distance):
    sv_score = max(0, (0.05 - vertical_distance) / 0.05)
    sh_score = min(horizontal_distance / 0.10, 1)
    return (sv_score + sh_score) / 2


def send_fall_event(confidence):
    try:
        requests.post(
            "http://127.0.0.1:8000/falls",
            json={
                "event_type": "fall",
                "confidence": confidence,
                "source": "mediapipe",
            },
        )
        print("Caída enviada al backend")
        return True
    except Exception as error:
        print(f"Error enviando evento: {error}")
        return False


def main():
    landmarker = create_landmarker()

    video_source = 0 if USE_CAMERA else VIDEO_PATH
    cap = cv2.VideoCapture(video_source)

    fall_frames = 0

    event_sent = False

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
            vertical_distance, horizontal_distance = calculate_distances(landmarks)

            fall_frames, fall_detected, recovered = update_detection_state(
                vertical_distance,
                horizontal_distance,
                fall_frames,
            )

            if recovered:
                print("RECOVERED")
                event_sent = False

            confidence = calculate_confidence(
                vertical_distance,
                horizontal_distance,
            )

            if fall_detected and not event_sent:
                event_sent = send_fall_event(confidence)

            print(
                f"SV={vertical_distance:.2f} "
                f"SH={horizontal_distance:.2f}"
            )

            print(
                f"Frames={fall_frames}"
            )

            draw_pose(
                frame,
                landmarks,
                vertical_distance,
                horizontal_distance,
                fall_frames,
                fall_detected,
            )

        cv2.imshow("Pose Live", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()