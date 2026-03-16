"use client";

import { useEffect, useState } from "react";
import InvestorCard from "@/components/InvestorCard";
import { getInvestors, Investor } from "@/lib/api";

export default function InvestorsPage() {
  const [investors, setInvestors] = useState<Investor[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getInvestors()
      .then(setInvestors)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load investors"))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[var(--foreground)]">Investors</h1>
        <p className="text-[var(--muted)] mt-1">
          Browse tracked investors and their market perspectives.
        </p>
      </div>

      {isLoading && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="h-36 rounded-xl bg-[var(--card)] border border-[var(--card-border)] animate-pulse"
            />
          ))}
        </div>
      )}

      {error && (
        <div className="p-4 rounded-lg bg-[var(--danger)]/10 border border-[var(--danger)]/20 text-[var(--danger)] text-sm">
          {error}
        </div>
      )}

      {!isLoading && !error && investors.length === 0 && (
        <div className="text-center py-16 text-[var(--muted)]">
          <p>No investors found.</p>
          <p className="text-sm mt-1">Make sure the backend API is running.</p>
        </div>
      )}

      {!isLoading && investors.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {investors.map((investor) => (
            <InvestorCard
              key={investor.slug}
              slug={investor.slug}
              name={investor.name}
              fund={investor.fund}
              topics={investor.topics}
              companiesTracked={investor.companies_tracked}
            />
          ))}
        </div>
      )}
    </div>
  );
}
