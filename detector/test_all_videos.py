from pathlib import Path

import cv2
import mediapipe as mp

from fall_detector import (
    calculate_distances,
    create_landmarker,
    update_detection_state,
)


VIDEO_DIR = Path(__file__).parent / "videos"


def check_video(video_path, landmarker):
    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        raise RuntimeError(f"No se pudo abrir el vídeo: {video_path}")

    fall_frames = 0
    event_sent = False
    detected_falls = 0

    try:
        while True:
            success, frame = capture.read()
            if not success:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame,
            )
            result = landmarker.detect(image)

            if not result.pose_landmarks:
                continue

            landmarks = result.pose_landmarks[0]
            vertical_distance, horizontal_distance = calculate_distances(
                landmarks
            )

            fall_frames, fall_detected, recovered = update_detection_state(
                vertical_distance,
                horizontal_distance,
                fall_frames,
            )

            if recovered:
                event_sent = False

            if fall_detected and not event_sent:
                detected_falls += 1
                event_sent = True

        return detected_falls

    finally:
        capture.release()


def main():
    video_paths = sorted(VIDEO_DIR.glob("*.mp4"))

    if not video_paths:
        print(f"No se encontraron vídeos en {VIDEO_DIR}")
        return

    landmarker = create_landmarker()

    try:
        for video_path in video_paths:
            detected_falls = check_video(video_path, landmarker)
            result = "DETECTADA" if detected_falls else "NO DETECTADA"
            print(
                f"{video_path.name}: {result} "
                f"({detected_falls} caída(s) detectada(s))"
            )
    finally:
        landmarker.close()


if __name__ == "__main__":
    main()