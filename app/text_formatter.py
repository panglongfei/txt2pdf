import re
from textwrap import wrap

class TextFormatter:
    def __init__(self, line_spacing=1, paragraph_spacing=1, indent_spaces=4, max_line_width=80):
        """
        初始化文本格式化器
        :param line_spacing: 行间距倍数
        :param paragraph_spacing: 段落间距倍数
        :param indent_spaces: 段落缩进空格数
        :param max_line_width: 每行最大字符数
        """
        self.line_spacing = line_spacing
        self.paragraph_spacing = paragraph_spacing
        self.indent_spaces = indent_spaces
        self.max_line_width = max_line_width
        self.font_size = 12  # 固定字体大小为12

    def format_text(self, text):
        """
        格式化文本
        :param text: 原始文本
        :return: 格式化后的文本
        """
        if not text:
            return ""

        # 1. 统一换行符
        text = text.replace('\r\n', '\n').replace('\r', '\n')

        # 2. 分割成段落
        paragraphs = text.split('\n')

        # 3. 处理每个段落
        formatted_paragraphs = []
        for paragraph in paragraphs:
            # 跳过空段落
            if not paragraph.strip():
                formatted_paragraphs.append('')
                continue

            # 清理段落
            cleaned_para = self._clean_paragraph(paragraph)
            
            # 添加缩进并进行自动换行
            formatted_para = self._wrap_paragraph(cleaned_para)
            
            formatted_paragraphs.append(formatted_para)

        # 4. 使用额外的换行符连接段落（创建段落间距）
        paragraph_separator = '\n' * self.paragraph_spacing
        formatted_text = paragraph_separator.join(formatted_paragraphs)

        return formatted_text

    def _clean_paragraph(self, paragraph):
        """
        清理段落文本
        :param paragraph: 原始段落文本
        :return: 清理后的段落文本
        """
        # 1. 删除首尾空白
        paragraph = paragraph.strip()

        # 2. 替换多个空格为单个空格
        paragraph = re.sub(r'\s+', ' ', paragraph)

        # 3. 处理标点符号
        # 在中文标点后添加空格
        paragraph = re.sub(r'([。！？：；，、])', r'\1 ', paragraph)
        # 删除多余的空格
        paragraph = re.sub(r'\s+', ' ', paragraph)

        # 4. 处理特殊标点
        # 处理引号
        paragraph = re.sub(r'([""''])', r' \1 ', paragraph)
        # 处理括号
        paragraph = re.sub(r'([（）\(\)\[\]【】])', r' \1 ', paragraph)

        return paragraph.strip()

    def _wrap_paragraph(self, paragraph):
        """
        对段落进行自动换行处理
        :param paragraph: 清理后的段落文本
        :return: 格式化后的段落文本
        """
        # 计算实际可用宽度（考虑缩进和固定宽度调整）
        effective_width = self.max_line_width - self.indent_spaces - 34  # 固定宽度调整值为15

        # 分割段落成行
        lines = []
        
        # 处理第一行（添加缩进）
        first_line = ' ' * self.indent_spaces + paragraph[:effective_width]
        lines.append(first_line)
        
        # 处理剩余文本
        remaining_text = paragraph[effective_width:]
        while remaining_text:
            # 查找合适的断句点
            break_point = self._find_break_point(remaining_text, effective_width)
            
            # 添加新行
            lines.append(' ' * self.indent_spaces + remaining_text[:break_point].strip())
            remaining_text = remaining_text[break_point:].strip()

        return '\n'.join(lines)

    def _find_break_point(self, text, width):
        """
        找到合适的断句点
        :param text: 要处理的文本
        :param width: 最大宽度
        :return: 断句位置
        """
        if len(text) <= width:
            return len(text)

        # 优先在标点符号处断句
        punctuation_marks = '。！？：；，、""''）】'
        for i in range(width, -1, -1):
            if i < len(text) and text[i] in punctuation_marks:
                return i + 1

        # 如果找不到标点符号，就在空格处断句
        for i in range(width, -1, -1):
            if i < len(text) and text[i].isspace():
                return i + 1

        # 如果都找不到合适的断句点，就强制断句
        return width

    def _count_display_width(self, text):
        """
        计算文本显示宽度（考虑中英文混排）
        :param text: 要计算的文本
        :return: 显示宽度
        """
        width = 0
        for char in text:
            if ord(char) > 127:  # 中文字符
                width += 2
            else:  # 英文字符
                width += 1
        return width 