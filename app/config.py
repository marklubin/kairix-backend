import os
import boto3
from botocore.config import Config

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_DEFAULT_MODEL = os.getenv('OPENAI_DEFAULT_MODEL', 'text-davinci-003')
    OPENAI_DEFAULT_TEMPERATURE = float(os.getenv('OPENAI_DEFAULT_TEMPERATURE', 0.7))
    OPENAI_DEFAULT_MAX_TOKENS = int(os.getenv('OPENAI_DEFAULT_MAX_TOKENS', 150))    

class TestConfig(BaseConfig):
    """Testing configuration - uses SQLite in-memory."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class DevTestConfig(BaseConfig):
    """Development Testing configuration - uses local PostgreSQL test database."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/chatdb_test'

class DevelopmentConfig(BaseConfig):
    """Development configuration - uses local PostgreSQL."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/chatdb'

class ProductionConfig(BaseConfig):
    """Production configuration - uses AWS RDS with IAM authentication."""
    DEBUG = False
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # Configure AWS SDK
        boto3_config = Config(
            region_name=os.getenv('AWS_REGION', 'us-west-2')
        )
        
        # Get RDS client
        rds_client = boto3.client('rds', config=boto3_config)
        
        # Generate auth token
        auth_token = rds_client.generate_db_auth_token(
            DBHostname=os.getenv('RDS_HOST'),
            Port=5432,
            DBUsername=os.getenv('DB_USER'),
            Region=os.getenv('AWS_REGION', 'us-west-2')
        )
        
        return f"postgresql://{os.getenv('DB_USER')}:{auth_token}@{os.getenv('RDS_HOST')}:5432/{os.getenv('DB_NAME')}"

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'devtest': DevTestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Dynamically get the config class based on an environment variable."""
    config_name = os.getenv("FLASK_CONFIG", "default")  # Default to 'default' (development)
    return config.get(config_name, DevelopmentConfig)  # Fallback to DevelopmentConfig