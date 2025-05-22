from PyQt5.QtWidgets import QToolButton
from PyQt5.QtCore import QSize, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QFont


class NavigationButton(QToolButton):
    """دکمه ناوبری مدرن با انیمیشن"""
    
    # سیگنال‌های اضافی
    hover_entered = pyqtSignal()
    hover_left = pyqtSignal()
    
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setText(text)
        
        self.setProperty("class", "navigation-button")
        
        # تنظیمات پیش‌فرض
        self.setMinimumSize(40, 40)
        self.setMaximumSize(50, 50)
        
        # تنظیم فونت
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.setFont(font)
        
        # انیمیشن برای hover
        self._setup_animations()
        
    def _setup_animations(self):
        """راه‌اندازی انیمیشن‌ها"""
        # انیمیشن اندازه
        self.size_animation = QPropertyAnimation(self, b"minimumSize")
        self.size_animation.setDuration(150)
        self.size_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def set_arrow_left(self):
        """تنظیم به عنوان دکمه چپ"""
        self.setText("←")
        self.setToolTip("صفحه قبل")
        return self
        
    def set_arrow_right(self):
        """تنظیم به عنوان دکمه راست"""  
        self.setText("→")
        self.setToolTip("صفحه بعد")
        return self
        
    def set_arrow_up(self):
        """تنظیم به عنوان دکمه بالا"""
        self.setText("↑")
        self.setToolTip("بالا")
        return self
        
    def set_arrow_down(self):
        """تنظیم به عنوان دکمه پایین"""
        self.setText("↓")
        self.setToolTip("پایین")
        return self
        
    def set_custom_symbol(self, symbol: str, tooltip: str = ""):
        """تنظیم نماد سفارشی"""
        self.setText(symbol)
        if tooltip:
            self.setToolTip(tooltip)
        return self
        
    def set_circular(self, circular: bool = True):
        """تنظیم شکل دایره‌ای"""
        if circular:
            size = min(self.width(), self.height())
            self.setStyleSheet(f"""
                QToolButton {{
                    border-radius: {size//2}px;
                }}
            """)
        return self
        
    def enterEvent(self, event):
        """رویداد ورود ماوس"""
        super().enterEvent(event)
        self.hover_entered.emit()
        
        # انیمیشن بزرگ شدن
        self.size_animation.setStartValue(QSize(40, 40))
        self.size_animation.setEndValue(QSize(45, 45))
        self.size_animation.start()
        
    def leaveEvent(self, event):
        """رویداد خروج ماوس"""
        super().leaveEvent(event)
        self.hover_left.emit()
        
        # انیمیشن کوچک شدن
        self.size_animation.setStartValue(QSize(45, 45))
        self.size_animation.setEndValue(QSize(40, 40))
        self.size_animation.start()
        
    def set_enabled_with_animation(self, enabled: bool):
        """فعال/غیرفعال کردن با انیمیشن"""
        # انیمیشن محو شدن/ظاهر شدن
        opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        opacity_animation.setDuration(200)
        
        if enabled:
            opacity_animation.setStartValue(0.5)
            opacity_animation.setEndValue(1.0)
            self.setEnabled(True)
        else:
            opacity_animation.setStartValue(1.0)
            opacity_animation.setEndValue(0.5)
            opacity_animation.finished.connect(lambda: self.setEnabled(False))
            
        opacity_animation.start()
        
    def pulse_animation(self):
        """انیمیشن پالس برای جلب توجه"""
        pulse = QPropertyAnimation(self, b"minimumSize")
        pulse.setDuration(300)
        pulse.setEasingCurve(QEasingCurve.InOutQuad)
        pulse.setStartValue(QSize(40, 40))
        pulse.setEndValue(QSize(50, 50))
        
        # برگشت به اندازه اصلی
        def return_to_normal():
            return_pulse = QPropertyAnimation(self, b"minimumSize")
            return_pulse.setDuration(300)
            return_pulse.setEasingCurve(QEasingCurve.InOutQuad)
            return_pulse.setStartValue(QSize(50, 50))
            return_pulse.setEndValue(QSize(40, 40))
            return_pulse.start()
            
        pulse.finished.connect(return_to_normal)
        pulse.start()