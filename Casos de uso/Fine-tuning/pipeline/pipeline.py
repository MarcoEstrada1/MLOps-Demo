from kfp.v2 import dsl
from google_cloud_pipeline_components import aiplatform as gcc_aip


@dsl.pipeline(name="bert-sentiment-classification", pipeline_root="gs://proyecto-facturable/pipeline_root/marco_2")
def pipeline(
    project: str,
    location: str,
    display_name: str,
    container_uri: str,
    base_output_dir: str,
    endpoint_name: str,
):
    # Entrenamiento
    train_op = gcc_aip.CustomContainerTrainingJobRunOp(
        project=project,
        location=location,
        display_name=display_name,
        container_uri=container_uri,
        base_output_dir=base_output_dir,
    )

    # Registro del modelo
    register_op = gcc_aip.ModelUploadOp(
        project=project,
        location=location,
        display_name=display_name,
        artifact_uri=train_op.outputs["output_artifact_uri"],
        serving_container_image_uri=container_uri,
    )

    # Despliegue del modelo
    deploy_op = gcc_aip.ModelDeployOp(
        model=register_op.outputs["model"],
        endpoint=endpoint_name,
        traffic_split={"0": 100},
    )