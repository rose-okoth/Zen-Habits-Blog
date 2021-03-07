import os

class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oem:m3stravaill3s@localhost/blog1'
    UPLOADED_PHOTOS_DEST ='app/static'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    # email configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oem:m3stravaill3s@localhost/blog1'

class TestConfig(Config):
    '''
    Testing configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oem:m3stravaill3s@localhost/blog1'

class DevConfig(Config):
    '''
    Development configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oem:m3stravaill3s@localhost/blog1'

    DEBUG = True
    ENV = 'development'
    
config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}

