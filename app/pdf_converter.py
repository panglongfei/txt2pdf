from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .text_formatter import TextFormatter
import os

class PDFConverter:
    def __init__(self):
        # 注册中文字体（使用微软雅黑或宋体）
        try:
            # Windows 系统默认字体路径
            windows_font_path = "C:/Windows/Fonts/msyh.ttf"  # 微软雅黑
            fallback_font_path = "C:/Windows/Fonts/simsun.ttc"  # 宋体
            
            if os.path.exists(windows_font_path):
                pdfmetrics.registerFont(TTFont('MicrosoftYaHei', windows_font_path))
                self.font_name = 'MicrosoftYaHei'
            elif os.path.exists(fallback_font_path):
                pdfmetrics.registerFont(TTFont('SimSun', fallback_font_path))
                self.font_name = 'SimSun'
            else:
                self.font_name = 'Helvetica'
        except:
            self.font_name = 'Helvetica'
            print("Warning: Using fallback font Helvetica")

        # 创建文本格式化器
        self.formatter = TextFormatter()

    def convert_txt_to_pdf(self, txt_content, output_path):
        """
        将文本内容转换为PDF文件
        :param txt_content: 文本内容
        :param output_path: 输出PDF文件路径
        :return: 生成的PDF文件路径
        """
        # 创建PDF文档
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4

        # 设置字体
        c.setFont(self.font_name, 12)  # 固定字体大小为12

        # 页面边距
        margin_left = 50
        margin_top = height - 50
        line_height = 12 * 1.5
        
        # 格式化文本
        formatted_text = self.formatter.format_text(txt_content)

        # 分行处理文本
        lines = formatted_text.split('\n')
        current_y = margin_top
        page_number = 1

        for line in lines:
            # 如果当前行超出页面底部，创建新页面
            if current_y < 50:
                # 添加页码
                self._add_page_number(c, page_number)
                c.showPage()
                page_number += 1
                current_y = margin_top
                c.setFont(self.font_name, 12)  # 重新设置字体

            try:
                # 绘制文本
                c.drawString(margin_left, current_y, line)
            except:
                print(f"Warning: Unable to process line: {line}")
            
            current_y -= line_height
            
            # 检查是否需要新页面
            if current_y < 50 and line:
                # 添加页码
                self._add_page_number(c, page_number)
                c.showPage()
                page_number += 1
                current_y = margin_top
                c.setFont(self.font_name, 12)  # 重新设置字体

        # 添加最后一页的页码
        self._add_page_number(c, page_number)

        # 保存PDF文件
        c.save()
        return output_path

    def _add_page_number(self, canvas, page_number):
        """
        添加页码
        :param canvas: PDF画布
        :param page_number: 页码
        """
        # 保存当前字体设置
        current_font = canvas._fontname
        current_size = canvas._fontsize

        # 设置页码字体和大小
        canvas.setFont(self.font_name, 10)
        
        # 在页面底部居中添加页码
        canvas.drawString(A4[0]/2 - 15, 30, f"- {page_number} -")

        # 恢复原来的字体设置
        canvas.setFont(current_font, current_size) 