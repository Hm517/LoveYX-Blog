/**
 * 博客文章 Frontmatter 类型定义
 */
export interface BlogFrontmatter {
  title: string;
  date: string; // ISO 日期字符串 YYYY-MM-DD
  updated?: string;
  tags: string[];
  category: string;
  cover?: string;
  description?: string;
  draft?: boolean;
}

/**
 * 博客文章完整元数据（含 Astro 注入字段）
 */
export interface BlogPost {
  id: string;
  slug: string;
  body: string;
  collection: string;
  data: BlogFrontmatter;
  render: () => Promise<{ Content: any; headings: Heading[] }>;
}

/**
 * Markdown 标题信息
 */
export interface Heading {
  depth: number;
  text: string;
  slug: string;
}

/**
 * 分类统计
 */
export interface CategoryInfo {
  name: string;
  count: number;
}

/**
 * 标签统计
 */
export interface TagInfo {
  name: string;
  count: number;
}

/**
 * 搜索索引条目
 */
export interface SearchIndexEntry {
  slug: string;
  title: string;
  description: string;
  category: string;
  tags: string[];
  date: string;
  body: string;
}
