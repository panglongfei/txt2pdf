from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import Config

# 创建数据库实例
db = SQLAlchemy()
# 创建序列化实例
ma = Marshmallow()
# 创建迁移实例
migrate = Migrate()

def create_app(config_class=Config):
    """
    工厂函数：创建并配置Flask应用实例
    :param config_class: 配置类，默认使用Config
    :return: Flask应用实例
    """
    # 创建Flask应用实例
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    # 加载配置
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # 在应用上下文中导入和注册蓝图
        from app.routes import bp
        app.register_blueprint(bp)
    
    return app 