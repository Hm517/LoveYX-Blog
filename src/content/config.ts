import { defineCollection, z } from "astro:content";

/**
 * Blog 内容集合定义
 *
 * Frontmatter schema:
 * - title: 文章标题（必填）
 * - date: 发布日期（必填）
 * - updated: 最后更新日期（可选）
 * - tags: 标签列表（可选）
 * - category: 分类（可选）
 * - cover: 封面图路径（可选）
 * - description: 文章摘要/描述（可选，不填则自动截取正文前段）
 * - draft: 草稿标记（可选，true 时开发模式可见，构建时排除）
 */
const blogCollection = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    tags: z.array(z.string()).optional().default([]),
    category: z.string().optional(),
    cover: z.string().optional(),
    description: z.string().optional(),
    draft: z.boolean().optional().default(false),
  }),
});

export const collections = {
  blog: blogCollection,
};
