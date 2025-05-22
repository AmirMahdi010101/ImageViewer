# controllers/application_controller.py
from PyQt5.QtCore import QObject, pyqtSignal
from controllers.main_controller import MainController
from controllers.navigation_controller import NavigationController
from controllers.file_controller import FileController
from controllers.search_controller import SearchController


class ApplicationController(QObject):
    """کنترلر اصلی برنامه که سایر کنترلرها را مدیریت می‌کند"""
    
    # سیگنال‌های اصلی برای ارتباط با View
    status_updated = pyqtSignal(str)
    images_loaded = pyqtSignal()
    page_updated = pyqtSignal(int, int)  # current_page, total_pages
    navigation_updated = pyqtSignal(bool, bool)  # prev_enabled, next_enabled
    file_list_updated = pyqtSignal(str)  # file_name
    
    def __init__(self):
        super().__init__()
        
        # ایجاد کنترلرهای فرعی
        self.main_controller = MainController()
        self.navigation_controller = NavigationController()
        self.file_controller = FileController()
        self.search_controller = SearchController()
        
        # اتصال سیگنال‌ها
        self._connect_signals()
    
    def _connect_signals(self):
        """اتصال سیگنال‌های کنترلرهای مختلف"""
        
        # سیگنال‌های MainController
        self.main_controller.status_changed.connect(self.status_updated.emit)
        self.main_controller.file_loaded.connect(self.on_file_loaded)
        self.main_controller.images_updated.connect(self.on_images_updated)
        self.main_controller.page_changed.connect(self.on_page_changed)
        
        # سیگنال‌های FileController
        self.file_controller.file_selected.connect(self.on_file_selected)
        
        # سیگنال‌های SearchController
        self.search_controller.search_requested.connect(self.on_search_requested)
        self.search_controller.search_cleared.connect(self.on_search_cleared)
        
        # سیگنال‌های NavigationController
        self.navigation_controller.animation_finished.connect(self.on_animation_finished)
    
    def initialize_widgets(self, view):
        """مقداردهی اولیه ویجت‌ها"""
        # تنظیم ویجت‌های کنترلرهای فرعی
        self.file_controller.set_file_list_widget(view.file_list)
        self.search_controller.set_search_widget(view.search_input)
    
    def open_zip_file(self, parent_widget=None):
        """باز کردن فایل ZIP"""
        self.main_controller.open_zip_file(parent_widget)
    
    def next_page(self, animation_widget=None):
        """رفتن به صفحه بعد"""
        if self.main_controller.next_page():
            if animation_widget:
                self.navigation_controller.animate_page_change(
                    animation_widget, 
                    lambda: self.images_loaded.emit()
                )
            else:
                self.images_loaded.emit()
    
    def prev_page(self, animation_widget=None):
        """رفتن به صفحه قبل"""
        if self.main_controller.prev_page():
            if animation_widget:
                self.navigation_controller.animate_page_change(
                    animation_widget, 
                    lambda: self.images_loaded.emit()
                )
            else:
                self.images_loaded.emit()
    
    def get_current_page_groups(self):
        """دریافت گروه‌های تصاویر صفحه فعلی"""
        return self.main_controller.get_current_page_groups()
    
    def on_file_loaded(self, file_name):
        """پردازش بارگذاری فایل"""
        self.file_controller.add_file(file_name)
        self.file_list_updated.emit(file_name)
    
    def on_images_updated(self):
        """پردازش به‌روزرسانی تصاویر"""
        self.images_loaded.emit()
        self._update_navigation_state()
    
    def on_page_changed(self, current_page, total_pages):
        """پردازش تغییر صفحه"""
        self.page_updated.emit(current_page, total_pages)
        self._update_navigation_state()
    
    def on_file_selected(self, file_name):
        """پردازش انتخاب فایل از لیست"""
        self.status_updated.emit(f'فایل انتخاب شده: {file_name}')
    
    def on_search_requested(self, query):
        """پردازش درخواست جستجو"""
        # اینجا می‌توان منطق جستجو را پیاده‌سازی کرد
        filtered_groups = self.main_controller.search_images(query)
        self.status_updated.emit(f'جستجو برای: {query}')
    
    def on_search_cleared(self):
        """پردازش پاک کردن جستجو"""
        self.status_updated.emit('جستجو پاک شد')
        self.images_loaded.emit()
    
    def on_animation_finished(self):
        """پردازش اتمام انیمیشن"""
        self._update_navigation_state()
    
    def _update_navigation_state(self):
        """به‌روزرسانی وضعیت دکمه‌های ناوبری"""
        can_go_prev = self.main_controller.current_page > 0
        can_go_next = self.main_controller.current_page < self.main_controller.total_pages() - 1
        self.navigation_updated.emit(can_go_prev, can_go_next)
    
    def cleanup(self):
        """پاکسازی منابع"""
        self.main_controller.cleanup()