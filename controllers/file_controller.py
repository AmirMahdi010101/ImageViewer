# controllers/file_controller.py
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class FileController(QObject):
    """کنترلر مدیریت لیست فایل‌ها"""
    
    # سیگنال‌ها
    file_selected = pyqtSignal(str)  # file_name
    file_added = pyqtSignal(str)     # file_name
    file_removed = pyqtSignal(str)   # file_name
    list_cleared = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # مرجع به ویجت لیست
        self.file_list_widget = None
        
        # لیست فایل‌های بارگذاری شده
        self.loaded_files = []
        
        # فایل فعلی
        self.current_file = None
    
    def set_file_list_widget(self, file_list_widget):
        """تنظیم ویجت لیست فایل‌ها"""
        self.file_list_widget = file_list_widget
        
        # اتصال سیگنال‌های ویجت
        if self.file_list_widget:
            self.file_list_widget.itemClicked.connect(self.on_item_clicked)
            self.file_list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
            self.file_list_widget.currentItemChanged.connect(self.on_current_item_changed)
    
    def add_file(self, file_name, file_path=None):
        """اضافه کردن فایل به لیست"""
        if not self.file_list_widget:
            return False
        
        # بررسی تکراری نبودن فایل
        if file_name in self.loaded_files:
            self.select_file(file_name)
            return True
        
        # پاک کردن لیست قبلی (فعلاً فقط یک فایل پشتیبانی می‌شود)
        self.clear_files()
        
        # ایجاد آیتم جدید
        item = QListWidgetItem(file_name)
        item.setToolTip(file_path if file_path else file_name)
        
        # اضافه کردن به ویجت
        self.file_list_widget.addItem(item)
        
        # اضافه کردن به لیست داخلی
        self.loaded_files.append(file_name)
        self.current_file = file_name
        
        # انتخاب فایل جدید
        self.file_list_widget.setCurrentItem(item)
        
        # ارسال سیگنال
        self.file_added.emit(file_name)
        
        return True
    
    def remove_file(self, file_name):
        """حذف فایل از لیست"""
        if not self.file_list_widget:
            return False
        
        # پیدا کردن آیتم
        for i in range(self.file_list_widget.count()):
            item = self.file_list_widget.item(i)
            if item.text() == file_name:
                # حذف از ویجت
                self.file_list_widget.takeItem(i)
                
                # حذف از لیست داخلی
                if file_name in self.loaded_files:
                    self.loaded_files.remove(file_name)
                
                # بررسی فایل فعلی
                if self.current_file == file_name:
                    self.current_file = None
                
                # ارسال سیگنال
                self.file_removed.emit(file_name)
                
                return True
        
        return False
    
    def clear_files(self):
        """پاک کردن تمام فایل‌ها"""
        if self.file_list_widget:
            self.file_list_widget.clear()
        
        self.loaded_files.clear()
        self.current_file = None
        
        self.list_cleared.emit()
    
    def select_file(self, file_name):
        """انتخاب فایل مشخص"""
        if not self.file_list_widget:
            return False
        
        # پیدا کردن و انتخاب آیتم
        for i in range(self.file_list_widget.count()):
            item = self.file_list_widget.item(i)
            if item.text() == file_name:
                self.file_list_widget.setCurrentItem(item)
                self.current_file = file_name
                return True
        
        return False
    
    def get_selected_file(self):
        """دریافت فایل انتخاب شده"""
        if self.file_list_widget:
            current_item = self.file_list_widget.currentItem()
            if current_item:
                return current_item.text()
        return None
    
    def get_file_count(self):
        """دریافت تعداد فایل‌ها"""
        return len(self.loaded_files)
    
    def get_all_files(self):
        """دریافت لیست تمام فایل‌ها"""
        return self.loaded_files.copy()
    
    def is_file_loaded(self, file_name):
        """بررسی بارگذاری فایل"""
        return file_name in self.loaded_files
    
    # Event Handlers
    def on_item_clicked(self, item):
        """پردازش کلیک روی آیتم"""
        if item:
            file_name = item.text()
            self.current_file = file_name
            self.file_selected.emit(file_name)
    
    def on_item_double_clicked(self, item):
        """پردازش دابل کلیک روی آیتم"""
        if item:
            file_name = item.text()
            # می‌توان عملیات خاصی برای دابل کلیک تعریف کرد
            # مثل باز کردن جزئیات فایل
            pass
    
    def on_current_item_changed(self, current, previous):
        """پردازش تغییر آیتم فعلی"""
        if current:
            file_name = current.text()
            if self.current_file != file_name:
                self.current_file = file_name
                self.file_selected.emit(file_name)