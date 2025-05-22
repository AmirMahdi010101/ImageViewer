from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, pyqtSignal
from typing import Optional


class ModernButton(QPushButton):
    """دکمه با طراحی مدرن"""
    
    # سیگنال‌های اضافی
    long_pressed = pyqtSignal()  # فشار طولانی
    
    def __init__(self, text: str, icon_path: Optional[str] = None, parent=None):
        super().__init__(text, parent)
        
        self.setProperty("class", "modern-button")
        
        # تنظیم آیکون در صورت وجود
        if icon_path:
            self.set_icon(icon_path)
            
        # تنظیم ویژگی‌های پیش‌فرض
        self.setMinimumHeight(35)
        
        # شمارنده برای فشار طولانی
        self._press_timer = None
        
    def set_icon(self, icon_path: str, size: int = 18):
        """تنظیم آیکون دکمه"""
        if icon_path:
            icon = QIcon(icon_path)
            self.setIcon(icon)
            self.setIconSize(QSize(size, size))
        return self
        
    def set_primary_style(self):
        """تنظیم استایل اصلی (آبی)"""
        self.setProperty("style", "primary")
        self.style().polish(self)
        return self
        
    def set_secondary_style(self):
        """تنظیم استایل ثانویه (خاکستری)"""
        self.setProperty("style", "secondary")
        self.setStyleSheet("""
            QPushButton[style="secondary"] {
                background-color: #6c757d;
                color: white;
            }
            QPushButton[style="secondary"]:hover {
                background-color: #5a6268;
            }
            QPushButton[style="secondary"]:pressed {
                background-color: #495057;
            }
        """)
        return self
        
    def set_success_style(self):
        """تنظیم استایل موفقیت (سبز)"""
        self.setProperty("style", "success")
        self.setStyleSheet("""
            QPushButton[style="success"] {
                background-color: #28a745;
                color: white;
            }
            QPushButton[style="success"]:hover {
                background-color: #218838;
            }
            QPushButton[style="success"]:pressed {
                background-color: #1e7e34;
            }
        """)
        return self
        
    def set_danger_style(self):
        """تنظیم استایل خطر (قرمز)"""
        self.setProperty("style", "danger")
        self.setStyleSheet("""
            QPushButton[style="danger"] {
                background-color: #dc3545;
                color: white;
            }
            QPushButton[style="danger"]:hover {
                background-color: #c82333;
            }
            QPushButton[style="danger"]:pressed {
                background-color: #bd2130;
            }
        """)
        return self
        
    def set_outline_style(self):
        """تنظیم استایل خطی"""
        self.setProperty("style", "outline")
        self.setStyleSheet("""
            QPushButton[style="outline"] {
                background-color: transparent;
                color: #4a86e8;
                border: 2px solid #4a86e8;
            }
            QPushButton[style="outline"]:hover {
                background-color: #4a86e8;
                color: white;
            }
            QPushButton[style="outline"]:pressed {
                background-color: #3a76d8;
            }
        """)
        return self
        
    def set_loading(self, loading: bool):
        """تنظیم حالت بارگذاری"""
        if loading:
            self.setEnabled(False)
            self.original_text = self.text()
            self.setText("در حال بارگذاری...")
        else:
            self.setEnabled(True)
            if hasattr(self, 'original_text'):
                self.setText(self.original_text)
                
    def mousePressEvent(self, event):
        """رویداد فشار ماوس - شروع تایمر فشار طولانی"""
        super().mousePressEvent(event)
        
        # شروع تایمر برای فشار طولانی (500ms)
        from PyQt5.QtCore import QTimer
        self._press_timer = QTimer()
        self._press_timer.timeout.connect(self._on_long_press)
        self._press_timer.setSingleShot(True)
        self._press_timer.start(500)
        
    def mouseReleaseEvent(self, event):
        """رویداد رهاکردن ماوس - توقف تایمر"""
        super().mouseReleaseEvent(event)
        
        if self._press_timer:
            self._press_timer.stop()
            self._press_timer = None
            
    def _on_long_press(self):
        """رویداد فشار طولانی"""
        self.long_pressed.emit()