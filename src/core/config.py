from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from datetime import date
import os

ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = Path(__file__).resolve().parents[2]
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_DIR / ".env", extra="ignore")

    database_hostname: str | None = None
    database_port: str | None = None
    database_password: str | None = None
    database_name: str = "Proj1"
    collection_name: str = "Proj1-Data"
    database_username: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_region_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("AWS_REGION_NAME", "AWS_REGION"),
    )
    aws_bucket_name: str | None = None
    database_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DATABASE_URL", "MONGODB_URL"),
    )
    
    PIPELINE_NAME: str = ""
    ARTIFACT_DIR: str = "artifact"

    MODEL_FILE_NAME: str = "model.pkl"

    TARGET_COLUMN: str = "Response"
    CURRENT_YEAR: int = date.today().year
    PREPROCSSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"

    FILE_NAME: str = "data.csv"
    TRAIN_FILE_NAME: str = "train.csv"
    TEST_FILE_NAME: str = "test.csv"
    SCHEMA_FILE_PATH:str = os.path.join("config", "schema.yaml")


    """
    Data Ingestion related constant start with DATA_INGESTION VAR NAME
    """
    DATA_INGESTION_COLLECTION_NAME: str = "Proj1-Data"
    DATA_INGESTION_DIR_NAME: str = "data_ingestion"
    DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
    DATA_INGESTION_INGESTED_DIR: str = "ingested"
    DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25
    DATA_INGESTION_TEST_DIR: str = "test"
    DATA_INGESTION_TRAIN_DIR: str = "train"
    DATA_INGESTION_TRAIN_FILE_PATH: str = os.path.join(DATA_INGESTION_INGESTED_DIR, "train.csv")
    DATA_INGESTION_TEST_FILE_PATH: str = os.path.join(DATA_INGESTION_INGESTED_DIR, "test.csv")



    """
    Data Validation realted contant start with DATA_VALIDATION VAR NAME
    """
    DATA_VALIDATION_DIR_NAME: str = "data_validation"
    DATA_VALIDATION_REPORT_FILE_NAME: str = "report.yaml"

    """
    Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
    """
    DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
    DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
    DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

    """
    MODEL TRAINER related constant start with MODEL_TRAINER var name
    """
    MODEL_TRAINER_DIR_NAME: str = "model_trainer"
    MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
    MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
    MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
    MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")
    MODEL_TRAINER_N_ESTIMATORS:int=200
    MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7
    MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6
    MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10
    MIN_SAMPLES_SPLIT_CRITERION: str = 'entropy'
    MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101

    """
    MODEL Evaluation related constants
    """
    MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
    MODEL_BUCKET_NAME:str = "my-model-mlopsproj"
    MODEL_PUSHER_S3_KEY:str = "model-registry"


    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 5000


settings = Settings()
