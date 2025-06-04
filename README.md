# MLOps Demo

Este repositorio contiene prototipos sencillos para demostrar pipelines de entrenamiento y despliegue en Google Vertex AI.

## Estructura del repositorio

- **Casos de uso/Clv**: ejemplo de modelo de Customer Lifetime Value. Incluye un `Dockerfile`, `cloudbuild.yaml`, código del pipeline y scripts de entrenamiento.
- **Casos de uso/Fine-tuning**: ejemplo de ajuste fino de un modelo BERT. Contiene un `Dockerfile`, `cloudbuild.yaml`, notebooks y el código del pipeline.

Cada carpeta cuenta con sus propias dependencias en `requirements.txt` y scripts dentro de `trainer/`.

## Ejecución

1. Construye la imagen de entrenamiento usando Cloud Build:
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```
2. Ejecuta el pipeline desde `pipeline/pipeline_run.py` o compilando el pipeline y lanzándolo en Vertex AI.

Ajusta las rutas de almacenamiento y los parámetros de proyecto según tu entorno de Google Cloud.

