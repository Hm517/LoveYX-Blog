---
title: "Astro SSG 入门指南：从零构建高性能静态博客"
date: 2026-07-12
updated: 2026-07-12
category: "编程"
tags: ["Astro", "SSG", "前端"]
description: "全面解析 Astro 静态站点生成器的核心概念、群岛架构与常用实践，含 TypeScript 代码示例。"
cover: ""
---

## 什么是 Static Site Generation

静态站点生成（SSG）的理念很简单：在构建阶段把所有页面预渲染成 HTML，部署时直接提供静态文件。没有服务器运行时，没有数据库查询，CDN 可以直接缓存所有内容。结果是极致的加载速度和极高的安全性。

但传统 SSG 有一个明显缺陷：**每增加一点交互性，就不得不引入大量 JavaScript**。比如一个评论系统或搜索框，往往需要把整个页面变成一个 SPA。

Astro 的解决方法就是 **Islands Architecture（群岛架构）**。

## Islands Architecture 详解

Astro 把页面分为两个区域：

- **静态海洋**：页面主体内容（文章、导航、页脚），构建时直接渲染为 HTML，客户端零 JS。
- **交互岛屿**：需要交互的部分（评论区、主题切换按钮、搜索框），各自独立加载 JavaScript。

这意味着你的博客文章页可能只有评论区那个 3KB 的脚本，文章正文完全是纯 HTML。

```typescript
// 示例：在 Astro 页面中引入交互式组件
---
// 顶部 frontmatter（服务端执行，不会发送到客户端）
import CommentSection from '../components/CommentSection';
import ThemeToggle from '../components/ThemeToggle.astro';
---
<article>
  <h1>{frontmatter.title}</h1>
  <!-- 纯静态内容 -->
  <Content />
</article>

<!-- 交互式岛屿：只在需要时才加载 JS -->
<CommentSection client:load />
<ThemeToggle client:idle />
```

## Content Collections：类型安全的 Markdown

Astro 的 Content Collections 功能是其杀手锏之一。通过 Zod schema 定义 frontmatter 结构，你可以在编辑器中获得自动补全，在构建时捕获元数据错误：

```typescript
import { getCollection } from 'astro:content';

// 获取所有博客文章，自动按日期排序
const posts = await getCollection('blog', ({ data }) => {
  return !data.draft;
});

// 按分类筛选
const aiPosts = posts.filter(
  post => post.data.category === 'AI'
);
```

## 路由与动态页面

Astro 的文件路由极其直观。`src/pages/blog/[slug].astro` 自动匹配 `/blog/hello-world/` 这样的路径：

```typescript
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---
<BlogLayout frontmatter={post.data}>
  <Content />
</BlogLayout>
```

## 性能优化建议

1. **图片优化**：使用 Astro 内置的 `<Image />` 组件自动生成 WebP/AVIF 格式
2. **Font Optimization**：通过 `@fontsource` 本地化字体，避免 Google Fonts 的额外请求
3. **Prefetch**：利用 `<link rel="prefetch">` 预加载可能的下一页
4. **View Transitions**：Astro 3.0+ 内置页面过渡动画，SPA 般丝滑

## 部署到 Cloudflare Pages

Astro 对 Cloudflare Pages 的支持近乎完美。连接 GitHub 仓库后，设置构建命令 `npm run build` 和输出目录 `dist`，每次推送自动部署。免费套餐包含无限带宽和全球 CDN，个人博客完全够用。

Astro 生态还在快速成长。如果你正在考虑搭建下一个静态站点，不妨试试 Astro——它可能会是你用过最愉快的 SSG 框架。
