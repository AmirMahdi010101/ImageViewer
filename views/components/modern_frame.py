from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt


class ModernFrame(QFrame):
    """فریم مدرن با سایه و حاشیه گرد"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modernFrame")
        self.setProperty("class", "modern-frame")
        
        # تنظیم ویژگی‌های پیش‌فرض
        self.setFrameStyle(QFrame.StyledPanel)
        
    def set_minimum_size(self, width: int, height: int):
        """تنظیم حداقل اندازه فریم"""
        self.setMinimumSize(width, height)
        return self
        
    def set_maximum_size(self, width: int, height: int):
        """تنظیم حداکثر اندازه فریم"""
        self.setMaximumSize(width, height)
        return self
        
    def set_fixed_size(self, width: int, height: int):
        """تنظیم اندازه ثابت فریم"""
        self.setFixedSize(width, height)
        return self