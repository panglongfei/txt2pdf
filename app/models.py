from datetime import datetime
from app import db

class User(db.Model):
    """用户模型
    
    用于存储用户信息，支持用户注册登录功能
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 建立与转换历史的关系
    conversion_history = db.relationship('ConversionHistory', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'

class ConversionHistory(db.Model):
    """文件转换历史记录模型
    
    用于记录用户的文件转换操作历史
    """
    __tablename__ = 'conversion_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    txt_filename = db.Column(db.String(255), nullable=False)
    pdf_filename = db.Column(db.String(255), nullable=False)
    original_size = db.Column(db.Integer)  # 原始文件大小（字节）
    converted_size = db.Column(db.Integer)  # 转换后文件大小（字节）
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    error_message = db.Column(db.Text)  # 如果转换失败，存储错误信息
    conversion_time = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)  # 转换完成时间
    
    def __repr__(self):
        return f'<ConversionHistory {self.txt_filename} -> {self.pdf_filename}>'
    
    def to_dict(self):
        """将记录转换为字典格式，方便API返回"""
        return {
            'id': self.id,
            'txt_filename': self.txt_filename,
            'pdf_filename': self.pdf_filename,
            'original_size': self.original_size,
            'converted_size': self.converted_size,
            'status': self.status,
            'error_message': self.error_message,
            'conversion_time': self.conversion_time.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class FileQueue(db.Model):
    """文件转换队列模型
    
    用于管理待转换的文件队列
    """
    __tablename__ = 'file_queue'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='queued')  # queued, processing, completed, failed
    priority = db.Column(db.Integer, default=0)  # 优先级，数字越大优先级越高
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<FileQueue {self.filename}>' 