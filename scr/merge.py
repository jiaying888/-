import pandas as pd

# 读取两个CSV文件
df1 = pd.read_csv("clean_data/image_descriptions.csv")

df1.loc[: , 'image']= df1['image_path']    #新增image列
df1.loc[: , 'text']= df1['description']    #新增text列

df2 = pd.read_csv("clean_data/pre_labels.csv")


# 合并数据，保留df2中的所有行
merged_df = pd.merge(df2, df1, on='image', how='left')

# 调整列顺序
merged_df = merged_df[['image', 'text', 'label', 'x_min', 'y_min', 'x_max', 'y_max']]

# 保存结果到3.csv
merged_df.to_csv('clean_data/multimodal_labels.csv', index=False)  