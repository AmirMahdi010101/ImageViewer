from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from typing import Optional


class ImageCard(QFrame):
    """کارت نمایش تصویر با استایل مدرن"""
    
    def __init__(self, img_path: str, label_text: str, parent=None):
        super().__init__(parent)
        self.img_path = img_path
        self.label_text = label_text
        
        self.setObjectName("imageCard")
        self.setProperty("class", "image-card")
        
        self._setup_ui()
        self._load_image()
        
    def _setup_ui(self):
        """راه‌اندازی رابط کاربری کارت"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # فریم تصویر
        self.img_frame = QFrame()
        self.img_frame.setProperty("class", "image-frame")
        self.img_frame.setMinimumSize(150, 150)
        self.img_frame.setMaximumSize(200, 200)
        
        img_layout = QVBoxLayout(self.img_frame)
        img_layout.setContentsMargins(0, 0, 0, 0)
        
        # لیبل تصویر
        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setMinimumSize(150, 150)
        self.img_label.setMaximumSize(200, 200)
        self.img_label.setScaledContents(False)
        
        img_layout.addWidget(self.img_label)
        
        # برچسب نام فایل
        self.name_label = QLabel(self.label_text)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        
        name_font = QFont()
        name_font.setPointSize(9)
        self.name_label.setFont(name_font)
        
        # قرار دادن اجزا در لایه
        layout.addWidget(self.img_frame)
        layout.addWidget(self.name_label)
        
        # تنظیم اندازه
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setMinimumWidth(180)
        self.setMaximumWidth(220)
        
    def _load_image(self):
        """بارگذاری و نمایش تصویر"""
        if not self.img_path:
            self._show_placeholder()
            return
            
        try:
            pixmap = QPixmap(self.img_path)
            if pixmap.isNull():
                self._show_placeholder()
                return
                
            # تغییر اندازه تصویر با حفظ نسبت
            scaled_pixmap = pixmap.scaled(
                180, 180, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self.img_label.setPixmap(scaled_pixmap)
            
        except Exception:
            self._show_placeholder()
            
    def _show_placeholder(self):
        """نمایش placeholder در صورت عدم وجود تصویر"""
        self.img_label.setText("تصویر موجود نیست")
        self.img_label.setStyleSheet("color: #888; font-size: 12px;")
        
    def update_image(self, new_path: str, new_label: str = None):
        """به‌روزرسانی تصویر کارت"""
        self.img_path = new_path
        if new_label:
            self.label_text = new_label
            self.name_label.setText(new_label)
        self._load_image()
        
    def get_image_size(self) -> QSize:
        """دریافت اندازه تصویر اصلی"""
        if self.img_path:
            pixmap = QPixmap(self.img_path)
            return pixmap.size()
        return QSize(0, 0)
        
    def set_highlight(self, highlighted: bool):
        """برجسته کردن کارت"""
        if highlighted:
            self.setStyleSheet("""
                #imageCard {
                    border: 2px solid #4a86e8;
                    background-color: #f0f8ff;
                }
            """)
        else:
            self.setStyleSheet("")