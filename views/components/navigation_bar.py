from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from .navigation_button import NavigationButton


class NavigationBar(QFrame):
    """نوار ناوبری مدرن با دکمه‌های قبل/بعد و نمایش اطلاعات صفحه"""
    
    # سیگنال‌ها
    prev_clicked = pyqtSignal()
    next_clicked = pyqtSignal()
    page_info_clicked = pyqtSignal()  # کلیک روی اطلاعات صفحه
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_page = 1
        self.total_pages = 1
        
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        """راه‌اندازی رابط کاربری نوار ناوبری"""
        self.setMaximumHeight(60)
        self.setFrameStyle(QFrame.NoFrame)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(15)
        
        # فضای خالی از سمت چپ
        layout.addStretch()
        
        # دکمه قبل
        self.prev_btn = NavigationButton("←")
        self.prev_btn.set_arrow_left()
        self.prev_btn.setEnabled(False)
        
        # لیبل اطلاعات صفحه
        self.page_label = QLabel(f"صفحه {self.current_page} از {self.total_pages}")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setMinimumWidth(120)
        
        # تنظیم فونت لیبل
        label_font = QFont()
        label_font.setPointSize(13)
        label_font.setBold(True)
        self.page_label.setFont(label_font)
        self.page_label.setStyleSheet("color: #333333;")
        
        # امکان کلیک روی لیبل برای رفتن به صفحه خاص
        self.page_label.mousePressEvent = self._on_page_label_clicked
        self.page_label.setToolTip("کلیک کنید تا به صفحه مورد نظر بروید")
        self.page_label.setStyleSheet("""
            QLabel {
                color: #333333;
                padding: 5px;
                border-radius: 3px;
            }
            QLabel:hover {
                background-color: #f0f0f0;
                cursor: pointer;
            }
        """)
        
        # دکمه بعد
        self.next_btn = NavigationButton("→")
        self.next_btn.set_arrow_right()
        self.next_btn.setEnabled(False)
        
        # اضافه کردن ویجت‌ها
        layout.addWidget(self.prev_btn)
        layout.addWidget(self.page_label)
        layout.addWidget(self.next_btn)
        
    def _connect_signals(self):
        """اتصال سیگنال‌ها"""
        self.prev_btn.clicked.connect(self.prev_clicked.emit)
        self.next_btn.clicked.connect(self.next_clicked.emit)
        
    def _on_page_label_clicked(self, event):
        """رویداد کلیک روی لیبل صفحه"""
        self.page_info_clicked.emit()
        
    def update_navigation(self, current_page: int, total_pages: int, 
                         can_go_prev: bool = None, can_go_next: bool = None):
        """به‌روزرسانی اطلاعات ناوبری"""
        self.current_page = current_page
        self.total_pages = total_pages
        
        # به‌روزرسانی متن لیبل
        self.page_label.setText(f"صفحه {current_page} از {total_pages}")
        
        # تنظیم وضعیت دکمه‌ها
        if can_go_prev is not None:
            self.prev_btn.setEnabled(can_go_prev)
        else:
            self.prev_btn.setEnabled(current_page > 1)
            
        if can_go_next is not None:
            self.next_btn.setEnabled(can_go_next)
        else:
            self.next_btn.setEnabled(current_page < total_pages)
            
    def set_loading(self, loading: bool):
        """تنظیم حالت بارگذاری"""
        self.prev_btn.setEnabled(not loading)
        self.next_btn.setEnabled(not loading)
        
        if loading:
            self.page_label.setText("در حال بارگذاری...")
        else:
            self.page_label.setText(f"صفحه {self.current_page} از {self.total_pages}")
            
    def show_page_info(self, groups_in_page: int, total_groups: int):
        """نمایش اطلاعات تفصیلی صفحه"""
        tooltip_text = f"""
        صفحه {self.current_page} از {self.total_pages}
        گروه‌های این صفحه: {groups_in_page}
        کل گروه‌ها: {total_groups}
        """
        self.page_label.setToolTip(tooltip_text.strip())
        
    def highlight_direction(self, direction: str):
        """برجسته کردن دکمه جهت (برای راهنمایی کاربر)"""
        if direction == "prev" and self.prev_btn.isEnabled():
            self.prev_btn.pulse_animation()
        elif direction == "next" and self.next_btn.isEnabled():
            self.next_btn.pulse_animation()
            
    def reset(self):
        """بازنشانی نوار ناوبری"""
        self.current_page = 1
        self.total_pages = 1
        self.update_navigation(1, 1)
        
    def get_navigation_info(self) -> dict:
        """دریافت اطلاعات فعلی ناوبری"""
        return {
            'current_page': self.current_page,
            'total_pages': self.total_pages,
            'can_go_prev': self.prev_btn.isEnabled(),
            'can_go_next': self.next_btn.isEnabled()
        }