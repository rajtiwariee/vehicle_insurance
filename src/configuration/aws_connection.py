import boto3
import os
from src.core.config import settings
from src.utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

class S3Client:
    
    """
    AWS S3 Client
    """
    #creating shared s3 client
    s3_client = None
    s3_resource = None

    def __init__(self):
        
        if S3Client.s3_client is None or S3Client.s3_resource is None:
            __access_key_id = settings.AWS_ACCESS_KEY_ID or os.getenv('AWS_ACCESS_KEY_ID')
            __secret_access_key = settings.AWS_SECRET_ACCESS_KEY or os.getenv('AWS_SECRET_ACCESS_KEY')
            if not __access_key_id or not __secret_access_key:
                raise Exception("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are not configured.")
            
            s3_client = boto3.client('s3',
                                     aws_access_key_id=__access_key_id,
                                     aws_secret_access_key=__secret_access_key,
                                     region_name=settings.AWS_REGION_NAME)
            
            s3_resource = boto3.resource('s3',
                                         aws_access_key_id=__access_key_id,
                                         aws_secret_access_key=__secret_access_key,
                                         region_name=settings.AWS_REGION_NAME)
            
            S3Client.s3_client = s3_client
            S3Client.s3_resource = s3_resource
            
        self.s3_client = S3Client.s3_client
        self.s3_resource = S3Client.s3_resource
            
        