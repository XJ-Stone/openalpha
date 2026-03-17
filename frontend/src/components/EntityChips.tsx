"use client";

import { useEffect, useState } from "react";
import { getEntities, EntitiesResponse } from "@/lib/api";

interface EntityChipsProps {
  onSelect: (query: string) => void;
}

function formatLabel(entity: { name: string; kind: string }): string {
  return entity.kind === "company"
    ? entity.name
    : entity.name
        .replace(/-/g, " ")
        .replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function EntityChips({ onSelect }: EntityChipsProps) {
  const [data, setData] = useState<EntitiesResponse | null>(null);
  const [tab, setTab] = useState<"companies" | "topics">("companies");

  useEffect(() => {
    getEntities().then(setData).catch(() => {});
  }, []);

  if (!data || (data.companies.length === 0 && data.topics.length === 0)) {
    return null;
  }

  const items = tab === "companies" ? data.companies : data.topics;

  return (
    <div>
      <div className="flex items-center justify-center gap-4 mb-4">
        <h3 className="text-[11px] font-semibold uppercase tracking-widest text-[var(--muted)]">
          Trending
        </h3>
        <div className="flex gap-0.5 bg-[var(--card)] rounded-lg p-0.5 border border-[var(--card-border)]">
          <button
            onClick={() => setTab("companies")}
            className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
              tab === "companies"
                ? "bg-[var(--background)] text-[var(--foreground)] shadow-sm"
                : "text-[var(--muted)] hover:text-[var(--foreground)]"
            }`}
          >
            Companies
          </button>
          <button
            onClick={() => setTab("topics")}
            className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
              tab === "topics"
                ? "bg-[var(--background)] text-[var(--foreground)] shadow-sm"
                : "text-[var(--muted)] hover:text-[var(--foreground)]"
            }`}
          >
            Topics
          </button>
        </div>
      </div>
      <div className="flex flex-wrap justify-center gap-2">
        {items.map((entity) => (
          <button
            key={entity.name}
            onClick={() =>
              onSelect(
                `What are investors saying about ${formatLabel(entity)}?`
              )
            }
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-[var(--card-border)] text-xs font-medium text-[var(--muted)] hover:border-[var(--accent)]/50 hover:text-[var(--accent)] hover:bg-[var(--accent)]/5 transition-all duration-150 cursor-pointer"
          >
            {formatLabel(entity)}
            <span className="text-[10px] opacity-50">{entity.score}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
