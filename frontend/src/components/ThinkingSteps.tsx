"use client";

import { useState, useEffect, useRef } from "react";

export interface StatusStep {
  phase: string;
  detail: string;
  progress?: string; // e.g. "3/10"
}

interface ThinkingStepsProps {
  steps: StatusStep[];
  isActive: boolean; // still receiving status events
}

const PHASE_LABELS: Record<string, string> = {
  extract: "Analyzing question",
  search: "Searching knowledge base",
  map: "Reading appearances",
  reduce: "Synthesizing answer",
};

function buildCompletionSummary(steps: StatusStep[]): string {
  // Find the search step for context
  const searchStep = steps.find((s) => s.phase === "search");
  const mapStep = steps.filter((s) => s.phase === "map").pop();

  const parts: string[] = [];
  if (searchStep) parts.push(searchStep.detail);
  if (mapStep && mapStep.detail.includes("relevant")) parts.push(mapStep.detail);

  if (parts.length > 0) return parts.join(", ");
  return "Analysis complete";
}

export default function ThinkingSteps({ steps, isActive }: ThinkingStepsProps) {
  const [expanded, setExpanded] = useState(false);
  const startTime = useRef<number>(Date.now());
  const [elapsed, setElapsed] = useState<number>(0);

  // Track elapsed time
  useEffect(() => {
    if (!isActive) {
      setElapsed(Math.round((Date.now() - startTime.current) / 1000));
      return;
    }
    const interval = setInterval(() => {
      setElapsed(Math.round((Date.now() - startTime.current) / 1000));
    }, 1000);
    return () => clearInterval(interval);
  }, [isActive]);

  if (steps.length === 0) return null;

  const latestStep = steps[steps.length - 1];
  const isDone = !isActive;

  // Active: show current phase. Done: show summary with elapsed time.
  const displayLabel = isDone
    ? buildCompletionSummary(steps)
    : `${PHASE_LABELS[latestStep.phase] || latestStep.phase}...`;

  const elapsedLabel =
    elapsed >= 60
      ? `${Math.floor(elapsed / 60)}m ${elapsed % 60}s`
      : `${elapsed}s`;

  return (
    <div className="w-full mb-3">
      {/* Collapsed row — click to expand */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-2 text-sm text-[var(--muted)] hover:text-[var(--foreground)] transition-colors group"
      >
        {isActive ? (
          <svg
            className="animate-spin h-3.5 w-3.5 text-[var(--accent)]"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
              fill="none"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
        ) : (
          <svg
            className={`h-3.5 w-3.5 transition-transform ${expanded ? "rotate-90" : ""}`}
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
              clipRule="evenodd"
            />
          </svg>
        )}
        <span>{displayLabel}</span>
        {isActive && latestStep.progress && (
          <span className="text-xs text-[var(--accent)]">
            {latestStep.progress}
          </span>
        )}
        {isDone && (
          <span className="text-xs opacity-50">{elapsedLabel}</span>
        )}
      </button>

      {/* Expanded timeline */}
      {expanded && (
        <div className="mt-2 ml-1 pl-3 border-l border-[var(--card-border)]">
          {steps.map((step, idx) => {
            const isLast = idx === steps.length - 1;
            const phaseLabel = PHASE_LABELS[step.phase] || step.phase;
            const stepDone = !isLast || !isActive;

            return (
              <div
                key={idx}
                className={`flex items-start gap-2 py-1.5 text-xs ${
                  stepDone
                    ? "text-[var(--muted)]"
                    : "text-[var(--foreground)]"
                }`}
              >
                <span className="w-4 text-center flex-shrink-0">
                  {stepDone ? (
                    <svg
                      className="h-3.5 w-3.5 text-[var(--success)] inline"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  ) : (
                    <svg
                      className="animate-spin h-3 w-3 text-[var(--accent)] inline"
                      viewBox="0 0 24 24"
                    >
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                  )}
                </span>
                <div>
                  <span className="font-medium">{phaseLabel}</span>
                  <span className="ml-1.5 opacity-70">{step.detail}</span>
                  {step.progress && (
                    <span className="ml-1.5 text-[var(--accent)]">
                      ({step.progress})
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
