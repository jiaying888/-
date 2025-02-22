import json
import pandas as pd
from tqdm import tqdm
import os

# 路径配置（根据实际位置修改）
input_json = "./captions_train2017.json"
output_csv = "coco_captions.csv"

# 内存友好的分块处理
chunk_size = 1000  # 每处理1000条保存一次

def process_coco_json():
    # 读取JSON数据
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取关键信息
    images = {img['id']: img['file_name'] for img in data['images']}
    
    # 分块处理标注
    chunks = []
    for i in tqdm(range(0, len(data['annotations']), chunk_size)):
        chunk = data['annotations'][i:i+chunk_size]
        rows = []
        for ann in chunk:
            rows.append({
                "image_id": ann['image_id'],
                "file_name": images.get(ann['image_id'], 'unknown'),
                "caption": ann['caption'],
                "coco_url": f"http://images.cocodataset.org/train2017/{images.get(ann['image_id'], '')}"
            })
        chunks.append(pd.DataFrame(rows))
    
    # 合并并保存
    final_df = pd.concat(chunks)
    final_df.to_csv(output_csv, index=False)
    print(f"转换完成！共处理 {len(final_df)} 条数据，保存至 {output_csv}")

if __name__ == "__main__":
    process_coco_json()