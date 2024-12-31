import os

class Config:
    # 设置密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    
    # 配置SQLAlchemy数据库URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db'
    
    # 关闭SQLAlchemy的事件系统
    SQLALCHEMY_TRACK_MODIFICATIONS = False 