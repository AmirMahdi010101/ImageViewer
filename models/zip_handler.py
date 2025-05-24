import os
import re
import zipfile
import tempfile
from typing import List, Dict, Optional
from PyQt5.QtCore import QThread, pyqtSignal


class ZipHandler(QThread):
    """کلاس پردازش فایل‌های ZIP و استخراج تصاویر"""
    
    # سیگنال‌ها
    extraction_finished = pyqtSignal(list)  # لیست گروه‌های تصاویر
    extraction_progress = pyqtSignal(int)   # درصد پیشرفت
    extraction_error = pyqtSignal(str)      # پیام خطا

    def __init__(self, zip_path: str, temp_dir: str):
        super().__init__()
        self.zip_path = zip_path
        self.temp_dir = temp_dir
        self._is_cancelled = False

    def run(self):
        """اجرای عملیات استخراج در تردی جداگانه"""
        try:
            self._clear_temp_directory()
            image_groups = self._extract_and_group_images()
            if not self._is_cancelled:
                self.extraction_finished.emit(image_groups)
        except Exception as e:
            self.extraction_error.emit(f"خطا در پردازش فایل ZIP: {str(e)}")

    def cancel(self):
        """لغو عملیات استخراج"""
        self._is_cancelled = True

    def _clear_temp_directory(self):
        """پاک کردن فایل‌های قبلی از پوشه موقت"""
        try:
            for file_name in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            raise Exception(f"خطا در پاک کردن پوشه موقت: {str(e)}")

    def _extract_and_group_images(self) -> List[Dict]:
        """استخراج و گروه‌بندی تصاویر از فایل ZIP"""
        image_groups = []
        image_dict = {}

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                # یافتن فایل‌های تصویری
                jpg_files = [f for f in zip_ref.namelist() 
                           if f.lower().endswith(('.jpg', '.jpeg')) and not f.startswith('__MACOSX')]
                
                total_files = len(jpg_files)
                if total_files == 0:
                    raise Exception("هیچ فایل تصویری در آرشیو یافت نشد")

                # استخراج فایل‌ها
                for i, file_path in enumerate(jpg_files):
                    if self._is_cancelled:
                        break
                        
                    self._extract_single_image(zip_ref, file_path, image_dict)
                    
                    # به‌روزرسانی پیشرفت
                    progress = int((i + 1) / total_files * 100)
                    self.extraction_progress.emit(progress)

                # تبدیل دیکشنری به لیست گروه‌ها
                image_groups = self._convert_dict_to_groups(image_dict)
                
        except zipfile.BadZipFile:
            raise Exception("فایل ZIP معتبر نیست")
        except Exception as e:
            raise Exception(f"خطا در استخراج فایل‌ها: {str(e)}")

        return image_groups

    def _extract_single_image(self, zip_ref: zipfile.ZipFile, file_path: str, image_dict: Dict):
        """استخراج یک فایل تصویر و اضافه کردن به دیکشنری"""
        file_name = os.path.basename(file_path)
        if not file_name:
            return

        # مسیر خروجی
        output_path = os.path.join(self.temp_dir, file_name)
        
        # استخراج فایل
        with zip_ref.open(file_path) as source, open(output_path, 'wb') as target:
            target.write(source.read())

        # تشخیص نوع فایل و گروه‌بندی
        self._categorize_image(file_name, output_path, image_dict)

    def _categorize_image(self, file_name: str, file_path: str, image_dict: Dict):
        """دسته‌بندی تصویر بر اساس نام فایل"""
        main_pattern = re.match(r'^(\d+)\.jpg$', file_name, re.IGNORECASE)
        
        crop_pattern = re.match(r'^(\d+)_(L|R)_cb\.jpg$', file_name, re.IGNORECASE)

        if main_pattern:
            img_number = int(main_pattern.group(1))
            self._add_to_group(image_dict, img_number, 'main', file_path)
        elif crop_pattern:
            img_number = int(crop_pattern.group(1))
            side = crop_pattern.group(2)
            self._add_to_group(image_dict, img_number, side, file_path)

    def _add_to_group(self, image_dict: Dict, number: int, type_key: str, file_path: str):
        """اضافه کردن تصویر به گروه مربوطه"""
        if number not in image_dict:
            image_dict[number] = {"main": None, "L": None, "R": None}
        image_dict[number][type_key] = file_path

    def _convert_dict_to_groups(self, image_dict: Dict) -> List[Dict]:
        """تبدیل دیکشنری به لیست گروه‌های مرتب شده"""
        image_groups = []
        
        for img_number, paths in image_dict.items():
            image_groups.append({
                "number": img_number,
                "main": paths["main"],
                "L": paths["L"],
                "R": paths["R"]
            })
        
        # مرتب‌سازی بر اساس شماره
        image_groups.sort(key=lambda group: group["number"])
        return image_groups