import pandas as pd
from label_studio_sdk import Client
from PIL import Image

# 连接Label Studio
ls = Client(url='http://localhost:8080', api_key='e5ea95f7b959bda252319ea20d2b753fb768c8ef')
project = ls.get_project(34)  # 项目ID

# 读取CSV文件
df = pd.read_csv('clean_data/multimodal_labels.csv')

# 按图片路径分组
grouped = df.groupby('image')



tasks = []

df1 = pd.read_csv("clean_data/image_descriptions.csv")
for idx, row in df1.iterrows():
    # 使用os.path自动处理路径分隔符
    base_dir = r"C:\Users\Fiary\anaconda3\envs\label_studio\project\datas2\clean_data\coco2_images"  # 使用原始字符串
    img_path = os.path.join(base_dir, row['image-id'])

for image_path, group in grouped:
    image_path = image_path.strip()  # 清理路径中的空格
    text_description = group['text'].iloc[0]   #获取文本描述
    # 获取图片尺寸
    try:
        with Image.open(img_path) as img:
            img_width, img_height = img.size
    except FileNotFoundError:
        print(f"错误：图片 {image_path} 不存在，跳过")
        continue
    
    # 构建任务数据(包含图片和文本)
    task = {
        'data': {
            'image': image_path,  # 确保路径能被Label Studio访问
            'text': text_description  #文本描述
        },
        'annotations': [{
            'result': []
        }]
    }
    
    # 处理每个标注框
    for _, row in group.iterrows():
        x_min = row['x_min']
        y_min = row['y_min']
        x_max = row['x_max']
        y_max = row['y_max']
        label = row['label']
        
        # 计算百分比坐标
        x = (x_min / img_width) * 100
        y = (y_min / img_height) * 100
        width = ((x_max - x_min) / img_width) * 100
        height = ((y_max - y_min) / img_height) * 100
        
        # 构建标注结果
        result_item = {
            'type': 'rectanglelabels',
            'value': {
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'rectanglelabels': [label]
            },
            'from_name': 'label',  # 必须与Label Studio配置匹配
            'to_name': 'image'
        }
        task['annotations'][0]['result'].append(result_item)
    
    tasks.append(task)

# 导入任务
if tasks:
    project.import_tasks(tasks)
    print(f"成功导入 {len(tasks)} 条多模态任务！")
else:
    print("没有任务可导入。")