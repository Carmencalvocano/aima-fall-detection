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
- [x] Visualización del esqueleto en tiempo real
- [x] Backend FastAPI
- [x] Base de datos SQLite
- [x] Almacenamiento de eventos detectados
- [x] Análisis de landmarks relevantes (nariz, hombros, caderas y tobillos)
- [ ] Detección de caídas
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

La detección de landmarks se ha integrado correctamente sobre vídeo en tiempo real. Actualmente se visualizan tanto los landmarks individuales como el esqueleto corporal completo generado por MediaPipe Pose.

La siguiente fase consistirá en analizar los landmarks más relevantes (hombros, caderas, tobillos y nariz) para diseñar e implementar la lógica de detección de caídas.

---

### Análisis de landmarks

Se ha realizado una fase de exploración de los landmarks proporcionados por MediaPipe Pose para comprender su funcionamiento y evaluar su utilidad para la detección de caídas.

Durante esta fase se han analizado las propiedades:

```text
x
y
z
visibility
presence
```

Se ha verificado que MediaPipe devuelve 33 landmarks corporales normalizados y que cada uno de ellos dispone de métricas de confianza asociadas.

Para facilitar la experimentación se ha desarrollado una visualización en tiempo real que muestra:

```text
- Landmarks corporales
- Esqueleto completo
- Etiquetas de landmarks relevantes
```

Los landmarks identificados como más relevantes para la detección de caídas son:

```text
0  -> Nariz

11 -> Hombro izquierdo
12 -> Hombro derecho

23 -> Cadera izquierda
24 -> Cadera derecha

27 -> Tobillo izquierdo
28 -> Tobillo derecho
```

Estos puntos serán utilizados en la siguiente fase para diseñar la lógica de detección de caídas.

---

### Backend y almacenamiento de eventos

Se ha desarrollado un backend utilizando FastAPI para recibir y almacenar eventos detectados por el sistema.

Actualmente el backend dispone de los siguientes endpoints:

```text
GET /
GET /falls
POST /falls
```

Para la definición y validación de los datos de entrada se utiliza Pydantic mediante modelos tipados.

La documentación interactiva de la API se encuentra disponible a través de Swagger en:

```text
http://127.0.0.1:8000/docs
```

Se ha implementado una base de datos SQLite local:

```text
falls.db
```

que almacena los eventos detectados por el sistema.

La tabla principal contiene:

```text
id
event_type
timestamp
confidence
source
```

Actualmente los eventos pueden almacenarse y recuperarse correctamente mediante la API.

---

## Próximos pasos

1. Diseñar la lógica de detección de caídas.
2. Integrar la detección con el backend mediante peticiones HTTP.
3. Implementar filtrado de eventos por fecha y tipo.
4. Desarrollar el frontend para consulta de eventos.
5. Evaluar sensibilidad y falsos positivos mediante vídeos de prueba.
6. Preparar la propuesta de despliegue local para tablet (extra).