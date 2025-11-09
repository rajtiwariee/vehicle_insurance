import os
from src.core.config import settings
from dataclasses import dataclass
from datetime import datetime
from src.utils.main_utils import read_yaml_file
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


@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, settings.DATA_VALIDATION_DIR_NAME)
    validation_report_file_path: str = os.path.join(data_validation_dir, settings.DATA_VALIDATION_REPORT_FILE_NAME)
    
@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, settings.DATA_TRANSFORMATION_DIR_NAME)
    transformed_train_file_path: str = os.path.join(data_transformation_dir, settings.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                    settings.TRAIN_FILE_NAME.replace("csv", "npy"))
    transformed_test_file_path: str = os.path.join(data_transformation_dir, settings.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                   settings.TEST_FILE_NAME.replace("csv", "npy"))
    transformed_object_file_path: str = os.path.join(data_transformation_dir,
                                                     settings.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                     settings.PREPROCSSING_OBJECT_FILE_NAME)

@dataclass
class ModelTrainerConfig:
    #read yaml file
    model_config = read_yaml_file(file_path=settings.MODEL_TRAINER_MODEL_CONFIG_FILE_PATH)
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir,settings.MODEL_TRAINER_DIR_NAME)
    trained_model_file_path: str = os.path.join(model_trainer_dir, settings.MODEL_TRAINER_TRAINED_MODEL_DIR, settings.MODEL_FILE_NAME)
    expected_accuracy: float = model_config["model"]["trainer"]["expected_score"]
    model_config_file_path: str = settings.MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    _n_estimators = model_config["model"]["trainer"]["n_estimators"]
    _min_samples_split = model_config["model"]["trainer"]["min_samples_split"]
    _min_samples_leaf = model_config["model"]["trainer"]["min_samples_leaf"]
    _max_depth = model_config["model"]["trainer"]["max_depth"]
    _criterion = model_config["model"]["trainer"]["criterion"]
    _random_state = model_config["model"]["trainer"]["random_state"]
    
@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float = settings.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
    bucket_name: str = settings.MODEL_BUCKET_NAME
    s3_model_key_path: str = settings.MODEL_FILE_NAME

@dataclass
class ModelPusherConfig:
    bucket_name: str = settings.MODEL_BUCKET_NAME
    s3_model_key_path: str = settings.MODEL_FILE_NAME
    
@dataclass
class VehiclePredictorConfig:
    model_file_path: str = settings.MODEL_FILE_NAME
    model_bucket_name: str = settings.MODEL_BUCKET_NAME