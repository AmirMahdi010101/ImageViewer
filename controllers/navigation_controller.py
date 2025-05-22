# controllers/navigation_controller.py
from PyQt5.QtCore import QObject, pyqtSignal, QPropertyAnimation, QTimer, QEasingCurve
from PyQt5.QtWidgets import QGraphicsOpacityEffect


class NavigationController(QObject):
    """کنترلر ناوبری و انیمیشن‌ها"""
    
    # سیگنال‌ها
    animation_started = pyqtSignal()
    animation_finished = pyqtSignal()
    fade_out_finished = pyqtSignal()
    fade_in_finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # تنظیمات انیمیشن
        self.fade_out_duration = 150  # مدت زمان محو شدن (میلی‌ثانیه)
        self.fade_in_duration = 200   # مدت زمان ظاهر شدن (میلی‌ثانیه)
        
        # متغیرهای انیمیشن
        self.current_animation = None
        self.is_animating = False
    
    def animate_page_change(self, widget, callback):
        """انیمیشن تغییر صفحه با محو و ظاهر شدن"""
        if self.is_animating:
            return  # جلوگیری از اجرای همزمان چند انیمیشن
        
        self.is_animating = True
        self.animation_started.emit()
        
        # ذخیره callback برای اجرای بعدی
        self._page_change_callback = callback
        self._target_widget = widget
        
        # شروع انیمیشن محو شدن
        self._start_fade_out_animation(widget)
    
    def _start_fade_out_animation(self, widget):
        """شروع انیمیشن محو شدن"""
        self.current_animation = QPropertyAnimation(widget, b"opacity")
        self.current_animation.setDuration(self.fade_out_duration)
        self.current_animation.setStartValue(1.0)
        self.current_animation.setEndValue(0.5)
        self.current_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # اتصال سیگنال اتمام انیمیشن
        self.current_animation.finished.connect(self._on_fade_out_finished)
        
        # شروع انیمیشن
        self.current_animation.start()
    
    def _on_fade_out_finished(self):
        """پردازش اتمام انیمیشن محو شدن"""
        self.fade_out_finished.emit()
        
        # اجرای callback تغییر محتوا
        if hasattr(self, '_page_change_callback') and self._page_change_callback:
            self._page_change_callback()
        
        # شروع انیمیشن ظاهر شدن پس از تاخیر کوتاه
        QTimer.singleShot(50, self._start_fade_in_animation)
    
    def _start_fade_in_animation(self):
        """شروع انیمیشن ظاهر شدن"""
        if hasattr(self, '_target_widget') and self._target_widget:
            self.current_animation = QPropertyAnimation(self._target_widget, b"opacity")
            self.current_animation.setDuration(self.fade_in_duration)
            self.current_animation.setStartValue(0.5)
            self.current_animation.setEndValue(1.0)
            self.current_animation.setEasingCurve(QEasingCurve.InQuad)
            
            # اتصال سیگنال اتمام انیمیشن
            self.current_animation.finished.connect(self._on_fade_in_finished)
            
            # شروع انیمیشن
            self.current_animation.start()
    
    def _on_fade_in_finished(self):
        """پردازش اتمام انیمیشن ظاهر شدن"""
        self.fade_in_finished.emit()
        self.animation_finished.emit()
        
        # پاکسازی متغیرها
        self.is_animating = False
        self.current_animation = None
        self._page_change_callback = None
        self._target_widget = None
    
    def stop_animation(self):
        """توقف انیمیشن در حال اجرا"""
        if self.current_animation and self.is_animating:
            self.current_animation.stop()
            self.is_animating = False
            self.current_animation = None
    
    def set_animation_speed(self, speed_factor):
        """تنظیم سرعت انیمیشن (1.0 = عادی، 2.0 = دو برابر سریع‌تر)"""
        if speed_factor > 0:
            self.fade_out_duration = int(150 / speed_factor)
            self.fade_in_duration = int(200 / speed_factor)
    
    def is_animation_running(self):
        """بررسی اجرای انیمیشن"""
        return self.is_animating
    
    def create_simple_fade_animation(self, widget, start_opacity, end_opacity, duration=300):
        """ایجاد انیمیشن ساده محو شدن/ظاهر شدن"""
        animation = QPropertyAnimation(widget, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        return animation