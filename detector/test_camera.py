import cv2

cap = cv2.VideoCapture("http://192.168.1.37:4747/video")

while True:
    success, frame = cap.read()

    if not success:
        print("No se pudo leer la cámara")
        break

    cv2.imshow("Camara", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

