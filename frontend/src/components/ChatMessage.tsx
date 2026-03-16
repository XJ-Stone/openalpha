"use client";

import { useState } from "react";
import ThinkingSteps, { StatusStep } from "./ThinkingSteps";
import ResponseStream, { Source } from "./ResponseStream";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  steps?: StatusStep[];
  sources?: Source[];
  isStreaming?: boolean;
  isThinking?: boolean;
}

interface ChatMessageProps {
  message: Message;
  onRetry?: () => void;
}

function ActionButtons({
  content,
  onRetry,
}: {
  content: string;
  onRetry?: () => void;
}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      const textarea = document.createElement("textarea");
      textarea.value = content;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({ text: content });
      } catch {
        // User cancelled
      }
    } else {
      // Fallback: copy to clipboard
      await handleCopy();
    }
  };

  return (
    <div className="flex items-center gap-1 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
      {/* Copy */}
      <button
        onClick={handleCopy}
        className="p-1.5 rounded-md hover:bg-[var(--card)] text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
        title={copied ? "Copied!" : "Copy"}
      >
        {copied ? (
          <svg className="w-3.5 h-3.5 text-[var(--success)]" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        ) : (
          <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M8 2a1 1 0 000 2h2a1 1 0 100-2H8z" />
            <path d="M3 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v6h-4.586l1.293-1.293a1 1 0 00-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L10.414 13H15v3a2 2 0 01-2 2H5a2 2 0 01-2-2V5zM15 11h2a1 1 0 110 2h-2v-2z" />
          </svg>
        )}
      </button>

      {/* Share */}
      <button
        onClick={handleShare}
        className="p-1.5 rounded-md hover:bg-[var(--card)] text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
        title="Share"
      >
        <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
          <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
        </svg>
      </button>

      {/* Retry */}
      {onRetry && (
        <button
          onClick={onRetry}
          className="p-1.5 rounded-md hover:bg-[var(--card)] text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
          title="Retry"
        >
          <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
          </svg>
        </button>
      )}
    </div>
  );
}

export default function ChatMessage({ message, onRetry }: ChatMessageProps) {
  if (message.role === "user") {
    return (
      <div className="flex justify-end mb-6">
        <div className="max-w-[80%] px-4 py-3 rounded-2xl rounded-br-sm bg-[var(--accent)] text-white text-sm leading-relaxed">
          {message.content}
        </div>
      </div>
    );
  }

  const isDone = !message.isStreaming && !message.isThinking && message.content;

  // Assistant message
  return (
    <div className="flex justify-start mb-6 group">
      <div className="max-w-[85%] min-w-0">
        {/* Thinking steps */}
        {message.steps && message.steps.length > 0 && (
          <ThinkingSteps
            steps={message.steps}
            isActive={message.isThinking ?? false}
          />
        )}

        {/* Streamed content */}
        {message.content && (
          <ResponseStream
            content={message.content}
            isStreaming={message.isStreaming ?? false}
            sources={message.sources}
          />
        )}

        {/* Thinking state with no content yet — show subtle indicator */}
        {!message.content && message.isThinking && (
          <div className="mt-1">
            <span className="inline-block w-2 h-5 bg-[var(--accent)] animate-pulse rounded-sm" />
          </div>
        )}

        {/* Action buttons — shown on hover when response is complete */}
        {isDone && <ActionButtons content={message.content} onRetry={onRetry} />}
      </div>
    </div>
  );
}
