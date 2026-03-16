import Link from "next/link";

interface InvestorCardProps {
  slug: string;
  name: string;
  fund: string;
  sectors: string[];
  companiesTracked?: number;
}

export default function InvestorCard({
  slug,
  name,
  fund,
  sectors,
  companiesTracked,
}: InvestorCardProps) {
  return (
    <Link href={`/investors/${slug}`}>
      <div className="group p-5 rounded-xl bg-[var(--card)] border border-[var(--card-border)] hover:border-[var(--accent)]/50 transition-all cursor-pointer">
        <h3 className="text-lg font-semibold text-[var(--foreground)] group-hover:text-[var(--accent)] transition-colors">
          {name}
        </h3>
        <p className="text-sm text-[var(--muted)] mt-1">{fund}</p>

        {sectors.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-3">
            {sectors.map((sector) => (
              <span
                key={sector}
                className="px-2 py-0.5 text-xs rounded-full bg-[var(--accent)]/10 text-[var(--accent)] border border-[var(--accent)]/20"
              >
                {sector}
              </span>
            ))}
          </div>
        )}

        {companiesTracked !== undefined && (
          <p className="text-xs text-[var(--muted)] mt-3">
            {companiesTracked} companies tracked
          </p>
        )}
      </div>
    </Link>
  );
}
