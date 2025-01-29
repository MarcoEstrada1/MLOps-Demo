from kfp.v2 import dsl
from google_cloud_pipeline_components import aiplatform as gcc_aip


PIPELINE_ROOT = "gs://proyecto-facturable/pipeline_root/marco_2"

@dsl.pipeline(
    name="clv_pipeline",
    pipeline_root=PIPELINE_ROOT,
)

def pipeline(
    project: str,
    location: str,
    display_name: str,
    container_uri: str,
    base_output_dir: str,
    model_serving_container_image_uri: str,
    staging_bucket: str
):
    """Define un pipeline de entrenamiento, registro y despliegue en Vertex AI."""

    train_op = gcc_aip.CustomContainerTrainingJobRunOp(
        project=project,
        location=location,
        display_name=display_name,
        machine_type="e2-standard-4",
        container_uri=container_uri,
        base_output_dir=base_output_dir,
        model_serving_container_image_uri=model_serving_container_image_uri,
        staging_bucket=staging_bucket
    )

    
    endpoint_create_op = gcc_aip.EndpointCreateOp(
        # Vertex AI Python SDK authentication parameters.
        project=project,
        location=location,
        display_name=display_name
    )
    
    register_op = gcc_aip.ModelUploadOp(
        model=train_op.outputs["model"],
        endpoint=endpoint_create_op.outputs["endpoint"],
        traffic_split={"0": 100},
        dedicated_resources_machine_type="e2-standard-4",
        dedicated_resources_min_replica_count=1,
        dedicated_resources_max_replica_count=1
    )
