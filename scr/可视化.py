import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# 1. 读取数据
# ======================
df = pd.read_csv("clean_data/annotations.csv")  # 替换为你的CSV路径

# ======================
# 中文显示配置
# ======================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False


# ======================
#可视化看板
# ======================
plt.figure(figsize=(15, 5))
# ----------------------
# 图表：文本分类分布
# ----------------------
plt.subplot(1, 3, 3)
df['text_type'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title('文本分类分布')

plt.tight_layout()
plt.show()