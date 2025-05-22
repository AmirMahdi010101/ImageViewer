# views/main_view.py
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                           QSplitter, QScrollArea, QFrame, QStatusBar, QMessageBox,
                           QProgressBar, QApplication)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from views.components.modern_frame import ModernFrame
from views.components.modern_button import ModernButton
from views.components.navigation_button import NavigationButton
from views.components.image_card import ImageCard
from views.panels.left_panel import LeftPanel
from views.panels.right_panel import RightPanel
from controllers.application_controller import ApplicationController


class MainView(QMainWindow):
    """View اصلی برنامه با معماری MVC"""
    
    def __init__(self):
        super().__init__()
        
        # ایجاد کنترلر اصلی
        self.controller = ApplicationController()
        
        # متغیرهای UI
        self.image_frames = []
        self.frames_per_page = 6
        self.groups_per_frame = 2
        
        # مقداردهی اولیه
        self.init_ui()
        self.setup_styles()
        self.connect_controller_signals()
        
        # مقداردهی کنترلرها
        self.controller.initialize_widgets(self)
    
    def init_ui(self):
        """مقداردهی اولیه رابط کاربری"""
        self.setWindowTitle('نمایش‌دهنده تصاویر مدرن - MVC')
        self.setGeometry(100, 100, 1280, 800)
        
        # ایجاد نوار وضعیت
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('برنامه آماده است')
        
        # ایجاد ویجت مرکزی
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # لایه اصلی
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # ایجاد اسپلیتر
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(2)
        self.splitter.setStyleSheet("QSplitter::handle { background-color: #dddddd; }")
        
        # ایجاد پنل‌ها
        self.left_panel = LeftPanel()
        self.right_panel = RightPanel()
        
        # دسترسی به کامپوننت‌های مهم
        self.file_list = self.left_panel.file_list
        self.search_input = self.left_panel.search_input
        self.scroll_area = self.right_panel.scroll_area
        self.frames_container = self.right_panel.frames_container
        self.frames_layout = self.right_panel.frames_layout
        self.prev_btn = self.right_panel.prev_btn
        self.next_btn = self.right_panel.next_btn
        self.page_label = self.right_panel.page_label
        
        # اضافه کردن پنل‌ها به اسپلیتر
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([250, 1030])
        
        # اضافه کردن اسپلیتر به لایه اصلی
        main_layout.addWidget(self.splitter)
        
        # ایجاد فریم‌های تصویر
        self.create_image_frames()
        
        # اتصال سیگنال‌های UI
        self.connect_ui_signals()
    
    def create_image_frames(self):
        """ایجاد فریم‌های نمایش تصاویر"""
        self.image_frames = []
        
        # ایجاد ردیف‌های فریم
        for i in range(self.frames_per_page):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setSpacing(15)
            
            # ایجاد دو فریم در هر ردیف
            for j in range(2):
                frame = ModernFrame()
                frame.setMinimumHeight(300)
                
                # چیدمان گرید برای هر فریم
                from PyQt5.QtWidgets import QGridLayout
                grid_layout = QGridLayout(frame)
                grid_layout.setContentsMargins(15, 15, 15, 15)
                grid_layout.setSpacing(15)
                
                # اضافه کردن فریم به لیست
                self.image_frames.append((frame, grid_layout))
                row_layout.addWidget(frame)
            
            # اضافه کردن ردیف به لایه اصلی
            self.frames_layout.addWidget(row_widget)
        
        # اضافه کردن فضای خالی
        self.frames_layout.addStretch(1)
    
    def connect_ui_signals(self):
        """اتصال سیگنال‌های رابط کاربری"""
        # دکمه باز کردن فایل
        self.left_panel.open_btn.clicked.connect(
            lambda: self.controller.open_zip_file(self)
        )
        
        # دکمه‌های ناوبری
        self.prev_btn.clicked.connect(
            lambda: self.controller.prev_page(self.frames_container)
        )
        self.next_btn.clicked.connect(
            lambda: self.controller.next_page(self.frames_container)
        )
    
    def connect_controller_signals(self):
        """اتصال سیگنال‌های کنترلر"""
        # سیگنال‌های اصلی
        self.controller.status_updated.connect(self.update_status)
        self.controller.images_loaded.connect(self.display_images)
        self.controller.page_updated.connect(self.update_page_info)
        self.controller.navigation_updated.connect(self.update_navigation_buttons)
        self.controller.file_list_updated.connect(self.update_file_list)
        
        # سیگنال‌های خطا
        self.controller.main_controller.error_occurred.connect(self.show_error_message)
        
        # سیگنال‌های پیشرفت
        self.controller.main_controller.progress_changed.connect(self.show_progress)
    
    def setup_styles(self):
        """تنظیم استایل‌های برنامه"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QScrollArea {
                background-color: #f5f7fa;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QListWidget {
                background-color: #ffffff;
                border-radius: 5px;
                border: 1px solid #e0e0e0;
                padding: 5px;
            }
            QListWidget::item {
                height: 28px;
                border-radius: 4px;
                padding: 5px;
                margin: 2px 0px;
            }
            QListWidget::item:selected {
                background-color: #e6f0ff;
                color: #2a66c8;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
            }
        """)
    
    # متدهای پردازش سیگنال‌ها
    def update_status(self, message):
        """به‌روزرسانی نوار وضعیت"""
        self.status_bar.showMessage(message)
    
    def display_images(self):
        """نمایش تصاویر صفحه فعلی"""
        # پاک کردن فریم‌ها
        self.clear_image_frames()
        
        # دریافت گروه‌های تصاویر از کنترلر
        image_groups = self.controller.get_current_page_groups()
        
        # نمایش گروه‌ها
        groups_per_page = self.groups_per_frame * self.frames_per_page
        for i, group in enumerate(image_groups[:groups_per_page]):
            frame_idx = i // self.groups_per_frame
            pos_in_frame = i % self.groups_per_frame
            
            if frame_idx < len(self.image_frames):
                frame, grid_layout = self.image_frames[frame_idx]
                self.display_image_group(group, grid_layout, pos_in_frame)
        
        # نمایش/مخفی کردن فریم‌ها
        frames_needed = (len(image_groups) + self.groups_per_frame - 1) // self.groups_per_frame
        for i, (frame, _) in enumerate(self.image_frames):
            frame.setVisible(i < frames_needed)
    
    def display_image_group(self, group, grid_layout, row):
        """نمایش یک گروه تصویر"""
        img_num = group.get("number", 0)
        main_path = group.get("main")
        left_path = group.get("L")
        right_path = group.get("R")
        
        # ایجاد ویجت برای نمایش تصاویر
        img_widget = QWidget()
        img_layout = QHBoxLayout(img_widget)
        img_layout.setContentsMargins(0, 0, 0, 0)
        img_layout.setSpacing(15)
        
        # نمایش تصاویر
        if main_path:
            main_card = ImageCard(main_path, f"{img_num}.jpg")
            img_layout.addWidget(main_card)
        
        if left_path:
            left_card = ImageCard(left_path, f"{img_num}_L_cb.jpg")
            img_layout.addWidget(left_card)
        
        if right_path:
            right_card = ImageCard(right_path, f"{img_num}_R_cb.jpg")
            img_layout.addWidget(right_card)
        
        img_layout.addStretch()
        
        # اضافه کردن به گرید
        grid_layout.addWidget(img_widget, row + 1, 0, 1, 3)
    
    def clear_image_frames(self):
        """پاک کردن تمام فریم‌های تصویر"""
        for _, grid_layout in self.image_frames:
            while grid_layout.count():
                item = grid_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
    
    def update_page_info(self, current_page, total_pages):
        """به‌روزرسانی اطلاعات صفحه"""
        self.page_label.setText(f'صفحه {current_page} از {total_pages}')
    
    def update_navigation_buttons(self, prev_enabled, next_enabled):
        """به‌روزرسانی دکمه‌های ناوبری"""
        self.prev_btn.setEnabled(prev_enabled)
        self.next_btn.setEnabled(next_enabled)
    
    def update_file_list(self, file_name):
        """به‌روزرسانی لیست فایل‌ها"""
        # این کار در FileController انجام می‌شود
        pass
    
    def show_error_message(self, error_message):
        """نمایش پیام خطا"""
        QMessageBox.critical(self, 'خطا', error_message)
    
    def show_progress(self, current, total):
        """نمایش نوار پیشرفت"""
        if not hasattr(self, 'progress_bar'):
            self.progress_bar = QProgressBar(self)
            self.status_bar.addWidget(self.progress_bar)
        
        if total > 0:
            self.progress_bar.setRange(0, total)
            self.progress_bar.setValue(current)
        else:
            self.progress_bar.setRange(0, 0)  # نوار نامحدود
        
        if current >= total and total > 0:
            # حذف نوار پیشرفت پس از اتمام
            QTimer.singleShot(1000, self.hide_progress)
    
    def hide_progress(self):
        """مخفی کردن نوار پیشرفت"""
        if hasattr(self, 'progress_bar'):
            self.status_bar.removeWidget(self.progress_bar)
            self.progress_bar.deleteLater()
            del self.progress_bar
    
    def closeEvent(self, event):
        """پردازش بستن برنامه"""
        # پاکسازی منابع کنترلر
        self.controller.cleanup()
        
        # نمایش پیام خداحافظی
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("با تشکر از استفاده شما")
        msg_box.setWindowTitle("خروج")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #333333;
                font-size: 12px;
            }
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
        """)
        msg_box.exec_()
        
        super().closeEvent(event)