from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass

from src.config_schemas.data_processing import dataset_cleaners_schema, dataset_readers_schema
from src.config_schemas.infrastructure import gcp_schema
from src.config_schemas.dask_cluster import dask_cluster_schema

@dataclass
class TokenizerTrainingConfig:

    
    infrastructure: gcp_schema.GCPConfig = gcp_schema.GCPConfig()

    data_parquet_path : str = MISSING
    text_column_name: str = MISSING


    docker_image_name : str = MISSING
    docker_image_tag : str = MISSING

    min_nrof_words : int = 2

def setup_config() -> None:
    gcp_schema.setup_config()
   
    cs = ConfigStore.instance()
    cs.store(name="tokenizer_training_config_schema",node=TokenizerTrainingConfig)
