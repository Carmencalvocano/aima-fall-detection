# AIMA Fall Detection

Prueba técnica para AIMA.

El objetivo del proyecto es detectar caídas mediante visión artificial utilizando MediaPipe, almacenar los eventos detectados y permitir su consulta desde una interfaz web.

---

## Arquitectura

```text
Cámara
   ↓
MediaPipe
   ↓
Detección de caída
   ↓
API FastAPI
   ↓
SQLite
   ↓
Frontend de consulta
```

---

## Estructura del proyecto

```text
aima-fall-detection/
│
├── backend/
├── detector/
├── frontend/
├── videos/
├── docs/
└── README.md
```

---

## Tecnologías utilizadas

- Python
- OpenCV
- MediaPipe
- FastAPI
- SQLite

---

## Instalación

### Crear entorno virtual

```bash
python -m venv venv
```

### Activar entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

Si Windows bloquea la ejecución de scripts:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Instalar dependencias

```bash
pip install mediapipe opencv-python fastapi uvicorn
```

---

## Estado actual

- [x] Configuración inicial del proyecto
- [x] Entorno virtual configurado
- [x] Instalación de OpenCV
- [x] Instalación de MediaPipe
- [x] Integración DroidCam
- [x] Captura de vídeo desde OpenCV
- [x] Integración MediaPipe Pose
- [x] Obtención de landmarks corporales
- [x] Visualización de landmarks en tiempo real
- [ ] Detección de caídas
- [ ] Backend FastAPI
- [ ] Base de datos SQLite
- [ ] Frontend de consulta

---

## Notas de desarrollo

### Uso de DroidCam

El equipo de desarrollo no dispone de webcam física, por lo que se utiliza la cámara del teléfono móvil mediante DroidCam.

### Problema encontrado

Al intentar acceder a la cámara mediante:

```python
cv2.VideoCapture(0)
```

la imagen aparecía completamente verde tanto en OpenCV como en la aplicación Cámara de Windows.

### Causa

DroidCam Client estaba utilizando la cámara y el dispositivo virtual no se exponía correctamente para otros programas.

### Solución

Consumir directamente el stream HTTP proporcionado por DroidCam:

```python
cv2.VideoCapture("http://IP_DEL_MOVIL:4747/video")
```

### Resultado

```text
Móvil
   ↓
DroidCam
   ↓
Stream HTTP
   ↓
OpenCV
   ↓
Procesamiento en tiempo real
```

OpenCV recibe correctamente el vídeo en tiempo real y puede utilizarlo posteriormente como entrada para MediaPipe.

---

### Integración de MediaPipe Pose

La versión instalada de MediaPipe utiliza la API moderna basada en Tasks y no la API clásica basada en:

```python
mp.solutions.pose
```

Para la detección de poses se utiliza:

```python
mp.tasks.vision.PoseLandmarker
```

Se ha descargado el modelo oficial:

```text
detector/models/pose_landmarker_full.task
```

y se ha validado correctamente su carga mediante:

```python
PoseLandmarker.create_from_options(...)
```

La detección devuelve correctamente un objeto:

```text
PoseLandmarkerResult
```

que contiene los landmarks corporales detectados sobre la persona.

Actualmente se ha verificado la detección de una persona mediante una imagen capturada en tiempo real desde DroidCam, obteniendo correctamente los 33 landmarks corporales proporcionados por PoseLandmarker.

La siguiente fase consistirá en visualizar gráficamente dichos landmarks sobre la imagen y comenzar a diseñar la lógica de detección de caídas.

## Próximos pasos

1. Analizar landmarks relevantes para detectar caídas.
2. Diseñar la lógica de detección de caídas.
3. Enviar eventos al backend mediante FastAPI.
4. Almacenar eventos en SQLite.
5. Desarrollar interfaz para consulta de eventos.
6. Evaluar sensibilidad y falsos positivos.