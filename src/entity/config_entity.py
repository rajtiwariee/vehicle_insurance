import os
from src.core.config import settings
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = settings.PIPELINE_NAME
    artifact_dir: str = os.path.join(settings.ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, settings.DATA_INGESTION_DIR_NAME)
    feature_store_file_path: str = os.path.join(data_ingestion_dir, settings.DATA_INGESTION_FEATURE_STORE_DIR, settings.FILE_NAME)
    training_file_path: str = os.path.join(data_ingestion_dir, settings.DATA_INGESTION_INGESTED_DIR, settings.TRAIN_FILE_NAME)
    testing_file_path: str = os.path.join(data_ingestion_dir, settings.DATA_INGESTION_INGESTED_DIR, settings.TEST_FILE_NAME)
    train_test_split_ratio: float = settings.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name:str = settings.DATA_INGESTION_COLLECTION_NAME
