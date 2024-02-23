class Config:
    # Define common configuration variables here
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_cases.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = '34kt0OC79E9_vAgP7NkeRgqhiChiVCVT0MpDlzM_JI0'
    JWT_TOKEN_LOCATION = ['headers', 'cookies']


class DevelopmentConfig(Config):
    # Define development-specific configuration variables here
    DEBUG = True


class ProductionConfig(Config):
    # Define production-specific configuration variables here
    DEBUG = False
