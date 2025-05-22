# controllers/main_controller.py
import os
import tempfile
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
from PyQt5.QtCore import QObject, pyqtSignal
from models.image_model import ImageModel
from models.zip_handler import ZipHandler


class MainController(QObject):
    """کنترلر اصلی برای مدیریت منطق برنامه"""
    
    # سیگنال‌ها برای ارتباط با View
    status_changed = pyqtSignal(str)
    progress_changed = pyqtSignal(int, int)  # current, total
    file_loaded = pyqtSignal(str)  # file name
    images_updated = pyqtSignal()
    page_changed = pyqtSignal(int, int)  # current_page, total_pages
    error_occurred = pyqtSignal(str)  # error message
    
    def __init__(self):
        super().__init__()
        
        # ایجاد مدل‌ها
        self.image_model = ImageModel()
        self.zip_handler = ZipHandler()
        
        # ایجاد پوشه موقت
        self.temp_dir = tempfile.mkdtemp()
        
        # تنظیمات صفحه‌بندی
        self.current_page = 0
        self.groups_per_frame = 2
        self.frames_per_page = 6
        self.groups_per_page = self.groups_per_frame * self.frames_per_page
        
        # متغیرهای کمکی
        self._current_file_name = ""
        
        # اتصال سیگنال‌های Model
        self._connect_model_signals()
    
    def _connect_model_signals(self):
        """اتصال سیگنال‌های مدل‌ها"""
        self.image_model.images_grouped.connect(self.on_images_grouped)
        self.zip_handler.extraction_progress.connect(self.progress_changed.emit)
        self.zip_handler.extraction_finished.connect(self.on_extraction_finished)
        self.zip_handler.extraction_error.connect(self.on_extraction_error)
    
    def open_zip_file(self, parent_widget=None):
        """باز کردن دیالوگ انتخاب فایل ZIP"""
        file_path, _ = QFileDialog.getOpenFileName(
            parent_widget, 
            'انتخاب فایل فشرده', 
            '', 
            'Zip files (*.zip)'
        )
        
        if file_path:
            self.load_zip_file(file_path)
    
    def load_zip_file(self, file_path):
        """بارگذاری فایل ZIP"""
        self.status_changed.emit('در حال بارگذاری فایل...')
        
        try:
            # ذخیره نام فایل
            self._current_file_name = os.path.basename(file_path)
            
            # پاک کردن فایل‌های قبلی
            self.clear_temp_files()
            
            # شروع استخراج فایل ZIP
            self.zip_handler.extract_images(file_path, self.temp_dir)
            
        except Exception as e:
            self.error_occurred.emit(f"خطا در بارگذاری فایل: {str(e)}")
    
    def on_extraction_finished(self, image_paths):
        """پردازش تصاویر استخراج شده"""
        if image_paths:
            self.status_changed.emit('در حال پردازش تصاویر...')
            self.image_model.group_images(image_paths)
            self.file_loaded.emit(self._current_file_name)
        else:
            self.error_occurred.emit("هیچ تصویری در فایل ZIP یافت نشد")
    
    def on_images_grouped(self):
        """پس از گروه‌بندی تصاویر"""
        self.current_page = 0
        self.images_updated.emit()
        self.update_page_info()
        
        total_groups = len(self.image_model.image_groups)
        self.status_changed.emit(
            f'"{self._current_file_name}" با موفقیت بارگذاری شد - {total_groups} گروه تصویر'
        )
    
    def on_extraction_error(self, error_message):
        """مدیریت خطاهای استخراج"""
        self.status_changed.emit('خطا در بارگذاری فایل')
        self.error_occurred.emit(error_message)
    
    def get_current_page_groups(self):
        """دریافت گروه‌های تصاویر صفحه فعلی"""
        start_idx = self.current_page * self.groups_per_page
        end_idx = min(start_idx + self.groups_per_page, len(self.image_model.image_groups))
        return self.image_model.image_groups[start_idx:end_idx]
    
    def next_page(self):
        """رفتن به صفحه بعد"""
        if self.current_page < self.total_pages() - 1:
            self.current_page += 1
            self.update_page_info()
            return True
        return False
    
    def prev_page(self):
        """رفتن به صفحه قبل"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page_info()
            return True
        return False
    
    def total_pages(self):
        """محاسبه تعداد کل صفحات"""
        if not self.image_model.image_groups:
            return 1
        return (len(self.image_model.image_groups) + self.groups_per_page - 1) // self.groups_per_page
    
    def update_page_info(self):
        """به‌روزرسانی اطلاعات صفحه"""
        current_page_num = self.current_page + 1
        total_pages_num = self.total_pages()
        self.page_changed.emit(current_page_num, total_pages_num)
    
    def search_images(self, query):
        """جستجو در تصاویر"""
        if hasattr(self.image_model, 'search_groups'):
            return self.image_model.search_groups(query)
        else:
            # پیاده‌سازی ساده جستجو
            filtered_groups = []
            for group in self.image_model.image_groups:
                if str(group.get('number', '')) in query:
                    filtered_groups.append(group)
            return filtered_groups
    
    def clear_temp_files(self):
        """پاک کردن فایل‌های موقت"""
        try:
            for file in os.listdir(self.temp_dir):
                try:
                    file_path = os.path.join(self.temp_dir, file)
                    os.remove(file_path)
                except Exception:
                    pass  # نادیده گیری خطاهای پاک کردن فایل
        except Exception:
            pass  # نادیده گیری خطای دسترسی به پوشه
    
    def cleanup(self):
        """پاکسازی نهایی منابع"""
        self.clear_temp_files()
        try:
            os.rmdir(self.temp_dir)
        except Exception:
            pass  # نادیده گیری خطای حذف پوشه
    
    def get_image_count(self):
        """دریافت تعداد کل تصاویر"""
        return len(self.image_model.image_groups)
    
    def is_valid_page(self, page_number):
        """بررسی معتبر بودن شماره صفحه"""
        return 0 <= page_number < self.total_pages()
    
    def go_to_page(self, page_number):
        """رفتن به صفحه مشخص"""
        if self.is_valid_page(page_number):
            self.current_page = page_number
            self.update_page_info()
            return True
        return False