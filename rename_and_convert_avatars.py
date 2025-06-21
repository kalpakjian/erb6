# rename_and_convert_avatars.py
import os
from PIL import Image
import re

# 設定參數
SOURCE_DIR = "static/icons"  # 原始圖片資料夾
OUTPUT_DIR = "static/icons/avatars"  # 輸出資料夾
TARGET_SIZE = (256, 256)  # 頭像尺寸
OUTPUT_FORMAT = "PNG"  # 輸出格式

def ensure_dir(directory):
    """確保目錄存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def is_image_file(filename):
    """檢查是否為圖片檔案"""
    extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")
    return filename.lower().endswith(extensions)

def make_square_image(image, size):
    """將圖片轉為正方形並調整尺寸"""
    # 調整圖片至目標尺寸，保持比例
    image.thumbnail(size, Image.Resampling.LANCZOS)
    
    # 創建白色背景的正方形畫布
    new_image = Image.new("RGBA", size, (255, 255, 255, 0))
    
    # 將圖片貼到畫布中央
    offset = ((size[0] - image.size[0]) // 2, (size[1] - image.size[1]) // 2)
    new_image.paste(image, offset)
    
    return new_image

def process_images():
    """處理圖片：重命名並轉換格式"""
    ensure_dir(OUTPUT_DIR)
    
    # 取得所有圖片檔案
    image_files = [f for f in os.listdir(SOURCE_DIR) if is_image_file(f)]
    
    for index, filename in enumerate(image_files, 1):
        try:
            # 讀取圖片
            img_path = os.path.join(SOURCE_DIR, filename)
            with Image.open(img_path) as img:
                # 轉換為正方形並調整尺寸
                processed_img = make_square_image(img, TARGET_SIZE)
                
                # 生成新檔案名稱（avatar_001.png）
                new_filename = f"avatar_{index:03d}.png"
                output_path = os.path.join(OUTPUT_DIR, new_filename)
                
                # 保存圖片
                processed_img.save(output_path, OUTPUT_FORMAT)
                print(f"已處理: {filename} -> {new_filename}")
                
        except Exception as e:
            print(f"處理 {filename} 時發生錯誤: {e}")

if __name__ == "__main__":
    process_images()
