import argparse
from kfp.v2 import compiler
from google.cloud import aiplatform
from pipeline.pipeline import pipeline
import datetime

PIPELINE_JSON_PATH = "pipeline/pipeline.json"

def compile_pipeline():
    """Compila el pipeline y guarda el archivo JSON."""
    print(f"Compilando el pipeline en: {PIPELINE_JSON_PATH}")
    compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path=PIPELINE_JSON_PATH,
    )

def run_pipeline(container_uri):
    """Envía el pipeline a Vertex AI."""
    print("Enviando el pipeline a Vertex AI...")
    aiplatform.init(project="proyecto-facturable", location="us-central1")

    job = aiplatform.PipelineJob(
        display_name="bert-sentiment-classification",
        template_path=PIPELINE_JSON_PATH,
        parameter_values={
            "project": "proyecto-facturable",
            "location": "us-central1",
            "display_name": "bert-sentiment-{}".format(TIMESTAMP),
            "container_uri":container_uri,
            "base_output_dir": "gs://proyecto-facturable/bert-sentiment-classifier-{}".format(TIMESTAMP),
            "endpoint_name": '3508613072489021440',
        },
    )

    job.submit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--compile-only", action="store_true", help="Compila el pipeline y genera el archivo JSON.")
    parser.add_argument("--run-only", action="store_true", help="Ejecuta el pipeline previamente compilado.")
    parser.add_argument("--container-uri", type=str, required="--run-only" in " ".join(parser.parse_args()), help="URI del contenedor.")
    args = parser.parse_args()
    
    if args.compile_only:
        compile_pipeline()
    elif args.run_only:
        if not args.container_uri:
            raise ValueError("Se requiere --container-uri para ejecutar el pipeline.")
        run_pipeline(container_uri=args.container_uri)
    else:
        compile_pipeline()
        run_pipeline(container_uri=args.container_uri)