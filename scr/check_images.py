# scripts/check_images.py
import os
from PIL import Image
import shutil

def check_and_move(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    bad_images = []
    
    for filename in os.listdir(src_dir):
        img_path = os.path.join(src_dir, filename)
        try:
            # 基础质量检查
            with Image.open(img_path) as img:
                img.verify()  # 校验文件完整性
                
                # 分辨率要求：最小600x600
                if img.width < 450 or img.height < 450:
                    raise ValueError("分辨率不足")
                    
                # 保存合格图片
                shutil.copy(img_path, os.path.join(dst_dir, filename))
        except Exception as e:
            bad_images.append((filename, str(e)))
    
    print(f"合格图片：{len(os.listdir(dst_dir))}/200")
    print("问题图片：")
    for f, err in bad_images:
        print(f" - {f}: {err}")

# 执行检查（根据实际路径修改）
check_and_move(
    src_dir="./coco_images",
    dst_dir="./coco2_images"
)