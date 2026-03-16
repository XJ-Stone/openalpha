interface SentimentBadgeProps {
  sentiment: "bullish" | "bearish" | "neutral";
}

const config = {
  bullish: {
    label: "Bullish",
    classes: "bg-[var(--success)]/10 text-[var(--success)] border-[var(--success)]/20",
  },
  bearish: {
    label: "Bearish",
    classes: "bg-[var(--danger)]/10 text-[var(--danger)] border-[var(--danger)]/20",
  },
  neutral: {
    label: "Neutral",
    classes: "bg-[var(--warning)]/10 text-[var(--warning)] border-[var(--warning)]/20",
  },
};

export default function SentimentBadge({ sentiment }: SentimentBadgeProps) {
  const { label, classes } = config[sentiment] || config.neutral;

  return (
    <span className={`inline-block px-2.5 py-0.5 text-xs font-medium rounded-full border ${classes}`}>
      {label}
    </span>
  );
}
