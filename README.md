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
├── backend/
│   ├── database.py
│   └── main.py
├── detector/
│   ├── models/
│   │   └── pose_landmarker_full.task
│   ├── tests/
│   ├── videos/
│   │   └── fall-*.mp4
│   ├── fall_detector.py
│   ├── test_all_videos.py
│   ├── pose_live.py
│   └── pose_videos.py
├── frontend/
│   └── index.html
├── requirements.txt
├── falls.db (generado automáticamente)
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
pip install -r requirements.txt
```

---

## Ejecución del prototipo

### 1. Crear la base de datos

Antes de arrancar el sistema es necesario crear la base de datos SQLite:

```bash
python backend/database.py
```

Esto generará el fichero:

```text
falls.db
```

y creará las tablas necesarias para almacenar los eventos detectados.

---

### 2. Iniciar el backend

Desde la raíz del proyecto:

```bash
uvicorn backend.main:app --reload
```

El backend quedará disponible en:

```text
http://127.0.0.1:8000
```

La documentación Swagger puede consultarse en:

```text
http://127.0.0.1:8000/docs
```

---

### 3. Iniciar el frontend

Abrir el archivo:

```text
frontend/index.html
```

desde el navegador.

El frontend consultará automáticamente los eventos almacenados en la base de datos a través del backend.

---

### 4. Ejecutar el detector de caídas

En una nueva terminal:

```bash
python detector/fall_detector.py
```

El detector procesará la entrada de vídeo y analizará la pose corporal mediante MediaPipe Pose.

Cuando se detecte una caída:

```text
FALL DETECTED
```

se generará automáticamente un evento que será enviado al backend y almacenado en SQLite.

---

### 5. Verificar los resultados

Los eventos detectados pueden verificarse:

#### Desde Swagger

```text
GET /falls
```

#### Desde el frontend

Accediendo a la tabla de eventos, donde se muestran:

- Tipo de evento
- Fecha y hora
- Nivel de confianza
- Fuente de detección

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
- [x] Frontend de consulta
- [x] Filtrado por fecha
- [x] Filtrado por tipo
- [x] Análisis de landmarks relevantes (nariz, hombros, caderas y tobillos)
- [x] Implementación de pruebas sobre vídeo mediante MediaPipe Pose
- [x] Evaluación de métricas Nariz-Caderas
- [x] Evaluación de métricas Hombros-Caderas
- [x] Comparativa de estrategias para detección de caídas
- [x] Detección de caídas mediante MediaPipe Pose
- [x] Integración detector → FastAPI
- [x] Almacenamiento automático de eventos detectados
- [x] Cálculo dinámico de confianza
- [x] Validación mediante vídeos del UR Fall Detection Dataset
- [x] Validación mediante cámara en tiempo real
- [x] Prevención de eventos duplicados

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

Posteriormente se analizaron los landmarks más relevantes (hombros, caderas, tobillos y nariz) para diseñar e implementar la lógica de detección de caídas.

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

### Experimentos de detección de caídas

Se ha realizado una fase experimental utilizando vídeos del dataset UR Fall Detection Dataset con el objetivo de identificar métricas capaces de discriminar correctamente una caída frente a otros estados corporales.

Para ello se desarrollaron distintas herramientas de visualización que permiten reproducir vídeos, mostrar el esqueleto generado por MediaPipe Pose y analizar la evolución de determinados landmarks a lo largo del tiempo.

Se evaluaron dos aproximaciones principales:

#### Estrategia 1: Nariz - Caderas

Se calculó la posición media de las caderas y se comparó con la posición de la nariz.

A partir de estos puntos se obtuvieron:

- Distancia vertical
- Distancia horizontal

Los experimentos mostraron que:

- La distancia vertical disminuye significativamente durante una caída.
- La distancia horizontal aumenta cuando la persona termina tumbada.
- Los resultados son satisfactorios en vistas frontales y laterales.

Sin embargo, cuando la persona cae de espaldas a la cámara la nariz deja de ser un landmark suficientemente estable, reduciendo la robustez de esta estrategia.

#### Estrategia 2: Hombros - Caderas

Posteriormente se sustituyó la nariz por el punto medio de ambos hombros.

Se calcularon igualmente:

- Distancia vertical entre hombros y caderas
- Distancia horizontal entre hombros y caderas

Los resultados obtenidos muestran un comportamiento más consistente para diferentes orientaciones corporales:

- Vista frontal
- Vista lateral
- Vista posterior

Por este motivo la aproximación basada en hombros y caderas se considera actualmente la candidata principal para la implementación final del detector de caídas.

---

### Patrones observados

Durante las pruebas realizadas se observaron los siguientes comportamientos:

Estado de pie:

SV = 0.15 - 0.35

SH = 0.00 - 0.03

Estado sentado:

SV = 0.20 - 0.25

SH = 0.01 - 0.05

Durante una caída:

SV disminuye progresivamente

SH aumenta progresivamente

Estado tumbado:

SV = 0.00 - 0.05

SH = 0.10 - 0.16

---

### Estrategia seleccionada

Tras el análisis experimental de diferentes métricas se seleccionó la estrategia basada en los puntos medios de hombros y caderas.

La caída se considera detectada cuando se cumplen estas condiciones durante **5 frames consecutivos**:

```text
SV < 0.05
SH > 0.10
```

Donde:

- **SV** es la distancia vertical entre los puntos medios de los hombros y las caderas.
- **SH** es la distancia horizontal entre los puntos medios de los hombros y las caderas.

Esta aproximación mostró mejores resultados que la estrategia basada en nariz-caderas. Permitió detectar correctamente múltiples caídas tanto en los vídeos del dataset como en pruebas en tiempo real mediante cámara.

Para reducir eventos duplicados, el detector incorpora un mecanismo de recuperación: la persona debe volver a una postura estable antes de que se permita registrar una nueva caída.

---

### Detección e integración de eventos

Cuando se detecta una caída, el detector genera automáticamente un evento y lo envía al backend mediante una petición HTTP.

Ejemplo de evento generado:

```json
{
  "event_type": "fall",
  "confidence": 0.94,
  "source": "mediapipe"
}
```

La confianza se calcula dinámicamente a partir de los valores observados para las distancias vertical y horizontal utilizadas por la regla de detección.

Los eventos se envían automáticamente al endpoint:

```text
POST /falls
```

Luego quedan almacenados en SQLite para su posterior consulta desde la interfaz web.

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

### Frontend de consulta

Se ha desarrollado una interfaz web ligera basada en HTML, CSS y JavaScript para consultar los eventos almacenados por el sistema.

El frontend consume la API REST desarrollada con FastAPI mediante peticiones HTTP y muestra los resultados en formato tabular.

Actualmente permite:

```text
- Consultar eventos almacenados
- Filtrar por tipo de evento
- Filtrar por fecha
- Visualizar el nivel de confianza
- Consultar el número de eventos encontrados
```

La interfaz se comunica directamente con los endpoints:

```text
GET /falls
```

para recuperar los eventos registrados en la base de datos SQLite.

Se ha habilitado soporte CORS en FastAPI para permitir la comunicación entre el frontend y el backend durante el desarrollo local.

---

### Resultados obtenidos

Se realizaron pruebas utilizando vídeos del **UR Fall Detection Dataset** y pruebas en tiempo real mediante cámara.

Resultados observados:

- Detección correcta de caídas frontales.
- Detección correcta de caídas laterales.
- Registro automático de eventos en SQLite.
- Visualización correcta de eventos en el frontend.
- Detección y registro de múltiples caídas consecutivas cuando la persona recupera previamente una postura estable.

---

### Validación realizada

El sistema fue validado utilizando dos enfoques complementarios:

#### Vídeos de prueba

Se utilizaron vídeos procedentes del UR Fall Detection Dataset para analizar distintos tipos de caída y evaluar el comportamiento de las métricas implementadas.

Las pruebas permitieron ajustar los umbrales de detección y comparar diferentes estrategias basadas en landmarks corporales.

#### Pruebas en tiempo real

Además de los vídeos del dataset, se realizaron pruebas reales utilizando una cámara conectada al sistema.

Durante estas pruebas se verificó:

- Detección automática de caídas.
- Registro de eventos en SQLite.
- Envío automático de eventos al backend.
- Visualización de eventos en el frontend.
- Registro independiente de múltiples caídas consecutivas tras la recuperación de la persona.

---

### Limitaciones identificadas

Durante las pruebas realizadas se identificaron algunas limitaciones de la heurística implementada:

- Las caídas de espaldas pueden no producir suficiente desplazamiento horizontal entre hombros y caderas.
- Las caídas en las que la persona termina en una postura encogida o semisentada pueden presentar valores similares a una postura sentada, dificultando su detección mediante la métrica hombros-caderas.
- Algunas caídas muy rápidas pueden no cumplir la condición durante suficientes frames consecutivos.
- Los umbrales utilizados fueron obtenidos experimentalmente a partir de un conjunto reducido de vídeos.
- El sistema trabaja con una única cámara RGB y no dispone de información de profundidad real.

Estas limitaciones sugieren que futuras versiones deberían incorporar características adicionales además de la geometría hombros-caderas.

---

## Próximos pasos

- Mejorar la detección de caídas de espaldas.
- Incorporar nuevas métricas basadas en velocidad y aceleración de landmarks.
- Evaluar el sistema sobre un conjunto de datos más amplio.
- Reducir falsos negativos en caídas rápidas.
- Preparar una propuesta de despliegue sobre tablet Android.