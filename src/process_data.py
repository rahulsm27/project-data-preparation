from hydra.utils import instantiate
from dask.distributed import Client
import dask.dataframe as dd
from src.config_schemas.data_processing_config_schema import DataProcessingConfig
from src.config_schemas.data_processing.dataset_cleaners_schema import DatasetCleanerManagerConfig

from src.utils.data_utils import filter_based_on_minimum_number_of_words
from src.utils.config_utils import get_config,custom_instantiate
from src.utils.data_utils import get_raw_data_with_version
from src.utils.gcp_utils import access_secret_version
from src.utils.config_utils import get_pickle_config
from src.utils.utils import get_logger
from pathlib import Path
from src.utils.io_utils import write_yaml_file

import os

def process_raw_data(df_partition : dd.core.DataFrame, dataset_cleaner_manager : DatasetCleanerManagerConfig) -> dd.core.Series:
    processed_partition: dd.core.Series = df_partition["text"].apply(dataset_cleaner_manager)
    return processed_partition

# custom decorator created
@get_pickle_config(config_path="src/configs/automatically_generated", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None:
    # print(config)
    # from omegaconf import OmegaConf
    # print(OmegaConf.to_yaml(config))

 
    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data...")

    processed_data_save_dir = config.processed_data_save_dir
    
    cluster = custom_instantiate(config.dask_cluster)
    client = Client(cluster)
    try :
        # github_access_token = access_secret_version(config.infrastructure.project_id,config.github_access_token_secret_id)
        
        # process_data_save_dir = config.processed_data_save_dir

        # get_raw_data_with_version(version=config.version,
        #                       data_local_save_dir=config.data_local_save_dir,
        #                       dvc_remote_repo=config.dvc_remote_repo,
        #                       dvc_data_folder=config.dvc_data_folder,
        #                       github_user_name=config.github_user_name,
        #                       github_access_token=github_access_token)

        dataset_reader_manager = instantiate(config.dataset_reader_manager)
        dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)
        df = dataset_reader_manager.read_data(config.dask_cluster.n_workers)
        
        # print(df.compute().head())
        # exit()
        logger.info("Cleaning data...")


        df  = df.assign(cleaned_text=df.map_partitions(process_raw_data, dataset_cleaner_manager=dataset_cleaner_manager,meta=('text','object')))
        df = df.compute()

        train_parquet_path = os.path.join(processed_data_save_dir,"train.parquet")

        test_parquet_path = os.path.join(processed_data_save_dir,"test.parquet")
        
        dev_parquet_path = os.path.join(processed_data_save_dir,"dev.parquet")


        train_df = df[df["split"] == "train"]
        dev_df = df[df["split"] == "dev"]
        test_df = df[df["split"] == "test"]

        train_df = filter_based_on_minimum_number_of_words(train_df, min_nrof_words=config.min_nrof_words)
        dev_df = filter_based_on_minimum_number_of_words(dev_df, min_nrof_words=config.min_nrof_words)
        test_df = filter_based_on_minimum_number_of_words(test_df, min_nrof_words=config.min_nrof_words)

        train_df.to_parquet(train_parquet_path)
        dev_df.to_parquet(dev_parquet_path)
        test_df.to_parquet(test_parquet_path)
        

        #sample_df = df.sample(n=5)


        # for _, row in sample_df.iterrows():
        #     text = row["text"]
        #     cleaned_text = dataset_cleaner_manager(text)

        # print(df.head())

        docker_info = {"docker_image": config.docker_image_name, "docker_tag": config.docker_image_tag}
        docker_info_save_path = os.path.join(processed_data_save_dir, "docker_info.yaml")

        write_yaml_file(docker_info_save_path, docker_info)

        logger.info("Data processing finished!")
    finally:

        logger.info("Clossing cluster")
        client.close()
        cluster.close()


if __name__ == "__main__":
    process_data() 
