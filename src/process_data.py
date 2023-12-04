from hydra.utils import instantiate

from src.config_schemas.data_processing_config_schema import DataProcessingConfig
from src.utils.config_utils import get_config
from src.utils.data_utils import get_raw_data_with_version
from src.utils.gcp_utils import access_secret_version


# custom decorator created
@get_config(config_path="../configs", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None:
    # print(config)
    # from omegaconf import OmegaConf
    # print(OmegaConf.to_yaml(config))

    #   github_access_token = access_secret_version(config.infrastructure.project_id,config.github_access_token_secret_id)

    # get_raw_data_with_version(version=config.version,
    #                           data_local_save_dir=config.data_local_save_dir,
    #                           dvc_remote_repo=config.dvc_remote_repo,
    #                           dvc_data_folder=config.dvc_data_folder,
    #                           github_user_name=config.github_user_name,
    #                           github_access_token=github_access_token)

    dataset_reader_manager = instantiate(config.dataset_reader_manager)
    dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)

    df = dataset_reader_manager.read_data().compute()
    sample_df = df.sample(n=5)

    for _, row in sample_df.iterrows():
        text = row["text"]
        cleaned_text = dataset_cleaner_manager(text)

    print(df.head())


if __name__ == "__main__":
    process_data() 
