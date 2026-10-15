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
- [ ] Integración MediaPipe Pose
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

## Próximos pasos

1. Obtener landmarks corporales con MediaPipe Pose.
2. Dibujar el esqueleto sobre la imagen.
3. Diseñar la lógica de detección de caídas.
4. Enviar eventos al backend mediante FastAPI.
5. Almacenar eventos en SQLite.
6. Desarrollar interfaz para consulta de eventos.
7. Evaluar sensibilidad y falsos positivos.