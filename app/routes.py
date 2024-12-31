from flask import Blueprint, render_template, request, send_file, current_app
import os
from werkzeug.utils import secure_filename
from .pdf_converter import PDFConverter
import tempfile
import time

# 创建蓝图
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/convert', methods=['POST'])
def convert():
    if 'txtFile' not in request.files:
        return '没有选择文件', 400
    
    file = request.files['txtFile']
    if file.filename == '':
        return '没有选择文件', 400
        
    if not file.filename.lower().endswith('.txt'):
        return '请上传TXT文件', 400

    pdf_path = None
    try:
        # 读取文本内容
        txt_content = file.read().decode('utf-8')
        
        # 创建唯一的临时文件名
        timestamp = int(time.time() * 1000)
        temp_filename = f'converted_{timestamp}_{secure_filename(file.filename)}.pdf'
        pdf_path = os.path.join(tempfile.gettempdir(), temp_filename)
        
        # 转换为PDF
        converter = PDFConverter()
        converter.convert_txt_to_pdf(txt_content, pdf_path)
        
        # 发送文件
        response = send_file(
            pdf_path,
            as_attachment=True,
            download_name=secure_filename(file.filename.rsplit('.', 1)[0] + '.pdf'),
            mimetype='application/pdf'
        )
        
        # 设置回调以在响应发送后删除文件
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(pdf_path):
                    os.unlink(pdf_path)
            except:
                pass
                
        return response

    except Exception as e:
        # 如果发生错误，尝试删除临时文件
        try:
            if pdf_path and os.path.exists(pdf_path):
                os.unlink(pdf_path)
        except:
            pass
        return f'转换失败：{str(e)}', 500 