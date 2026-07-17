---
title: "2026 上半年学习总结：在 AI 浪潮中保持清醒"
date: 2026-07-17
updated: 2026-07-17
category: "学习"
tags: ["学习", "笔记"]
description: "回顾 2026 上半年在 Rust、分布式系统和 AI Agent 框架方面的学习历程，反思学习方法论。"
cover: ""
---

## 写在前面

2026 年上半年转瞬即逝。这半年我刻意减少了「信息消费」的时间（刷推、看文章），把更多精力投入到「知识生产」上——写代码、做项目、整理笔记。以下是这半年的学习总结。

## Rust：从入门到能写 CLI 工具

年初开始系统学习 Rust。选择 Rust 不是因为它是「最受喜爱的语言」，而是它的所有权系统和借用检查器逼迫你思考内存管理的本质。

学习路径大致是：

1. 《The Rust Programming Language》前 15 章精读
2. Rustlings 全部练习做完
3. 用 Clap 写一个 Markdown 到 HTML 的转换 CLI
4. 用 Axum 写了一个最小化的 REST API

下面是使用 Clap 构建 CLI 工具的基础模板：

```rust
use clap::Parser;

/// 一个简单的 Markdown 转 HTML 工具
#[derive(Parser)]
#[command(name = "md2html")]
#[command(version = "0.1.0")]
struct Cli {
    /// 输入 Markdown 文件路径
    input: String,

    /// 输出 HTML 文件路径
    #[arg(short = 'o', long = "output", default_value = "output.html")]
    output: String,
}

fn main() {
    let cli = Cli::parse();
    println!("转换 {} -> {}", cli.input, cli.output);
}
```

最大的收获不是学会了 Rust 的语法，而是开始用 Rust 的思维方式去审视所有语言的代码——**数据所有权是谁的？生命周期多久？会不会有数据竞争？**

## 分布式系统理论补课

花了一个半月时间重点学习了两个主题：

- **Raft 共识算法**：跟着 MIT 6.824 的 Lab 2 实现了 Raft 的核心逻辑。Leader Election、Log Replication、Snapshot 三段式读下来，对一致性问题有了实操层面的理解。
- **CAP 定理的工程实践**：理论上的 CAP 不可兼得，实践中往往是「牺牲一点点 C 换 A，或者牺牲一点点 A 换 C」。理解这个权衡比背诵定理更重要。

## AI Agent 框架调研

上半年花了不少时间研究 AI Agent 框架——LangChain、CrewAI、AutoGen 都跑了一遍。结论是：Agent 框架还处在非常早期的阶段，很多「自主决策」更像是精心编排的状态机。

真正有价值的是理解了 Agent 的核心抽象：**感知 → 规划 → 执行 → 反馈** 这个循环。无论框架怎么变，这个基本模式不会变。

## 方法论的反思

这半年最大的心得：**深度 > 广度**。以前我习惯「刷」——刷完一门课、刷完一本书，就觉得自己「学会了」。但现在我更愿意在一个问题上多停留几周，直到能用自己的话向别人解释清楚。

下半年计划在 Rust 上继续深入，同时把 AI Agent 的实践落地到一个具体的项目上。保持焦虑不如保持行动。
