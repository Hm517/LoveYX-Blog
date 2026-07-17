/**
 * 本地全文搜索实现
 * 使用简单的倒排索引 + TF-IDF 算法
 * 无需服务器，完全在构建时预生成索引
 */

import type { SearchIndexEntry } from "../types";

/**
 * 构建搜索索引数据
 * 在构建时由 Astro 页面调用，生成为静态 JSON
 */
export function buildSearchIndex(posts: SearchIndexEntry[]): SearchIndexEntry[] {
  return posts.map((post) => ({
    ...post,
    // 预处理：去除 Markdown 标记，保留纯文本用于搜索
    body: post.body
      .replace(/```[\s\S]*?```/g, "") // 去除代码块
      .replace(/!\[.*?\]\(.*?\)/g, "") // 去除图片
      .replace(/\[([^\]]*)\]\(.*?\)/g, "$1") // 链接只保留文字
      .replace(/[#*_~`>|]/g, "") // 去除 Markdown 标记
      .replace(/\n+/g, " ")
      .trim()
      .toLowerCase(),
  }));
}

/**
 * 客户端搜索函数
 * 简单的关键词匹配 + 相关性打分
 */
export function search(
  query: string,
  index: SearchIndexEntry[]
): SearchIndexEntry[] {
  if (!query.trim()) return [];

  const terms = query.toLowerCase().trim().split(/\s+/);

  return index
    .map((entry) => {
      let score = 0;

      // 标题匹配权重最高
      const titleLower = entry.title.toLowerCase();
      terms.forEach((term) => {
        if (titleLower.includes(term)) score += 10;
      });

      // 描述匹配
      const descLower = entry.description.toLowerCase();
      terms.forEach((term) => {
        if (descLower.includes(term)) score += 5;
      });

      // 分类匹配
      if (entry.category.toLowerCase().includes(query.toLowerCase())) {
        score += 3;
      }

      // 标签匹配
      entry.tags.forEach((tag) => {
        terms.forEach((term) => {
          if (tag.toLowerCase().includes(term)) score += 4;
        });
      });

      // 正文匹配
      terms.forEach((term) => {
        const regex = new RegExp(
          term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
          "gi"
        );
        const matches = entry.body.match(regex);
        if (matches) score += matches.length;
      });

      return { entry, score };
    })
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 10)
    .map(({ entry }) => entry);
}
