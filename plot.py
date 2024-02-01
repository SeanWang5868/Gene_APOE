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

# 删选出第一作者和最后一名作者的数据
first_authors = df[df['AuthorN'] == 1]
last_authors = df[df['AuthorN'] == df.groupby('PMID')['AuthorN'].transform('max')]

# 统计每位作者作为第一作者和最后一名作者发表的文章数量
first_author_counts = first_authors.groupby('FullName').size()
last_author_counts = last_authors.groupby('FullName').size()

# 通过 reset_index() 重置索引，以确保长度一致
total_counts = pd.concat([first_author_counts, last_author_counts], axis=1, keys=['FirstAuthorCounts', 'LastAuthorCounts']).fillna(0).reset_index()

# 计算第四列的值
total_counts['TotalCounts'] = total_counts['FirstAuthorCounts'] + total_counts['LastAuthorCounts']

# 创建包含结果的新 DataFrame
result_df = pd.DataFrame({
    'FullName': total_counts['FullName'],
    'FirstAuthorCounts': total_counts['FirstAuthorCounts'],
    'LastAuthorCounts': total_counts['LastAuthorCounts'],
    'TotalCounts': total_counts['TotalCounts']
})

# 按照 'TotalCounts' 列从大到小排序
result_df_sorted = result_df.sort_values(by='TotalCounts', ascending=False)

# 打印排序后的结果
print(result_df_sorted.head(20))

# 删选出前20个人的数据
top_20_names = result_df_sorted.head(20)['FullName']
selected_authors = df[df['FullName'].isin(top_20_names)]

# 创建图
G = nx.Graph()

# 遍历每行数据，将有合作关系的作者之间连接起来
for _, row in selected_authors.iterrows():
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
