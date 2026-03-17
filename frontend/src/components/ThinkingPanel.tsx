"use client";

import { useEffect, useRef, useState } from "react";
import { StatusStep } from "./ThinkingSteps";

interface ThinkingPanelProps {
  steps: StatusStep[];
  isActive: boolean;
  savedDuration?: number;
  onClose: () => void;
}

const PHASE_LABELS: Record<string, string> = {
  extract: "Analyzing question",
  search: "Searching knowledge base",
  map: "Reading appearances",
  reduce: "Synthesizing answer",
};

const PHASE_ICONS: Record<string, string> = {
  extract: "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
  search: "M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z",
  map: "M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z",
  reduce: "M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z",
};

export default function ThinkingPanel({ steps, isActive, savedDuration, onClose }: ThinkingPanelProps) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const startTime = useRef<number>(Date.now());
  const [elapsed, setElapsed] = useState(savedDuration ?? 0);

  useEffect(() => {
    if (savedDuration !== undefined) {
      setElapsed(savedDuration);
    }
  }, [savedDuration]);

  useEffect(() => {
    if (steps.length === 1 && savedDuration === undefined) {
      startTime.current = Date.now();
      setElapsed(0);
    }
  }, [steps.length, savedDuration]);

  useEffect(() => {
    if (savedDuration !== undefined) return;
    if (!isActive) {
      setElapsed(Math.round((Date.now() - startTime.current) / 1000));
      return;
    }
    const interval = setInterval(() => {
      setElapsed(Math.round((Date.now() - startTime.current) / 1000));
    }, 1000);
    return () => clearInterval(interval);
  }, [isActive, savedDuration]);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [steps.length]);

  const elapsedLabel =
    elapsed >= 60
      ? `${Math.floor(elapsed / 60)}m ${elapsed % 60}s`
      : `${elapsed}s`;

  // Group consecutive steps by phase
  const groupedSteps = steps.reduce<
    { phase: string; items: StatusStep[] }[]
  >((acc, step) => {
    const last = acc[acc.length - 1];
    if (last && last.phase === step.phase) {
      last.items.push(step);
    } else {
      acc.push({ phase: step.phase, items: [step] });
    }
    return acc;
  }, []);

  return (
    <div className="h-full flex flex-col border-l border-[var(--card-border)] bg-[var(--background)]">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-[var(--card-border)] flex-shrink-0">
        <div className="flex items-center gap-3">
          {isActive ? (
            <div className="relative flex items-center justify-center w-5 h-5">
              <span className="absolute w-5 h-5 rounded-full bg-[var(--accent)]/20 animate-ping" />
              <span className="relative w-2 h-2 rounded-full bg-[var(--accent)]" />
            </div>
          ) : (
            <svg className="w-4 h-4 text-[var(--success)]" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          )}
          <div>
            <h2 className="text-sm font-semibold text-[var(--foreground)]">
              {isActive ? "Thinking..." : "Thought process"}
            </h2>
            <p className="text-xs text-[var(--muted)]">
              {elapsed > 0 ? elapsedLabel : ""}
            </p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg hover:bg-[var(--card)] text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
        >
          <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      {/* Timeline */}
      <div className="flex-1 overflow-y-auto px-5 py-4">
        {groupedSteps.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-[var(--muted)]">
            <div className="w-8 h-8 border-2 border-[var(--muted)]/20 border-t-[var(--accent)] rounded-full animate-spin mb-3" />
            <p className="text-xs">Starting analysis...</p>
          </div>
        ) : (
          <div className="relative">
            {groupedSteps.map((group, gIdx) => {
              const isLastGroup = gIdx === groupedSteps.length - 1;
              const isGroupActive = isLastGroup && isActive;
              const phaseLabel = PHASE_LABELS[group.phase] || group.phase;
              const iconPath = PHASE_ICONS[group.phase];
              const lastItem = group.items[group.items.length - 1];

              return (
                <div key={gIdx} className="relative pl-7 pb-6 last:pb-0">
                  {/* Connecting line */}
                  {!isLastGroup && (
                    <div className="absolute left-[5px] top-[14px] bottom-0 w-px bg-[var(--card-border)]" />
                  )}

                  {/* Dot */}
                  <div className="absolute left-0 top-1 w-[11px] h-[11px] flex items-center justify-center">
                    {isGroupActive ? (
                      <span className="relative flex items-center justify-center">
                        <span className="absolute w-[11px] h-[11px] rounded-full bg-[var(--accent)]/30 animate-ping" />
                        <span className="w-[7px] h-[7px] rounded-full bg-[var(--accent)]" />
                      </span>
                    ) : (
                      <span className="w-[7px] h-[7px] rounded-full bg-[var(--success)]" />
                    )}
                  </div>

                  {/* Phase header */}
                  <div className="flex items-center gap-2 mb-1.5">
                    {iconPath && (
                      <svg
                        className={`w-3.5 h-3.5 ${isGroupActive ? "text-[var(--accent)]" : "text-[var(--muted)]"}`}
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d={iconPath} />
                      </svg>
                    )}
                    <span
                      className={`text-xs font-semibold uppercase tracking-wider ${
                        isGroupActive ? "text-[var(--accent)]" : "text-[var(--foreground)]"
                      }`}
                    >
                      {phaseLabel}
                    </span>
                    {lastItem.progress && (
                      <span className="text-[10px] font-medium px-1.5 py-0.5 rounded-full bg-[var(--accent)]/10 text-[var(--accent)]">
                        {lastItem.progress}
                      </span>
                    )}
                  </div>

                  {/* Details */}
                  <div className="space-y-1">
                    {group.items.map((step, sIdx) => (
                      <div
                        key={sIdx}
                        className={`text-xs leading-relaxed ${
                          isGroupActive && sIdx === group.items.length - 1
                            ? "text-[var(--foreground)]"
                            : "text-[var(--muted)]"
                        }`}
                      >
                        {isGroupActive && sIdx === group.items.length - 1 ? (
                          <span className="thinking-shimmer">{step.detail}</span>
                        ) : (
                          step.detail
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Footer */}
      <div className="px-5 py-3 border-t border-[var(--card-border)] flex-shrink-0">
        {isActive ? (
          <div className="flex items-center gap-2">
            <div className="flex gap-0.5">
              <span className="w-1 h-1 rounded-full bg-[var(--accent)] animate-bounce [animation-delay:0ms]" />
              <span className="w-1 h-1 rounded-full bg-[var(--accent)] animate-bounce [animation-delay:150ms]" />
              <span className="w-1 h-1 rounded-full bg-[var(--accent)] animate-bounce [animation-delay:300ms]" />
            </div>
            <span className="text-xs text-[var(--muted)]">Processing...</span>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <svg className="w-3.5 h-3.5 text-[var(--success)]" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            <span className="text-xs text-[var(--muted)]">Finished in {elapsedLabel}</span>
          </div>
        )}
      </div>
    </div>
  );
}
