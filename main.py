# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

# اضافه کردن مسیر پروژه به sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.main_view import MainView


class ImageViewerApplication:
    """کلاس اصلی برنامه"""
    
    def __init__(self):
        self.app = None
        self.main_view = None
    
    def setup_application(self):
        """تنظیم برنامه PyQt5"""
        self.app = QApplication(sys.argv)
        
        # تنظیم فونت پیش‌فرض
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.app.setFont(font)
        
        # تنظیم نام برنامه
        self.app.setApplicationName("Image Viewer MVC")
        self.app.setApplicationVersion("2.0")
        self.app.setOrganizationName("Image Viewer Team")
    
    def create_main_view(self):
        """ایجاد View اصلی"""
        self.main_view = MainView()
        return self.main_view
    
    def show_welcome_message(self):
        """نمایش پیام خوش‌آمدگویی"""
        if self.main_view:
            QTimer.singleShot(500, lambda: 
                self.main_view.status_bar.showMessage(
                    'به نرم‌افزار نمایشگر تصاویر خوش آمدید - نسخه MVC'
                )
            )
    
    def run(self):
        """اجرای برنامه"""
        # تنظیم برنامه
        self.setup_application()
        
        # ایجاد و نمایش View اصلی
        main_view = self.create_main_view()
        main_view.show()
        
        # نمایش پیام خوش‌آمدگویی
        self.show_welcome_message()
        
        # شروع حلقه اصلی برنامه
        return self.app.exec_()


def main():
    """تابع اصلی برنامه"""
    try:
        # ایجاد و اجرای برنامه
        app = ImageViewerApplication()
        exit_code = app.run()
        
        # خروج با کد مناسب
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"خطا در اجرای برنامه: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()