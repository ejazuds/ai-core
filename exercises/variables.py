RESOURCE_GROUP = "team001" # your resource group e.g. team-01
EMBEDDING_MODEL_NAME = "gpt-4o-mini" # default is "text-embedding-ada-002"
EMBEDDING_DEPLOYMENT_ID = "db4f37170f864370" # e.g. d6b74feab22bc49a
LLM_DEPLOYMENT_ID = "d5b6e66815ec86cc" # e.g. d091bc956f115eb2
EMBEDDING_TABLE = "EMBEDDINGS_CODEJAM_SYED"

# You could for example try chunk size 100
# EMBEDDING_TABLE_CHUNK_SIZE_100 = "EMBEDDINGS_CODEJAM_+<YOUR_NAME>"+"CHUNK_SIZE_100"

AICORE_ORCHESTRATION_DEPLOYMENT_URL = "https://api.ai.prod.ap-southeast-2.aws.ml.hana.ondemand.com/v2/inference/deployments/d5b6e66815ec86cc"
