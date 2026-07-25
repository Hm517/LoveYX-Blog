#!/usr/bin/env python3
"""
LoveYX Blog - 快速发布脚本

用法：
    python publish.py "文章标题" "分类" "标签1,标签2"
    
    然后输入 Markdown 正文（Ctrl+Z 然后回车结束，或管道传入）。

示例：
    echo "# 你好" | python publish.py "我的新文章" "生活" "日常,碎碎念"
"""

import sys
import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

def slugify(title):
    """把中文标题转成安全的文件名（取拼音首字母 + 日期）"""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'[-\s]+', '-', safe).strip('-')
    if not safe or any('\u4e00' <= c <= '\u9fff' for c in safe):
        # Contains Chinese, use date-based fallback
        safe = datetime.now().strftime("post-%Y%m%d")
    return safe.lower()

def markdown_to_html(md_text):
    """Simple Markdown to HTML converter for blog posts."""
    lines = md_text.strip().split('\n')
    result = []
    in_code_block = False
    code_lines = []
    in_list = False
    list_type = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                lang = code_lines[0].strip() if code_lines else ''
                code_content = '\n'.join(code_lines[1:] if code_lines[0].strip() else code_lines)
                # Escape HTML entities
                code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                result.append(f'<pre><code>{code_content}</code></pre>')
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
                code_lines.append(line.strip()[3:])  # Store language hint
            i += 1
            continue
        
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
        
        stripped = line.strip()
        
        # Close list
        if not stripped.startswith(('- ', '* ', '+ ', '1. ', '2. ', '3. ')) and in_list:
            result.append('</ul>' if list_type == 'ul' else '</ol>')
            in_list = False
            list_type = None
        
        # Headings
        if stripped.startswith('### '):
            result.append(f'<h3>{stripped[4:]}</h3>')
        elif stripped.startswith('## '):
            result.append(f'<h2>{stripped[2:]}</h2>')
        elif stripped.startswith('# '):
            result.append(f'<h2>{stripped[2:]}</h2>')
        # Unordered list
        elif stripped.startswith(('- ', '* ', '+ ')):
            if not in_list:
                result.append('<ul>')
                in_list = True
                list_type = 'ul'
            result.append(f'<li>{stripped[2:]}</li>')
        # Ordered list
        elif re.match(r'^\d+\.\s', stripped):
            if not in_list:
                result.append('<ol>')
                in_list = True
                list_type = 'ol'
            result.append(f'<li>{re.sub(r"^\d+\.\s", "", stripped)}</li>')
        # Empty line
        elif not stripped:
            result.append('')
        # Regular paragraph
        else:
            # Bold
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
            # Italic
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            # Inline code
            text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
            result.append(f'<p>{text}</p>')
        
        i += 1
    
    if in_list:
        result.append('</ul>' if list_type == 'ul' else '</ol>')
    
    return '\n'.join(result)


def generate_article(title, category, tags, date_str, html_body):
    """Generate HTML from template."""
    tags_html = ''.join(f'<span class="tag">{t.strip()}</span>' for t in tags)
    
    # Read template
    template_path = os.path.join(BASE_DIR, "new-post.html")
    if not os.path.exists(template_path):
        print(f"错误：找不到模板文件 {template_path}")
        sys.exit(1)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace placeholders
    template = template.replace(
        '<title>文章标题 — LoveYX Blog</title>',
        f'<title>{title} — LoveYX Blog</title>'
    )
    template = template.replace(
        '<meta name="description" content="文章简介，用于SEO和社交媒体分享">',
        f'<meta name="description" content="{title}">'
    )
    template = template.replace(
        '<div class="category-badge">分类名称</div>',
        f'<div class="category-badge">{category}</div>'
    )
    template = template.replace(
        '<h1>文章标题</h1>',
        f'<h1>{title}</h1>'
    )
    template = template.replace(
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>2026-07-25',
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>{date_str}'
    )
    template = template.replace(
        '<span>分类名称</span>',
        f'<span>{category}</span>'
    )
    template = template.replace(
        '<span class="tag">标签1</span>\n            <span class="tag">标签2</span>',
        tags_html
    )
    
    # Replace body content
    # Find the article-content div and replace its inner HTML
    content_start = template.find('<div class="article-content">')
    content_end = template.find('</div>\n      </article>')
    if content_start != -1 and content_end != -1:
        content_start += len('<div class="article-content">\n')
        template = template[:content_start] + '\n' + html_body + '\n        ' + template[content_end:]
    
    return template


def insert_card_into_index(title, category, tags, date_str, filename):
    """Insert a new card at the top of index.html card grid."""
    if not os.path.exists(INDEX_PATH):
        print(f"警告：找不到 {INDEX_PATH}，请手动添加首页卡片")
        return
    
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    tags_html = ''.join(f'<span class="card-tag">{t.strip()}</span>' for t in tags)
    
    card_html = (
        '          <a href="' + filename + '" class="card">\n'
        '            <div class="card-category">' + category + '</div>\n'
        '            <h3>' + title + '</h3>\n'
        '            <p>' + title + '</p>\n'
        '            <div class="card-meta">\n'
        '              <span><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>' + date_str + '</span>\n'
        '              <span><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>5 分钟</span>\n'
        '            </div>\n'
        '            <div class="card-tags">' + tags_html + '</div>\n'
        '          </a>\n'
    )
    
    # Find card-grid and insert after the opening div
    marker = '<div class="card-grid">'
    marker_pos = index_content.find(marker)
    if marker_pos != -1:
        insert_pos = marker_pos + len(marker) + 1  # +1 for newline
        index_content = index_content[:insert_pos] + card_html + index_content[insert_pos:]
        with open(INDEX_PATH, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"已在 index.html 添加文章卡片")
    else:
        print("警告：未找到 card-grid，请手动在 index.html 中添加文章卡片")


def main():
    if len(sys.argv) < 3:
        print('用法：python publish.py "文章标题" "分类" "标签1,标签2"')
        print('然后输入 Markdown 正文（Ctrl+Z 回车结束，或管道传入）')
        sys.exit(1)
    
    title = sys.argv[1]
    category = sys.argv[2]
    tags = sys.argv[3].split(',') if len(sys.argv) > 3 else []
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Read Markdown from stdin
    print("请输入 Markdown 正文（输入完成后按 Ctrl+Z 然后回车）：")
    md_lines = sys.stdin.read()
    
    if not md_lines.strip():
        print("错误：未接收到正文内容")
        sys.exit(1)
    
    # Convert Markdown to HTML
    html_body = markdown_to_html(md_lines)
    
    # Generate article
    article_html = generate_article(title, category, tags, date_str, html_body)
    
    # Write file
    filename = slugify(title) + ".html"
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article_html)
    
    print(f"\n已生成文章：{filepath}")
    
    # Insert card into index
    insert_card_into_index(title, category, tags, date_str, filename)
    
    print(f"\n下一步：")
    print(f"  1. 检查 {filename} 的内容")
    print(f"  2. 在浏览器中打开 index.html 预览")
    print(f"  3. git add -A && git commit -m '新文章：{title}' && git push")


if __name__ == "__main__":
    main()
