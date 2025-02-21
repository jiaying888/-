import pandas as pd
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# 路径配置
csv_path = "./coco_captions.csv"
image_dir = Path("coco_images")
image_dir.mkdir(exist_ok=True)  # 创建图片存储目录

# 读取CSV文件（仅加载必要列）
df = pd.read_csv(csv_path, usecols=['file_name', 'caption']).drop_duplicates('file_name').head(350)

# 生成下载URL（COCO官方地址格式）
def generate_url(file_name):
    return f"http://images.cocodataset.org/train2017/{file_name}"

# 下载单张图片（带重试机制）
def download_image(row):
    url = generate_url(row['file_name'])
    save_path = image_dir / row['file_name']
    
    if save_path.exists():  # 跳过已存在文件
        return
    
    for _ in range(3):  # 最大重试3次
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            return
        except Exception as e:
            print(f"下载失败 {row['file_name']}: {str(e)}")
    print(f"放弃下载 {row['file_name']}")

# 使用8线程加速下载
with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(download_image, df.to_dict('records'))

print(f"下载完成！图片保存在 {image_dir}")