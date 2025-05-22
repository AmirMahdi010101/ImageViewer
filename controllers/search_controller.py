# controllers/search_controller.py
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QLineEdit


class SearchController(QObject):
    """کنترلر جستجو"""
    
    # سیگنال‌ها
    search_requested = pyqtSignal(str)  # search_query
    search_cleared = pyqtSignal()
    search_text_changed = pyqtSignal(str)  # current_text
    
    def __init__(self):
        super().__init__()
        
        # مرجع به ویجت جستجو
        self.search_widget = None
        
        # تایمر برای تاخیر در جستجو
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        
        # تنظیمات جستجو
        self.search_delay = 300  # میلی‌ثانیه تاخیر قبل از جستجو
        self.min_search_length = 1  # حداقل طول متن برای جستجو
        
        # متغیرهای جستجو
        self.current_query = ""
        self.last_search_query = ""
        self.is_search_active = False
    
    def set_search_widget(self, search_widget):
        """تنظیم ویجت جستجو"""
        self.search_widget = search_widget
        
        # اتصال سیگنال‌های ویجت
        if self.search_widget:
            self.search_widget.textChanged.connect(self.on_text_changed)
            self.search_widget.returnPressed.connect(self.on_enter_pressed)
            
            # تنظیم placeholder text
            self.search_widget.setPlaceholderText("جستجو بر اساس شماره تصویر...")
    
    def on_text_changed(self, text):
        """پردازش تغییر متن جستجو"""
        self.current_query = text.strip()
        self.search_text_changed.emit(self.current_query)
        
        # توقف تایمر قبلی
        self.search_timer.stop()
        
        if self.current_query:
            # بررسی حداقل طول متن
            if len(self.current_query) >= self.min_search_length:
                # شروع تایمر برای جستجو با تاخیر
                self.search_timer.start(self.search_delay)
            else:
                self.is_search_active = False
        else:
            # پاک کردن جستجو
            self.clear_search()
    
    def on_enter_pressed(self):
        """پردازش فشردن کلید Enter"""
        # جستجوی فوری بدون تاخیر
        self.search_timer.stop()
        self.perform_search()
    
    def perform_search(self):
        """انجام جستجو"""
        if not self.current_query:
            return
        
        # بررسی تغییر query
        if self.current_query != self.last_search_query:
            self.last_search_query = self.current_query
            self.is_search_active = True
            
            # ارسال سیگنال جستجو
            self.search_requested.emit(self.current_query)
    
    def clear_search(self):
        """پاک کردن جستجو"""
        if self.is_search_active or self.last_search_query:
            self.is_search_active = False
            self.last_search_query = ""
            self.search_cleared.emit()
        
        # پاک کردن متن ویجت
        if self.search_widget:
            self.search_widget.clear()
    
    def set_search_text(self, text):
        """تنظیم متن جستجو"""
        if self.search_widget:
            self.search_widget.setText(text)
    
    def get_search_text(self):
        """دریافت متن جستجو"""
        if self.search_widget:
            return self.search_widget.text().strip()
        return ""
    
    def set_search_delay(self, delay_ms):
        """تنظیم تاخیر جستجو (میلی‌ثانیه)"""
        if delay_ms >= 0:
            self.search_delay = delay_ms
    
    def set_min_search_length(self, min_length):
        """تنظیم حداقل طول متن برای جستجو"""
        if min_length >= 0:
            self.min_search_length = min_length
    
    def is_searching(self):
        """بررسی فعال بودن جستجو"""
        return self.is_search_active
    
    def get_last_query(self):
        """دریافت آخرین کوئری جستجو"""
        return self.last_search_query
    
    def focus_search_widget(self):
        """فوکوس روی ویجت جستجو"""
        if self.search_widget:
            self.search_widget.setFocus()
    
    def select_all_text(self):
        """انتخاب تمام متن در ویجت جستجو"""
        if self.search_widget:
            self.search_widget.selectAll()
        