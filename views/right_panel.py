from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QScrollArea, 
                           QWidget, QGridLayout, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from typing import List, Dict
from .components import ModernFrame, ImageCard, NavigationBar


class RightPanel(ModernFrame):
    """پنل سمت راست برای نمایش تصاویر"""
    
    # سیگنال‌ها
    prev_page_requested = pyqtSignal()
    next_page_requested = pyqtSignal()
    image_clicked = pyqtSignal(str, str)  # مسیر تصویر و نوع آن
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # تنظیمات نمایش
        self.groups_per_frame = 2
        self.frames_per_page = 6
        self.image_frames = []
        
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        """راه‌اندازی رابط کاربری پنل راست"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # ناحیه اسکرول
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        
        # کانتینر فریم‌های تصاویر
        self.frames_container = QWidget()
        self.frames_container.setStyleSheet("background-color: transparent;")
        self.frames_layout = QVBoxLayout(self.frames_container)
        self.frames_layout.setSpacing(20)
        self.frames_layout.setContentsMargins(10, 10, 10, 10)
        
        # ایجاد فریم‌های نمایش تصاویر
        self._create_image_frames()
        
        # فضای خالی در انتها
        self.frames_layout.addStretch(1)
        
        self.scroll_area.setWidget(self.frames_container)
        
        # نوار ناوبری
        self.navigation_bar = NavigationBar()
        
        # اضافه کردن به لایه اصلی
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.navigation_bar)
        
        # ایجاد افکت opacity برای انیمیشن‌ها
        self.opacity_effect = QGraphicsOpacityEffect()
        self.frames_container.setGraphicsEffect(self.opacity_effect)
        
    def _create_image_frames(self):
        """ایجاد فریم‌های نمایش تصاویر"""
        self.image_frames = []
        
        for i in range(self.frames_per_page):
            # ویجت ردیف
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setSpacing(15)
            row_layout.setContentsMargins(0, 0, 0, 0)
            
            # ایجاد دو فریم در هر ردیف
            row_frames = []
            for j in range(2):
                frame = ModernFrame()
                frame.setMinimumHeight(300)
                frame.setVisible(False)  # پنهان کردن در ابتدا
                
                # گرید برای تصاویر در هر فریم
                grid_layout = QGridLayout(frame)
                grid_layout.setContentsMargins(15, 15, 15, 15)
                grid_layout.setSpacing(15)
                
                row_frames.append((frame, grid_layout))
                row_layout.addWidget(frame)
                
            self.image_frames.extend(row_frames)
            self.frames_layout.addWidget(row_widget)
            
    def _connect_signals(self):
        """اتصال سیگنال‌ها"""
        self.navigation_bar.prev_clicked.connect(self.prev_page_requested.emit)
        self.navigation_bar.next_clicked.connect(self.next_page_requested.emit)
        
    def display_image_groups(self, groups: List[Dict]):
        """نمایش گروه‌های تصاویر"""
        # پاک کردن تصاویر قبلی
        self._clear_all_frames()
        
        # نمایش گروه‌های جدید
        for i, group in enumerate(groups):
            if i >= len(self.image_frames):
                break
                
            frame_idx = i // self.groups_per_frame
            pos_in_frame = i % self.groups_per_frame
            
            if frame_idx < len(self.image_frames):
                frame, grid_layout = self.image_frames[frame_idx]
                self._display_single_group(group, grid_layout, pos_in_frame)
                frame.setVisible(True)
                
        # پنهان کردن فریم‌های خالی
        frames_needed = (len(groups) + self.groups_per_frame - 1) // self.groups_per_frame
        for i, (frame, _) in enumerate(self.image_frames):
            frame.setVisible(i < frames_needed)
            
    def _display_single_group(self, group: Dict, grid_layout: QGridLayout, row: int):
        """نمایش یک گروه تصویر"""
        img_num = group["number"]
        
        # ویجت برای نمایش تصاویر در یک ردیف
        img_widget = QWidget()
        img_layout = QHBoxLayout(img_widget)
        img_layout.setContentsMargins(0, 0, 0, 0)
        img_layout.setSpacing(15)
        
        # نمایش تصویر اصلی
        if group['main']:
            main_card = ImageCard(group['main'], f"{img_num}.jpg")
            main_card.mousePressEvent = lambda event, path=group['main']: self._on_image_clicked(path, 'main')
            img_layout.addWidget(main_card)
            
        # نمایش تصویر برش چپ
        if group['L']:
            left_card = ImageCard(group['L'], f"{img_num}_L_cb.jpg")
            left_card.mousePressEvent = lambda event, path=group['L']: self._on_image_clicked(path, 'L')
            img_layout.addWidget(left_card)
            
        # نمایش تصویر برش راست
        if group['R']:
            right_card = ImageCard(group['R'], f"{img_num}_R_cb.jpg")
            right_card.mousePressEvent = lambda event, path=group['R']: self._on_image_clicked(path, 'R')
            img_layout.addWidget(right_card)
            
        # فضای خالی
        img_layout.addStretch()
        
        # اضافه کردن به گرید
        grid_layout.addWidget(img_widget, row, 0, 1, 3)
        
    def _on_image_clicked(self, image_path: str, image_type: str):
        """رویداد کلیک روی تصویر"""
        self.image_clicked.emit(image_path, image_type)
        
    def _clear_all_frames(self):
        """پاک کردن همه فریم‌ها"""
        for _, grid_layout in self.image_frames:
            while grid_layout.count():
                item = grid_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                    
    def update_navigation(self, current_page: int, total_pages: int, 
                         can_go_prev: bool, can_go_next: bool):
        """به‌روزرسانی نوار ناوبری"""
        self.navigation_bar.update_navigation(
            current_page, total_pages, can_go_prev, can_go_next
        )
        
    def show_page_info(self, groups_in_page: int, total_groups: int):
        """نمایش اطلاعات صفحه"""
        self.navigation_bar.show_page_info(groups_in_page, total_groups)
        
    def animate_page_transition(self, direction: str = "fade"):
        """انیمیشن تغییر صفحه"""
        if direction == "fade":
            self._fade_animation()
        elif direction == "slide":
            self._slide_animation()
            
    def _fade_animation(self):
        """انیمیشن محو و ظاهر شدن"""
        # انیمیشن محو
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(200)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.3)
        self.fade_out.setEasingCurve(QEasingCurve.OutCubic)
        
        # انیمیشن ظاهر شدن
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0.3)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.InCubic)
        
        # شروع انیمیشن محو
        self.fade_out.start()
        return self.fade_out, self.fade_in
        
    def _slide_animation(self):
        """انیمیشن کشیدن (برای آینده)"""
        # می‌توان بعداً پیاده‌سازی کرد
        pass
        
    def set_loading_state(self, loading: bool):
        """تنظیم حالت بارگذاری"""
        self.navigation_bar.set_loading(loading)
        
        if loading:
            self._clear_all_frames()
            
    def show_empty_state(self, message: str = "هیچ تصویری برای نمایش وجود ندارد"):
        """نمایش حالت خالی"""
        self._clear_all_frames()
        
        # اضافه کردن پیام خالی
        from PyQt5.QtWidgets import QLabel
        empty_label = QLabel(message)
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet("color: #888; font-size: 16px; padding: 50px;")
        
        if len(self.image_frames) > 0:
            frame, grid_layout = self.image_frames[0]
            grid_layout.addWidget(empty_label, 0, 0, 1, 3)
            frame.setVisible(True)
            
    def reset(self):
        """بازنشانی پنل"""
        self._clear_all_frames()
        self.navigation_bar.reset()
        
        # پنهان کردن همه فریم‌ها
        for frame, _ in self.image_frames:
            frame.setVisible(False)