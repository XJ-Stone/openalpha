"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getInvestor, InvestorDetail } from "@/lib/api";

export default function InvestorProfilePage() {
  const params = useParams();
  const slug = params.slug as string;

  const [investor, setInvestor] = useState<InvestorDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    getInvestor(slug)
      .then(setInvestor)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load investor"))
      .finally(() => setIsLoading(false));
  }, [slug]);

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 space-y-4">
        <div className="h-8 w-48 rounded bg-[var(--card)] animate-pulse" />
        <div className="h-4 w-32 rounded bg-[var(--card)] animate-pulse" />
        <div className="h-64 rounded-xl bg-[var(--card)] animate-pulse mt-8" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        <Link href="/investors" className="text-sm text-[var(--accent)] hover:underline mb-4 block">
          &larr; Back to Investors
        </Link>
        <div className="p-4 rounded-lg bg-[var(--danger)]/10 border border-[var(--danger)]/20 text-[var(--danger)] text-sm">
          {error}
        </div>
      </div>
    );
  }

  if (!investor) return null;

  // Sort appearances by date, most recent first
  const sortedAppearances = [...(investor.appearances || [])].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
  );

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
      <Link href="/investors" className="text-sm text-[var(--accent)] hover:underline mb-6 block">
        &larr; Back to Investors
      </Link>

      {/* Profile header */}
      <div className="p-6 rounded-xl bg-[var(--card)] border border-[var(--card-border)]">
        <h1 className="text-3xl font-bold text-[var(--foreground)]">{investor.name}</h1>
        <p className="text-[var(--muted)] mt-1">
          {investor.role ? `${investor.role} at ` : ""}
          {investor.fund}
        </p>

        <div className="flex flex-wrap gap-4 mt-4 text-sm">
          {investor.aum && (
            <div>
              <span className="text-[var(--muted)]">AUM: </span>
              <span className="text-[var(--foreground)] font-medium">{investor.aum}</span>
            </div>
          )}
        </div>

        {investor.topics.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-4">
            {investor.topics.map((topic) => (
              <span
                key={topic}
                className="px-2.5 py-1 text-xs rounded-full bg-[var(--accent)]/10 text-[var(--accent)] border border-[var(--accent)]/20"
              >
                {topic}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Appearances */}
      <div className="mt-8">
        <h2 className="text-xl font-semibold text-[var(--foreground)] mb-4">
          Appearances
          {sortedAppearances.length > 0 && (
            <span className="text-sm font-normal text-[var(--muted)] ml-2">
              ({sortedAppearances.length})
            </span>
          )}
        </h2>

        {sortedAppearances.length === 0 ? (
          <p className="text-[var(--muted)] text-sm">No appearances recorded yet.</p>
        ) : (
          <div className="space-y-3">
            {sortedAppearances.map((appearance, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl bg-[var(--card)] border border-[var(--card-border)]"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-sm font-medium text-[var(--foreground)]">{appearance.source}</p>
                    <p className="text-xs text-[var(--muted)] mt-0.5">{appearance.date}</p>
                  </div>
                  {appearance.source_url && (
                    <a
                      href={appearance.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-[var(--accent)] hover:underline shrink-0"
                    >
                      View source
                    </a>
                  )}
                </div>

                {appearance.summary && (
                  <p className="text-sm text-[var(--foreground)]/80 mt-2">{appearance.summary}</p>
                )}

                {appearance.companies_mentioned.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mt-3">
                    {appearance.companies_mentioned.map((company) => (
                      <span
                        key={company}
                        className="px-2 py-0.5 text-xs rounded bg-[var(--card-border)]/30 text-[var(--foreground)]/70 border border-[var(--card-border)]"
                      >
                        {company}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
