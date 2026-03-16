"use client";

export interface Source {
  index: number;
  investor: string;
  date: string;
  source: string;
  url: string;
  title?: string;
}

interface ResponseStreamProps {
  content: string;
  isStreaming?: boolean;
  sources?: Source[];
}

/**
 * Renders streaming markdown response with citation support.
 */
export default function ResponseStream({
  content,
  isStreaming = false,
  sources = [],
}: ResponseStreamProps) {
  if (!content) return null;

  const renderMarkdown = (text: string): string => {
    let html = text
      // Escape HTML
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      // Headings
      .replace(/^### (.+)$/gm, '<h3 class="text-base font-semibold text-[var(--foreground)] mt-3 mb-1">$1</h3>')
      .replace(/^## (.+)$/gm, '<h2 class="text-lg font-bold text-[var(--foreground)] mt-4 mb-1">$1</h2>')
      .replace(/^# (.+)$/gm, '<h1 class="text-xl font-bold text-[var(--foreground)] mt-4 mb-2">$1</h1>')
      // Bold and italic
      .replace(/\*\*(.+?)\*\*/g, '<strong class="text-[var(--foreground)] font-semibold">$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      // Inline code
      .replace(/`([^`]+)`/g, '<code class="px-1 py-0.5 rounded bg-[var(--card)] text-xs font-mono">$1</code>')
      // Citation markers [1], [2] etc. — make them clickable
      .replace(/\[(\d+)\]/g, (_match, num) => {
        const src = sources.find((s) => s.index === parseInt(num));
        if (src?.url) {
          return `<a href="${src.url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center justify-center w-4 h-4 text-[10px] rounded bg-[var(--accent)]/20 text-[var(--accent)] hover:bg-[var(--accent)]/30 no-underline align-super ml-0.5" title="${src.investor} — ${src.source} (${src.date})">${num}</a>`;
        }
        return `<sup class="text-[10px] text-[var(--accent)] ml-0.5">[${num}]</sup>`;
      })
      // Bullet lists
      .replace(/^- (.+)$/gm, '<li class="ml-4 list-disc">$1</li>')
      // Paragraphs: double newlines become paragraph breaks
      .replace(/\n\n/g, '</p><p class="mt-2">')
      // Single newlines within a paragraph
      .replace(/\n/g, "<br/>");

    // Wrap in paragraph tags
    html = `<p>${html}</p>`;

    // Wrap consecutive <li> elements in <ul>
    html = html.replace(
      /(<li[^>]*>.*?<\/li>(?:<br\/?>)?)+/g,
      (match) =>
        `<ul class="space-y-0.5 my-2">${match.replace(/<br\/?>/g, "")}</ul>`
    );

    // Clean up stray <br/> right before or after block elements
    html = html.replace(/<br\/?>\s*(<\/?(h[1-3]|ul|li|div))/g, "$1");
    html = html.replace(/(<\/(?:h[1-3]|ul|li|div)>)\s*<br\/?>/g, "$1");

    // Clean up empty paragraphs (including those with only whitespace or <br/>)
    html = html.replace(/<p[^>]*>(\s|<br\/?>)*<\/p>/g, "");

    return html;
  };

  return (
    <div className="w-full">
      <div
        className="max-w-none text-[var(--foreground)]/90 text-sm leading-relaxed [&_p]:my-0"
        dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
      />
      {isStreaming && (
        <span className="inline-block w-1.5 h-4 bg-[var(--accent)] ml-0.5 animate-pulse rounded-sm" />
      )}
      {/* Source list at the bottom */}
      {!isStreaming && sources.length > 0 && (
        <div className="mt-4 pt-3 border-t border-[var(--card-border)]">
          <p className="text-xs text-[var(--muted)] mb-2">Sources</p>
          <div className="flex flex-col gap-1">
            {sources.map((src) => (
              <a
                key={src.index}
                href={src.url || "#"}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-baseline gap-2 text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-colors group"
              >
                <span className="inline-flex items-center justify-center w-4 h-4 rounded bg-[var(--accent)]/20 text-[var(--accent)] text-[10px] flex-shrink-0">
                  {src.index}
                </span>
                <span>
                  {src.investor} — {src.source}
                  {src.date && ` (${src.date})`}
                </span>
                {src.url && (
                  <svg className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                    <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
                  </svg>
                )}
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
