from app import ma
from app.models import User, ConversionHistory, FileQueue
from marshmallow import fields, validates, ValidationError

class UserSchema(ma.SQLAlchemySchema):
    """用户数据序列化模式"""
    class Meta:
        model = User
        load_instance = True  # 反序列化时创建模型实例
    
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    created_at = ma.auto_field()
    # 不序列化密码字段，保证安全性
    
    # 添加转换历史关系
    conversion_history = ma.Nested('ConversionHistorySchema', many=True, exclude=('user',))
    
    @validates('username')
    def validate_username(self, value):
        """验证用户名长度"""
        if len(value) < 3 or len(value) > 64:
            raise ValidationError('用户名长度必须在3-64个字符之间')

class ConversionHistorySchema(ma.SQLAlchemySchema):
    """文件转换历史序列化模式"""
    class Meta:
        model = ConversionHistory
        load_instance = True
    
    id = ma.auto_field()
    txt_filename = ma.auto_field()
    pdf_filename = ma.auto_field()
    original_size = ma.auto_field()
    converted_size = ma.auto_field()
    status = ma.auto_field()
    error_message = ma.auto_field()
    conversion_time = ma.auto_field()
    completed_at = ma.auto_field()
    
    # 添加用户关系
    user = ma.Nested('UserSchema', only=('id', 'username'))
    
    # 添加自定义字段
    file_size_mb = fields.Method("get_file_size_mb")
    
    def get_file_size_mb(self, obj):
        """将文件大小转换为MB"""
        if obj.original_size:
            return round(obj.original_size / (1024 * 1024), 2)
        return 0

class FileQueueSchema(ma.SQLAlchemySchema):
    """文件队列序列化模式"""
    class Meta:
        model = FileQueue
        load_instance = True
    
    id = ma.auto_field()
    filename = ma.auto_field()
    status = ma.auto_field()
    priority = ma.auto_field()
    created_at = ma.auto_field()
    
    # 添加用户关系
    user = ma.Nested('UserSchema', only=('id', 'username'))
    
    @validates('filename')
    def validate_filename(self, value):
        """验证文件名是否为txt格式"""
        if not value.lower().endswith('.txt'):
            raise ValidationError('只支持txt格式的文件')

# 创建schema实例，用于处理单个对象和对象列表
user_schema = UserSchema()
users_schema = UserSchema(many=True)

conversion_history_schema = ConversionHistorySchema()
conversion_histories_schema = ConversionHistorySchema(many=True)

file_queue_schema = FileQueueSchema()
file_queues_schema = FileQueueSchema(many=True) 