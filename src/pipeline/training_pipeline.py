import sys
from src.utils.exception import MyException
from src.utils.logger import get_logger
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher
from src.entity.config_entity import (DataIngestionConfig,
                                          DataValidationConfig,
                                          DataTransformationConfig,
                                          ModelTrainerConfig,
                                          ModelEvaluationConfig,
                                          ModelPusherConfig)
                                          
from src.entity.artifact_entity import (DataIngestionArtifact,
                                            DataValidationArtifact,
                                            DataTransformationArtifact,
                                            ModelTrainerArtifact,
                                            ModelEvaluationArtifact,
                                            ModelPusherArtifact)


logger = get_logger(__name__)
class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()


    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            logger.info("Entered the start_data_ingestion method of TrainPipeline class")
            logger.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logger.info("Got the train_set and test_set from mongodb")
            logger.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """_summary_

        Args:
            data_ingestion_artifact (DataIngestionArtifact): _description_

        Returns:
            DataValidationArtifact: _description_
        """
        try:
            logger.info("Entered the start_data_validation method of TrainPipeline class")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                              data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logger.info("Performed the data validation operation")
            logger.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e, sys) from e
        
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logger.info("Entered the start_data_transformation method of TrainPipeline class")

            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                       data_validation_artifact=data_validation_artifact,
                                                       data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logger.info("Exited the start_data_transformation method of TrainPipeline class")
            return data_transformation_artifact
        except Exception as e:
            raise MyException(e, sys)
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            logger.info("Entered the start_model_trainer method of TrainPipeline class")
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config,
                                         data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logger.info("Exited the start_model_trainer method of TrainPipeline class")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e, sys)
        

    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               model_trainer_artifact: ModelTrainerArtifact):
        try:
            logger.info("Entered the start_model_evaluation method of TrainPipeline class")
            
            model_eval = ModelEvaluation(model_eval_config=self.model_evaluation_config,
                                          data_ingestion_artifact=data_ingestion_artifact,
                                          model_trainer_artifact=model_trainer_artifact)
            model_eval_artifact = model_eval.initiate_model_evaluation()
            logger.info("Exited the start_model_evaluation method of TrainPipeline class")
            return model_eval_artifact
        except Exception as e:
            raise MyException(e, sys)
        
        
    def start_model_pusher(self, model_eval_artifact: ModelEvaluationArtifact):
        try:
            logger.info("Entered the start_model_pusher method of TrainPipeline class")
            model_pusher = ModelPusher(
                                       model_evaluation_artifact=model_eval_artifact,
                                       model_pusher_config=self.model_pusher_config)
            model_pusher_artifact = model_pusher.initiate_model_pusher()

            return model_pusher_artifact
        except Exception as e:
            raise MyException(e, sys)
        
    def run_pipeline(self, ) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            logger.info("Entered the run_pipeline method of TrainPipeline class")
            
            data_ingestion_artifact = self.start_data_ingestion()
            logger.info(f'Data ingestion {data_ingestion_artifact}')
            logger.info(f'Starting data validation')
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            logger.info(f'Data validation {data_validation_artifact}')   
            
            logger.info(f'Starting data transformation')
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
            data_validation_artifact=data_validation_artifact)
            logger.info(f'Data transformation {data_transformation_artifact}')   
            
            logger.info(f'Starting model trainer')
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            logger.info(f'Model trainer {model_trainer_artifact}')   
            
            logger.info('Starting model evaluation')
            model_eval_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                             model_trainer_artifact=model_trainer_artifact)
            logger.info(f'Model evaluation {model_eval_artifact}')
            
            if model_eval_artifact.is_model_accepted:
                logger.info('Starting model pusher')
                model_pusher_artifact = self.start_model_pusher(model_eval_artifact=model_eval_artifact)
                logger.info(f'Model pusher {model_pusher_artifact}')
            else:
                logger.info("Model underperforms existing baseline; skipping push.")
                raise Exception('Model not accepted')      
            
        except Exception as e:
            raise MyException(e, sys)