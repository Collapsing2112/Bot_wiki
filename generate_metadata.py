import os
import json
import re
from markdown import Markdown

def unmark(text):
    """ 正确提取纯文本的版本 """
    # 创建 Markdown 转换器
    md = Markdown()
    # 转换 Markdown 到 HTML
    html_content = md.convert(text)
    # 去除 HTML 标签
    plain_text = re.sub(r'<[^>]+>', '', html_content)
    # 去除 Markdown 特殊字符（如**等）
    plain_text = re.sub(r'\*{2,}|_{2,}|`+', '', plain_text)
    # 合并多余空格和换行
    return re.sub(r'\s+', ' ', plain_text).strip()

articles = []
article_dir = "articles"

# 自动创建 articles 目录（如果不存在）
os.makedirs(article_dir, exist_ok=True)

# 获取已存在的 .md 文件列表
md_files = [f for f in os.listdir(article_dir) if f.endswith(".md")]

for idx, filename in enumerate(md_files, start=1):
    filepath = os.path.join(article_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
        # 尝试从内容第一行提取标题（# 标题）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else \
                os.path.splitext(filename)[0].replace("-", " ").title()
        
        # 生成内容预览
        plain_text = unmark(content)
        content_preview = plain_text[:200].rsplit(' ', 1)[0] + "..." \
                          if len(plain_text) > 200 else plain_text
        
        articles.append({
            "id": idx,
            "title": title,
            "file": filename,
            "contentPreview": content_preview
        })

# 保存元数据
with open(os.path.join(article_dir, "list.json"), "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"成功处理 {len(articles)} 篇文章：")
print("\n".join([f"{a['id']}. {a['title']}" for a in articles]))