"""
Global Flask Application Setting

See `.flaskenv` for default settings.
 """

import os
import sys

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.parse
else:
    import urlparse

if os.path.exists('config.env'):
    print('Importing environment from .env file')
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


class Config(object):
    FLASK_ENV =  None
    SECRET_KEY = os.getenv('FLASK_SECRET', 'flask-secret')

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, 'dist')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')

    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin_password')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@cryptotax.com')

    ETHEREUM_PROVIDER = os.getenv('ETH_PROVIDER', 'http')
    ETHEREUM_ENDPOINT_URI = os.getenv('ETH_NET_ADDR', 'http://127.0.0.1:7545')
    
    ETH_CONTRACT_OWNER = os.getenv('ETH_CONTRACT_OWNER')
    ETH_CONTRACTS_DIR = os.getenv('ETH_CONTRACTS_DIR',
                                  os.path.join(ROOT_DIR, 'etc/contracts'))
    ETH_CONTRACTS = dict(
        payment=dict(name='Payment', filename='Payment.sol'),
    )

     if not ETH_CONTRACT_OWNER or ETH_CONTRACT_OWNER == '':
        raise Exception("""ETH_CONTRACT_OWNER not set in env;\n
        Solution 1: Create a "config.env" file in project's root and add a line like "ETH_CONTRACT_OWNER=0xA6115D445B2D3DD2EBF9e7daEC2A135b4F750d02" (replace addr, no quotes)\n
        Solution 2: "export ETH_CONTRACT_OWNER=...""")

    if not os.path.exists(DIST_DIR):
        raise Exception('DIST_DIR not found: {}'.format(DIST_DIR))

    if not os.path.exists(ETH_CONTRACTS_DIR):
        raise Exception('ETH_CONTRACTS_DIR not found: {}'.format(ETH_CONTRACTS_DIR))

    for contract in ETH_CONTRACTS:
        contract_path = os.path.join(ETH_CONTRACTS_DIR,
                                     ETH_CONTRACTS[contract]['filename'])
        if not os.path.exists(contract_path):
            raise Exception('Contract not found: {}'.format(contract_path))

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL',
                                        'sqlite:///' + os.path.join(Config.ROOT_DIR, 'data-dev.sqlite'))
    @classmethod
    def init_app(cls, app):
        app.logger.info('THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'sqlite:///' + os.path.join(Config.ROOT_DIR, 'data.sqlite'))
    SSL_DISABLE = os.getenv('SSL_DISABLE', 'True') == 'True'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'unix': UnixConfig,
}