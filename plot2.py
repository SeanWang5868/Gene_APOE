import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 读取数据文件
df = pd.read_csv('authors.APOE.csv')

# 填充缺失值
df["AuthorForename"] = df["AuthorForename"].fillna('')
df["AuthorLastname"] = df["AuthorLastname"].fillna('')

# 合并姓和名
df["FullName"] = df["AuthorForename"] + df["AuthorLastname"]

# 创建图
G = nx.Graph()

# 遍历每行数据，将有合作关系的作者之间连接起来
for _, row in df.iterrows():
    authors_in_row = row['FullName'].split(', ')
    for author1 in authors_in_row:
        for author2 in authors_in_row:
            if author1 != author2:
                if G.has_edge(author1, author2):
                    G[author1][author2]['weight'] += 1
                else:
                    G.add_edge(author1, author2, weight=1)

# 绘制图
plt.figure(figsize=(12, 12))

# 提取权重信息
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

# 使用 spring 布局绘制图
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
nx.draw_networkx_edges(G, pos, alpha=0.7, edge_color='gray', width=edge_weights)
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', font_weight='bold')

# 显示图
plt.show()
