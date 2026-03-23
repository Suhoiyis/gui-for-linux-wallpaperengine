// src/lib/markdown.tsx
// 轻量级行内 Markdown 渲染器，专为壁纸名称等短文本设计
// 支持：***粗斜体***、**粗体**、*斜体*、`代码`、~~删除线~~、[链接](url)

import React from "react";

/**
 * 将包含行内 Markdown 语法的字符串转换为 React 节点
 * 若文本不包含任何 Markdown 语法，直接返回原始字符串（零开销）
 */
export function renderInlineMarkdown(text: string): React.ReactNode {
  // 快速路径：如果没有任何可能的 Markdown 标记，直接返回纯文本
  if (!/[*`~\[]/.test(text)) {
    return text;
  }

  // 按优先级从高到低匹配行内语法
  // 粗斜体必须在粗体和斜体之前匹配
  const inlinePattern =
    /(\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`|~~(.+?)~~|\[([^\]]+)\]\(([^)]+)\))/g;

  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  let match: RegExpExecArray | null;
  let key = 0;

  while ((match = inlinePattern.exec(text)) !== null) {
    // 添加匹配之前的纯文本
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index));
    }

    if (match[2]) {
      // ***粗斜体***
      parts.push(
        <strong key={key++}>
          <em>{match[2]}</em>
        </strong>,
      );
    } else if (match[3]) {
      // **粗体**
      parts.push(<strong key={key++}>{match[3]}</strong>);
    } else if (match[4]) {
      // *斜体*
      parts.push(<em key={key++}>{match[4]}</em>);
    } else if (match[5]) {
      // `代码`
      parts.push(
        <code
          key={key++}
          className="px-1 py-0.5 rounded bg-muted text-[0.85em] font-mono"
        >
          {match[5]}
        </code>,
      );
    } else if (match[6]) {
      // ~~删除线~~
      parts.push(<del key={key++}>{match[6]}</del>);
    } else if (match[7] && match[8]) {
      // [链接](url)
      parts.push(
        <a
          key={key++}
          href={match[8]}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary underline underline-offset-2 hover:text-primary/80"
          onClick={(e) => e.stopPropagation()}
        >
          {match[7]}
        </a>,
      );
    }

    lastIndex = match.index + match[0].length;
  }

  // 添加剩余的纯文本
  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex));
  }

  // 如果没有匹配到任何 Markdown（不太可能走到这里，但防御性编程）
  if (parts.length === 0) {
    return text;
  }

  return <>{parts}</>;
}
