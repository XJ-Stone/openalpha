"use client";

import { useEffect, useState } from "react";
import { getEntities, EntitiesResponse } from "@/lib/api";

interface EntityDrawerProps {
  open: boolean;
  onClose: () => void;
  onSelect: (query: string) => void;
}

function formatLabel(entity: { name: string; kind: string }): string {
  return entity.kind === "company"
    ? entity.name
    : entity.name
        .replace(/-/g, " ")
        .replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function EntityDrawer({
  open,
  onClose,
  onSelect,
}: EntityDrawerProps) {
  const [data, setData] = useState<EntitiesResponse | null>(null);
  const [tab, setTab] = useState<"companies" | "topics">("companies");

  useEffect(() => {
    if (open && !data) {
      getEntities().then(setData).catch(() => {});
    }
  }, [open, data]);

  const items = data
    ? tab === "companies"
      ? data.companies
      : data.topics
    : [];

  return (
    <>
      {/* Backdrop */}
      {open && (
        <div
          className="fixed inset-0 bg-black/20 z-40 backdrop-blur-[2px]"
          onClick={onClose}
        />
      )}

      {/* Drawer */}
      <div
        className={`fixed top-0 right-0 h-full w-80 bg-[var(--background)] border-l border-[var(--card-border)] z-50 transform transition-transform duration-200 ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between p-4 border-b border-[var(--card-border)]">
          <h2 className="text-sm font-semibold text-[var(--foreground)]">
            Trending Topics
          </h2>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-[var(--card)] text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
          >
            <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
              <path
                fillRule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </div>

        <div className="p-4">
          {/* Tabs */}
          <div className="flex gap-0.5 bg-[var(--card)] rounded-lg p-0.5 border border-[var(--card-border)] mb-5">
            <button
              onClick={() => setTab("companies")}
              className={`flex-1 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                tab === "companies"
                  ? "bg-[var(--background)] text-[var(--foreground)] shadow-sm"
                  : "text-[var(--muted)] hover:text-[var(--foreground)]"
              }`}
            >
              Companies
            </button>
            <button
              onClick={() => setTab("topics")}
              className={`flex-1 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                tab === "topics"
                  ? "bg-[var(--background)] text-[var(--foreground)] shadow-sm"
                  : "text-[var(--muted)] hover:text-[var(--foreground)]"
              }`}
            >
              Topics
            </button>
          </div>

          {/* Chips */}
          {!data ? (
            <div className="flex justify-center py-8">
              <div className="w-5 h-5 border-2 border-[var(--muted)]/30 border-t-[var(--accent)] rounded-full animate-spin" />
            </div>
          ) : items.length === 0 ? (
            <p className="text-xs text-[var(--muted)] text-center py-8">
              No data available
            </p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {items.map((entity) => {
                const label = formatLabel(entity);
                return (
                  <button
                    key={entity.name}
                    onClick={() => {
                      onSelect(
                        `What are investors saying about ${label}?`
                      );
                      onClose();
                    }}
                    className="px-3 py-1.5 rounded-full border border-[var(--card-border)] text-xs font-medium text-[var(--muted)] hover:border-[var(--accent)]/50 hover:text-[var(--accent)] hover:bg-[var(--accent)]/5 transition-all duration-150 cursor-pointer"
                  >
                    {label}
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
