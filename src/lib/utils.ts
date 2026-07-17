/**
 * 通用工具函数
 */

/**
 * 格式化日期为中文可读格式
 * @param dateStr ISO 日期字符串
 * @param locale 区域设置，默认 zh-CN
 */
export function formatDate(dateStr: string, locale: string = "zh-CN"): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString(locale, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

/**
 * 计算阅读时间（分钟）
 * 中文约 300 字/分钟，英文约 200 词/分钟
 * @param content Markdown 文本内容
 */
export function getReadingTime(content: string): number {
  // 统计中文字符数
  const chineseChars = (content.match(/[\u4e00-\u9fff]/g) || []).length;
  // 统计英文单词数（去除非 ASCII 后按空格分割）
  const englishText = content.replace(/[\u4e00-\u9fff]/g, " ");
  const englishWords = englishText
    .split(/\s+/)
    .filter((w) => w.length > 0).length;

  // 中文 300 字/分钟，英文 200 词/分钟
  const chineseTime = chineseChars / 300;
  const englishTime = englishWords / 200;
  const totalTime = chineseTime + englishTime;

  // 至少 1 分钟
  return Math.max(1, Math.ceil(totalTime));
}

/**
 * 按日期降序排列博客文章
 */
export function sortPostsByDate<T extends { data: { date: string } }>(
  posts: T[]
): T[] {
  return [...posts].sort(
    (a, b) =>
      new Date(b.data.date).getTime() - new Date(a.data.date).getTime()
  );
}

/**
 * 过滤草稿文章
 */
export function filterPublishedPosts<T extends { data: { draft?: boolean } }>(
  posts: T[]
): T[] {
  return posts.filter((post) => !post.data.draft);
}

/**
 * 获取唯一分类列表及计数
 */
export function getCategories<T extends { data: { category: string } }>(
  posts: T[]
): { name: string; count: number }[] {
  const map = new Map<string, number>();
  posts.forEach((p) => {
    const cat = p.data.category;
    map.set(cat, (map.get(cat) || 0) + 1);
  });
  return Array.from(map.entries())
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count);
}

/**
 * 获取唯一标签列表及计数
 */
export function getTags<T extends { data: { tags: string[] } }>(
  posts: T[]
): { name: string; count: number }[] {
  const map = new Map<string, number>();
  posts.forEach((p) => {
    p.data.tags.forEach((tag) => {
      map.set(tag, (map.get(tag) || 0) + 1);
    });
  });
  return Array.from(map.entries())
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count);
}

/**
 * 获取所有年份列表（用于归档）
 */
export function getYears<T extends { data: { date: string } }>(
  posts: T[]
): number[] {
  const years = new Set<number>();
  posts.forEach((p) => {
    years.add(new Date(p.data.date).getFullYear());
  });
  return Array.from(years).sort((a, b) => b - a);
}

/**
 * 按年份分组博客文章
 */
export function groupPostsByYear<T extends { data: { date: string } }>(
  posts: T[]
): Map<number, T[]> {
  const map = new Map<number, T[]>();
  posts.forEach((post) => {
    const year = new Date(post.data.date).getFullYear();
    if (!map.has(year)) {
      map.set(year, []);
    }
    map.get(year)!.push(post);
  });
  return map;
}

/**
 * 生成文章摘要（截取前 N 个字符）
 */
export function generateExcerpt(
  content: string,
  maxLength: number = 150
): string {
  // 去除 Markdown 语法标记
  const plainText = content
    .replace(/^#{1,6}\s+/gm, "")
    .replace(/[*_~`>#\[\]()|]/g, "")
    .replace(/!\[.*?\]\(.*?\)/g, "")
    .replace(/\[([^\]]*)\]\(.*?\)/g, "$1")
    .replace(/\n+/g, " ")
    .trim();

  if (plainText.length <= maxLength) return plainText;
  return plainText.slice(0, maxLength).trimEnd() + "...";
}

/**
 * Slugify：将字符串转为 URL 友好格式
 */
export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^\w-]+/g, "")
    .replace(/--+/g, "-")
    .replace(/^-+|-+$/g, "");
}

/**
 * 判断是否为外部链接
 */
export function isExternalLink(url: string): boolean {
  return /^https?:\/\//.test(url);
}
