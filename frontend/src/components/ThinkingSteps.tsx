"use client";

import { useState, useEffect, useRef } from "react";

export interface StatusStep {
  phase: string;
  detail: string;
  progress?: string; // e.g. "3/10"
}

interface ThinkingStepsProps {
  steps: StatusStep[];
  isActive: boolean;
  savedDuration?: number;
  onTogglePanel?: () => void;
}

const PHASE_LABELS: Record<string, string> = {
  extract: "Analyzing question",
  search: "Searching knowledge base",
  map: "Reading appearances",
  reduce: "Synthesizing answer",
};

export default function ThinkingSteps({ steps, isActive, savedDuration, onTogglePanel }: ThinkingStepsProps) {
  const startTime = useRef<number>(Date.now());
  const [elapsed, setElapsed] = useState<number>(savedDuration ?? 0);

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

  if (steps.length === 0) return null;

  const latestStep = steps[steps.length - 1];
  const isDone = !isActive;

  const elapsedLabel =
    elapsed >= 60
      ? `${Math.floor(elapsed / 60)}m ${elapsed % 60}s`
      : `${elapsed}s`;

  const displayLabel = isDone
    ? elapsed > 0 ? `Thought for ${elapsedLabel}` : "Thought"
    : `${PHASE_LABELS[latestStep.phase] || latestStep.phase}...`;

  return (
    <div className="w-full mb-3">
      <button
        onClick={onTogglePanel}
        className="flex items-center gap-2 text-sm text-[var(--muted)] hover:text-[var(--foreground)] transition-colors">
        {isActive ? (
          <svg
            className="animate-spin h-3.5 w-3.5 text-[var(--accent)]"
            viewBox="0 0 24 24"
          >
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        ) : (
          <svg className="h-3.5 w-3.5 text-[var(--success)]" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        )}
        <span>{displayLabel}</span>
        {isActive && latestStep.progress && (
          <span className="text-xs text-[var(--accent)]">
            {latestStep.progress}
          </span>
        )}
      </button>
    </div>
  );
}
