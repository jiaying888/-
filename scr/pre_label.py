#### **步骤3.2 运行预标注脚本**  
# scripts/pre_label.py
from ultralytics import YOLO
import pandas as pd
import os

# 加载模型
model = YOLO('yolov8n.pt')  # 自动下载约12MB的小模型

# 读取元数据
df = pd.read_csv("clean_data/image_descriptions.csv")
output = []

# 处理每张图片C:\Users\Fiary\anaconda3\envs\label_studio\project\datas2\clean_data\coco2_images
for idx, row in df.iterrows():
    # 使用os.path自动处理路径分隔符
    base_dir = r"C:\Users\Fiary\anaconda3\envs\label_studio\project\datas2\clean_data\coco2_images"  # 使用原始字符串
    img_path = os.path.join(base_dir, row['image-id'])
    results = model.predict(img_path)
    
    # 提取检测结果
    for r in results:
        for box in r.boxes:
            output.append({
                "image": row['image_path'],
                "label": r.names[box.cls.item()],
                "x_min": box.xyxy[0][0].item(),
                "y_min": box.xyxy[0][1].item(),
                "x_max": box.xyxy[0][2].item(),
                "y_max": box.xyxy[0][3].item()
            })

# 保存预标注结果
pd.DataFrame(output).to_csv("clean_data/pre_labels.csv", index=False)
print(f"生成{len(output)}条预标注")