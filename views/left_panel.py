from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                           QListWidget, QLineEdit, QWidget)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from .components import ModernFrame, ModernButton


class LeftPanel(ModernFrame):
    """پنل سمت چپ شامل کنترل‌ها و اطلاعات"""
    
    # سیگنال‌ها
    open_file_requested = pyqtSignal()
    search_changed = pyqtSignal(str)
    file_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.set_minimum_size(250, 0)
        self.set_maximum_size(300, 16777215)  # حداکثر ارتفاع Qt
        
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        """راه‌اندازی رابط کاربری پنل چپ"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # بخش هدر
        header_widget = self._create_header()
        layout.addWidget(header_widget)
        
        # خط جداکننده
        separator = self._create_separator()
        layout.addWidget(separator)
        
        # دکمه باز کردن فایل
        self.open_btn = ModernButton('باز کردن فایل ZIP')
        layout.addWidget(self.open_btn)
        
        # بخش جستجو
        search_widget = self._create_search_section()
        layout.addWidget(search_widget)
        
        # لیبل فایل‌ها
        files_label = QLabel('فایل‌ها')
        files_label.setProperty("class", "bold-label")
        files_label.setStyleSheet("margin-top: 5px;")
        layout.addWidget(files_label)
        
        # لیست فایل‌ها
        self.file_list = QListWidget()
        self.file_list.setAlternatingRowColors(True)
        layout.addWidget(self.file_list)
        
        # بخش اطلاعات
        info_frame = self._create_info_section()
        layout.addWidget(info_frame)
        
        # فضای خالی در انتها
        layout.addStretch(1)
        
    def _create_header(self) -> QWidget:
        """ایجاد بخش هدر"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        # عنوان اصلی
        title_label = QLabel('نمایش‌دهنده تصاویر')
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setProperty("class", "title-label")
        
        # زیرعنوان
        subtitle_label = QLabel('مشاهده و بررسی تصاویر از فایل زیپ')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setProperty("class", "subtitle-label")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        return header_widget
        
    def _create_separator(self) -> QFrame:
        """ایجاد خط جداکننده"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        return separator
        
    def _create_search_section(self) -> QWidget:
        """ایجاد بخش جستجو"""
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو بر اساس شماره...")
        self.search_input.setProperty("class", "search-input")
        
        search_layout.addWidget(self.search_input)
        
        return search_widget
        
    def _create_info_section(self) -> QFrame:
        """ایجاد بخش اطلاعات"""
        info_frame = QFrame()
        info_frame.setProperty("class", "info-frame")
        info_layout = QVBoxLayout(info_frame)
        
        info_label = QLabel('راهنما:')
        info_label.setProperty("class", "bold-label")
        
        self.info_text = QLabel('فایل ZIP حاوی تصاویر را باز کنید تا گروه‌های تصاویر نمایش داده شوند.')
        self.info_text.setWordWrap(True)
        
        info_layout.addWidget(info_label)
        info_layout.addWidget(self.info_text)
        
        return info_frame
        
    def _connect_signals(self):
        """اتصال سیگنال‌ها"""
        self.open_btn.clicked.connect(self.open_file_requested.emit)
        self.search_input.textChanged.connect(self.search_changed.emit)
        self.file_list.itemClicked.connect(
            lambda item: self.file_selected.emit(item.text())
        )
        
    def add_file_to_list(self, filename: str):
        """اضافه کردن فایل به لیست"""
        self.file_list.clear()
        self.file_list.addItem(filename)
        
    def update_info_text(self, text: str):
        """به‌روزرسانی متن اطلاعات"""
        self.info_text.setText(text)
        
    def set_loading_state(self, loading: bool):
        """تنظیم حالت بارگذاری"""
        self.open_btn.set_loading(loading)
        self.search_input.setEnabled(not loading)
        
    def clear_search(self):
        """پاک کردن جستجو"""
        self.search_input.clear()
        
    def set_search_text(self, text: str):
        """تنظیم متن جستجو"""
        self.search_input.setText(text)
        
    def get_search_text(self) -> str:
        """دریافت متن جستجو"""
        return self.search_input.text().strip()
        
    def show_statistics(self, stats: dict):
        """نمایش آمار تصاویر"""
        stats_text = f"""
        آمار تصاویر:
        • کل گروه‌ها: {stats.get('total_groups', 0)}
        • تصاویر اصلی: {stats.get('main_images', 0)}
        • تصاویر برش‌خورده: {stats.get('crop_images', 0)}
        • مجموع تصاویر: {stats.get('total_images', 0)}
        """
        self.update_info_text(stats_text.strip())
        
    def reset(self):
        """بازنشانی پنل"""
        self.file_list.clear()
        self.clear_search()
        self.update_info_text('فایل ZIP حاوی تصاویر را باز کنید تا گروه‌های تصاویر نمایش داده شوند.')
        self.set_loading_state(False)