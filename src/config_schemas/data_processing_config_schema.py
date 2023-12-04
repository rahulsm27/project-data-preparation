from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass

from src.config_schemas.data_processing import dataset_cleaners_schema, dataset_readers_schema
from src.config_schemas.infrastructure import gcp_schema
from src.config_schemas.dask_cluster import dask_cluster_schema

@dataclass
class DataProcessingConfig:
    version: str = MISSING
    data_local_save_dir: str = "./data/raw"
    dvc_remote_repo: str = "https://github.com/rahulsm27/project_dvc.git"
    dvc_data_folder: str = "data/raw"
    github_user_name: str = "rahulsm27"
    github_access_token_secret_id: str = "github"
    
    infrastructure: gcp_schema.GCPConfig = gcp_schema.GCPConfig()

    dataset_reader_manager: dataset_readers_schema.DatasetReaderManagerConfig = MISSING

    dataset_cleaner_manager: dataset_cleaners_schema.DatasetCleanerManagerConfig = MISSING

    dask_cluster: dask_cluster_schema.DaskClusterConfig = MISSING

    processed_data_save_dir: str = MISSING #"./data/processed"

def setup_config() -> None:
    gcp_schema.setup_config()
    dataset_readers_schema.setup_config()
    dataset_cleaners_schema.setup_config()
    dask_cluster_schema.setup_config()

    cs = ConfigStore.instance()
    cs.store(name="data_processing_config_schema",node=DataProcessingConfig)
