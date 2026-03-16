"use client";

import { useState, FormEvent } from "react";

interface SearchBarProps {
  onSubmit: (question: string) => void;
  onStop?: () => void;
  isLoading?: boolean;
}

export default function SearchBar({ onSubmit, onStop, isLoading = false }: SearchBarProps) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const trimmed = query.trim();
    if (trimmed && !isLoading) {
      onSubmit(trimmed);
      setQuery("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative flex items-center">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about investors, companies, or sectors..."
          className="w-full px-4 py-3 pr-24 rounded-xl bg-[var(--card)] border border-[var(--card-border)] text-[var(--foreground)] placeholder-[var(--muted)] text-sm focus:outline-none focus:border-[var(--accent)] focus:ring-1 focus:ring-[var(--accent)] transition-colors"
          disabled={isLoading}
        />
        {isLoading ? (
          <button
            type="button"
            onClick={onStop}
            className="absolute right-2 p-2 rounded-lg bg-[var(--danger)] hover:bg-[var(--danger)]/80 text-white transition-colors"
            title="Stop generating"
          >
            <svg className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <rect x="5" y="5" width="10" height="10" rx="1" />
            </svg>
          </button>
        ) : (
          <button
            type="submit"
            disabled={!query.trim()}
            className="absolute right-2 p-2 rounded-lg bg-[var(--accent)] hover:bg-[var(--accent-hover)] disabled:opacity-40 disabled:cursor-not-allowed text-white transition-colors"
          >
            <svg className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
            </svg>
          </button>
        )}
      </div>
    </form>
  );
}
