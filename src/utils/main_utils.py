import os
from pathlib import Path
import yaml
import sys
from src.utils.exception import MyException
from src.utils.logger import get_logger
import pickle
logger = get_logger(__name__)



def read_yaml_file(file_path: str) -> dict:
    try:
        
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise MyException(e, sys)
    
def write_yaml(file_path: str, data: dict) -> None:
    try:
        with open(file_path, "w") as f:
            yaml.dump(data, f)
    except Exception as e:
        raise MyException(e, sys)
    
    
def load_object_file(file_path: str) -> object:
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        raise MyException(e, sys)