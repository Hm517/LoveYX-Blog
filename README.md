# LoveYX Blog

记录技术、AI、生活与思考的个人博客。基于 Astro 构建，全站静态生成（SSG），部署于 Cloudflare Pages。

## 技术栈

- **框架**：Astro 5.x
- **语言**：TypeScript
- **样式**：Tailwind CSS
- **内容**：Markdown + MDX
- **代码高亮**：Shiki
- **数学公式**：KaTeX（remark-math + rehype-katex）
- **评论**：Giscus
- **分析**：Cloudflare Web Analytics
- **部署**：Cloudflare Pages
- **字体**：Inter / JetBrains Mono / Noto Sans SC

## 项目结构

```
LoveYX-Blog/
├── public/
│   ├── favicon.svg            # 网站图标
│   ├── images/                # 静态图片资源
│   └── robots.txt             # 搜索引擎爬虫规则
├── src/
│   ├── components/            # 可复用组件
│   ├── content/
│   │   ├── blog/              # 博客文章（Markdown/MDX）
│   │   └── config.ts          # 内容集合定义（Zod Schema）
│   ├── layouts/
│   │   ├── BaseLayout.astro   # 基础布局（SEO、主题切换、Analytics）
│   │   └── BlogLayout.astro   # 博客文章布局（TOC、评论、导航）
│   ├── pages/                 # 路由页面
│   ├── styles/
│   │   └── global.css         # 全局样式 + Tailwind 指令
│   └── env.d.ts               # TypeScript 类型声明
├── astro.config.mjs           # Astro 配置
├── tailwind.config.mjs        # Tailwind 配置
├── tsconfig.json              # TypeScript 配置
└── package.json
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 本地开发

```bash
npm run dev
```

浏览器访问 `http://localhost:4321` 即可预览。

### 构建生产版本

```bash
npm run build
```

输出到 `dist/` 目录。

### 预览生产版本

```bash
npm run preview
```

## Cloudflare Pages 部署步骤

### 第一步：将代码推送到 GitHub

在 GitHub 上创建一个新仓库（如 `loveyx-blog`），然后将项目代码推送上去：

```bash
git init
git add .
git commit -m "init: LoveYX Blog"
git remote add origin https://github.com/你的用户名/loveyx-blog.git
git push -u origin main
```

### 第二步：登录 Cloudflare Dashboard

访问 [Cloudflare Dashboard](https://dash.cloudflare.com/)，登录或注册账号。

### 第三步：创建 Pages 项目

1. 点击左侧菜单 **Workers & Pages**
2. 点击 **Create** → **Pages** → **Connect to Git**
3. 授权 Cloudflare 访问你的 GitHub 账号
4. 选择 `loveyx-blog` 仓库

### 第四步：配置构建设置

- **Framework preset**：选择 `Astro`
- **Build command**：`npm run build`
- **Build output directory**：`dist`
- 点击 **Save and Deploy**

### 第五步：等待部署完成

Cloudflare 会自动执行 `npm install` → `npm run build`，部署完成后会生成一个 `*.pages.dev` 的临时域名，通过该域名即可访问你的博客。后续每次推送代码到 `main` 分支都会自动触发重新部署。

## 绑定 loveyx.fun 域名

### 前提条件

确保你已经拥有 `loveyx.fun` 域名，且域名的 DNS 托管在 Cloudflare 上。

### 步骤一：进入 Pages 项目设置

在 Cloudflare Dashboard → Workers & Pages → 选择你的 `loveyx-blog` 项目 → 点击 **Custom domains** 选项卡。

### 步骤二：添加自定义域名

点击 **Set up a custom domain**，输入 `loveyx.fun`，点击 **Continue**。

### 步骤三：激活域名

Cloudflare 会自动配置 DNS 记录（CNAME 指向 `*.pages.dev`）。点击 **Activate domain** 完成绑定。

### 步骤四：等待 DNS 生效

DNS 生效通常需要几分钟到几小时。生效后通过 `https://loveyx.fun` 即可访问。

### 步骤五：配置 www 子域名（可选）

重复上述步骤，添加 `www.loveyx.fun`，Cloudflare 会自动设置从根域名到 `www` 的重定向。

## 发布新文章

1. 在 `src/content/blog/` 目录下新建 `.md` 文件
2. 按照以下 frontmatter 格式填写文章元数据：

```yaml
---
title: "文章标题"
date: 2026-07-17
updated: 2026-07-17
category: "分类名"
tags: ["标签1", "标签2"]
description: "简短描述"
cover: ""
---
```

3. 在 frontmatter 下方用 Markdown 撰写正文
4. 保存文件，推送到 GitHub：

```bash
git add src/content/blog/你的文章.md
git commit -m "post: 你的文章标题"
git push
```

5. Cloudflare Pages 会自动检测到推送并重新部署，约 1-2 分钟后新文章即可上线。

## 许可证

MIT
