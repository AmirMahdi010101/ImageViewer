import os
import tempfile
from typing import List, Dict, Optional, Tuple
from PyQt5.QtCore import QObject, pyqtSignal


class ImageModel(QObject):
    """مدل مدیریت داده‌های تصاویر و pagination"""
    
    # سیگنال‌ها
    data_changed = pyqtSignal()  # تغییر در داده‌ها
    page_changed = pyqtSignal(int)  # تغییر صفحه
    
    def __init__(self):
        super().__init__()
        self.temp_dir = None
        self.image_groups: List[Dict] = []
        self.current_page = 0
        
        # تنظیمات pagination
        self.groups_per_frame = 2    # تعداد گروه در هر فریم
        self.frames_per_page = 6     # تعداد فریم در هر صفحه
        self.groups_per_page = self.groups_per_frame * self.frames_per_page
        
        self._setup_temp_directory()
    
    def _setup_temp_directory(self):
        """ایجاد پوشه موقت برای ذخیره تصاویر"""
        self.temp_dir = tempfile.mkdtemp()
    
    def set_image_groups(self, groups: List[Dict]):
        """تنظیم گروه‌های تصاویر جدید"""
        self.image_groups = groups
        self.current_page = 0
        self.data_changed.emit()
    
    def get_current_page_data(self) -> List[Dict]:
        """دریافت داده‌های صفحه فعلی"""
        start_idx = self.current_page * self.groups_per_page
        end_idx = min(start_idx + self.groups_per_page, len(self.image_groups))
        return self.image_groups[start_idx:end_idx]
    
    def get_page_info(self) -> Dict:
        """دریافت اطلاعات صفحه‌بندی"""
        total_pages = self.get_total_pages()
        groups_in_current_page = len(self.get_current_page_data())
        
        return {
            'current_page': self.current_page + 1,
            'total_pages': total_pages,
            'groups_in_page': groups_in_current_page,
            'total_groups': len(self.image_groups),
            'can_go_next': self.can_go_next(),
            'can_go_prev': self.can_go_prev()
        }
    
    def get_total_pages(self) -> int:
        """محاسبه تعداد کل صفحات"""
        if not self.image_groups:
            return 1
        return (len(self.image_groups) + self.groups_per_page - 1) // self.groups_per_page
    
    def can_go_next(self) -> bool:
        """آیا می‌توان به صفحه بعد رفت؟"""
        return self.current_page < self.get_total_pages() - 1
    
    def can_go_prev(self) -> bool:
        """آیا می‌توان به صفحه قبل رفت؟"""
        return self.current_page > 0
    
    def go_to_next_page(self) -> bool:
        """رفتن به صفحه بعد"""
        if self.can_go_next():
            self.current_page += 1
            self.page_changed.emit(self.current_page)
            return True
        return False
    
    def go_to_prev_page(self) -> bool:
        """رفتن به صفحه قبل"""
        if self.can_go_prev():
            self.current_page -= 1
            self.page_changed.emit(self.current_page)
            return True
        return False
    
    def go_to_page(self, page_number: int) -> bool:
        """رفتن به صفحه مشخص (شماره صفحه از 1 شروع می‌شود)"""
        page_index = page_number - 1
        if 0 <= page_index < self.get_total_pages():
            self.current_page = page_index
            self.page_changed.emit(self.current_page)
            return True
        return False
    
    def search_groups(self, query: str) -> List[Dict]:
        """جستجو در گروه‌های تصاویر بر اساس شماره"""
        if not query.strip():
            return self.image_groups
        
        try:
            # اگر query عدد باشد، بر اساس شماره جستجو کن
            search_number = int(query.strip())
            return [group for group in self.image_groups 
                   if group['number'] == search_number]
        except ValueError:
            # اگر عدد نباشد، جستجوی متنی انجام بده
            query_lower = query.lower()
            return [group for group in self.image_groups 
                   if query_lower in str(group['number'])]
    
    def get_group_by_number(self, number: int) -> Optional[Dict]:
        """دریافت گروه تصویر بر اساس شماره"""
        for group in self.image_groups:
            if group['number'] == number:
                return group
        return None
    
    def get_available_images_in_group(self, group: Dict) -> List[Tuple[str, str]]:
        """دریافت لیست تصاویر موجود در یک گروه"""
        available_images = []
        
        if group['main']:
            available_images.append(('main', group['main']))
        if group['L']:
            available_images.append(('L', group['L']))
        if group['R']:
            available_images.append(('R', group['R']))
            
        return available_images
    
    def get_statistics(self) -> Dict:
        """دریافت آمار کلی تصاویر"""
        if not self.image_groups:
            return {'total_groups': 0, 'total_images': 0, 'main_images': 0, 'crop_images': 0}
        
        total_images = 0
        main_images = 0
        crop_images = 0
        
        for group in self.image_groups:
            if group['main']:
                main_images += 1
                total_images += 1
            if group['L']:
                crop_images += 1
                total_images += 1
            if group['R']:
                crop_images += 1
                total_images += 1
        
        return {
            'total_groups': len(self.image_groups),
            'total_images': total_images,
            'main_images': main_images,
            'crop_images': crop_images
        }
    
    def clear_data(self):
        """پاک کردن همه داده‌ها"""
        self.image_groups.clear()
        self.current_page = 0
        self.data_changed.emit()
    
    def cleanup_temp_files(self):
        """پاک کردن فایل‌های موقت"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                for file_name in os.listdir(self.temp_dir):
                    file_path = os.path.join(self.temp_dir, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(self.temp_dir)
            except Exception:
                pass  # در صورت خطا، نادیده بگیر