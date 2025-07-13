import uuid

from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
                                  Environment,
                                  ManagedOnlineDeployment,
                                  ManagedOnlineEndpoint,
)
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id="d2c9842b-923a-49d9-948e-50d8fd30d4ac",
    resource_group_name="PA2025",
    workspace_name="PAML",
)

model = ml_client.models.get(name="cv_ner_train", version="20")

print(f"✅ Model retrieved: {model.name}:{model.version}")

env = Environment(
    name="spacy-inference-env",
    description="Environment for Spacy NER inference",
    conda_file="env.yml",
    image="mcr.microsoft.com/azureml/minimal-ubuntu20.04-py310-cpu-inference:latest",
)
print(f"✅ Environment created: {env.name}")

ml_client.environments.create_or_update(env)

print("Creating endpoint...")
endpoint_name = f"cv-ner-endpoint-{uuid.uuid4().hex[:6]}"
endpoint = ManagedOnlineEndpoint(
    name=endpoint_name,
    description="Endpoint for SpaCy NER CV model",
    auth_mode="key",
)
ml_client.online_endpoints.begin_create_or_update(endpoint).result()
print(f"✅ Endpoint created: {endpoint.name}")

print("Creating deployment...")
deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name=endpoint_name,
    model=model,
    environment=env,
    code_path=".",
    instance_type="Standard_DS2_v2",
    instance_count=1,
)
print(f"✅ Deployment created: {deployment.name}")
ml_client.online_deployments.begin_create_or_update(deployment).result()

ml_client.online_endpoints.begin_update(
    endponit_name=endpoint.name,
    traffic={"blue": 100},
).result()

print(f"✅ Endpoint created: {endpoint.name}")