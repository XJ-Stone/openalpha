const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface EntityRanking {
  name: string;
  kind: "company" | "topic";
  score: number;
}

export interface EntitiesResponse {
  companies: EntityRanking[];
  topics: EntityRanking[];
}

export interface Investor {
  slug: string;
  name: string;
  fund: string;
  role?: string;
  aum?: string;
  topics: string[];
  companies_tracked?: number;
}

export interface InvestorDetail extends Investor {
  appearances: Appearance[];
}

export interface Appearance {
  date: string;
  source: string;
  source_url?: string;
  companies_mentioned: string[];
  summary?: string;
}

export interface AnalyzeInvestorCard {
  name: string;
  fund: string;
  sentiment: "bullish" | "bearish" | "neutral";
  key_quote: string;
  date: string;
  source_url?: string;
}

export interface ChatHistoryMessage {
  role: "user" | "assistant";
  content: string;
}

/**
 * Calls POST /analyze with the user's question and optional chat history.
 * Returns a ReadableStream for streaming the response.
 */
export async function analyzeQuestion(
  question: string,
  options?: {
    history?: ChatHistoryMessage[];
    signal?: AbortSignal;
  }
): Promise<Response> {
  const body: Record<string, unknown> = { question };
  if (options?.history && options.history.length > 0) {
    body.history = options.history;
  }

  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal: options?.signal,
  });

  if (!res.ok) {
    throw new Error(`Analyze request failed: ${res.status} ${res.statusText}`);
  }

  return res;
}

/**
 * Fetches ranked entities (companies + topics) from recent appearances.
 */
export async function getEntities(): Promise<EntitiesResponse> {
  const res = await fetch(`${API_BASE}/entities`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch entities: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

/**
 * Fetches all investors from GET /investors.
 */
export async function getInvestors(): Promise<Investor[]> {
  const res = await fetch(`${API_BASE}/investors`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch investors: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

/**
 * Fetches a single investor profile from GET /investors/{slug}.
 */
export async function getInvestor(slug: string): Promise<InvestorDetail> {
  const res = await fetch(`${API_BASE}/investors/${encodeURIComponent(slug)}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch investor: ${res.status} ${res.statusText}`);
  }

  return res.json();
}
