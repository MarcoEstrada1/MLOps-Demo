import kfp
from google.cloud import aiplatform
from pipeline import pipeline

# Configuración de Google Cloud
PROJECT_ID = "proyecto-facturable"
LOCATION = "us-central1"
PIPELINE_ROOT = "gs://proyecto-facturable/pipeline_root/marco_2"

# Nombre único del pipeline
PIPELINE_NAME = "clv_pipeline"

# Crear cliente de Vertex AI Pipelines
aiplatform.init(project=PROJECT_ID, location=LOCATION)

# Compilar pipeline
PIPELINE_PACKAGE_PATH = "bert_pipeline.json"
kfp.v2.compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path=PIPELINE_PACKAGE_PATH,
)

# Ejecutar pipeline en Vertex AI
job = aiplatform.PipelineJob(
    display_name=PIPELINE_NAME,
    template_path=PIPELINE_PACKAGE_PATH,
    pipeline_root=PIPELINE_ROOT,
    parameter_values={
        "project": PROJECT_ID,
        "location": LOCATION,
        "display_name": "bert-sentiment-model",
        "container_uri": f"gcr.io/{PROJECT_ID}/online-retail-clv/dnn-regressor:$SHORT_SHA",  # Especificamos el contenedor de entrenamiento
        "base_output_dir": PIPELINE_ROOT,
    },
)

job.run(sync=True)