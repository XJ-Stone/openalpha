"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import Link from "next/link";
import SearchBar from "@/components/SearchBar";
import ChatMessage, { Message } from "@/components/ChatMessage";
import { StatusStep } from "@/components/ThinkingSteps";
import { Source } from "@/components/ResponseStream";
import EntityChips from "@/components/EntityChips";
import EntityDrawer from "@/components/EntityDrawer";
import ThemeToggle from "@/components/ThemeToggle";
import { analyzeQuestion } from "@/lib/api";

// ---------------------------------------------------------------------------
// Chat history types & localStorage helpers
// ---------------------------------------------------------------------------

interface ChatSession {
  id: string;
  title: string; // first user message, truncated
  messages: Message[];
  createdAt: number;
}

const STORAGE_KEY = "openalpha_chats";
const MAX_SAVED_CHATS = 20;

function loadChats(): ChatSession[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveChats(chats: ChatSession[]) {
  try {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(chats.slice(0, MAX_SAVED_CHATS))
    );
  } catch {
    // localStorage full — silently fail
  }
}

function generateId() {
  return `chat-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
}

let messageIdCounter = 0;
function nextMsgId() {
  return `msg-${++messageIdCounter}`;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function HomePage() {
  const [chats, setChats] = useState<ChatSession[]>([]);
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);
  const userScrolledUpRef = useRef(false);

  // Load chats from localStorage on mount
  useEffect(() => {
    setChats(loadChats());
  }, []);

  // Persist current chat whenever messages change (and not streaming)
  useEffect(() => {
    if (!activeChatId || isLoading) return;
    if (messages.length === 0) return;

    setChats((prev) => {
      const updated = prev.map((c) =>
        c.id === activeChatId ? { ...c, messages } : c
      );
      saveChats(updated);
      return updated;
    });
  }, [messages, isLoading, activeChatId]);

  // Track user scroll: if they scroll up, stop auto-scrolling.
  // If they scroll back near the bottom, resume auto-scrolling.
  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;

    const onScroll = () => {
      const distFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
      userScrolledUpRef.current = distFromBottom > 80;
    };

    el.addEventListener("scroll", onScroll, { passive: true });
    return () => el.removeEventListener("scroll", onScroll);
  }, []);

  // Auto-scroll on new content, but only if user hasn't scrolled up.
  // We check the live scroll position rather than only the ref, because
  // the ref can be stale due to React batching and passive listener timing.
  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const distFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    if (distFromBottom > 80) return;
    el.scrollTop = el.scrollHeight;
  }, [messages]);

  const startNewChat = useCallback(() => {
    setActiveChatId(null);
    setMessages([]);
    setSidebarOpen(false);
  }, []);

  const loadChat = useCallback((chat: ChatSession) => {
    setActiveChatId(chat.id);
    setMessages(
      chat.messages.map((m) => ({
        ...m,
        isStreaming: false,
        isThinking: false,
      }))
    );
    setSidebarOpen(false);
  }, []);

  const deleteChat = useCallback(
    (chatId: string) => {
      setChats((prev) => {
        const updated = prev.filter((c) => c.id !== chatId);
        saveChats(updated);
        return updated;
      });
      if (activeChatId === chatId) {
        setActiveChatId(null);
        setMessages([]);
      }
    },
    [activeChatId]
  );

  const handleStop = useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
  }, []);

  const handleSearch = useCallback(
    async (question: string) => {
      // Reset auto-scroll on new question
      userScrolledUpRef.current = false;

      // Create chat session if this is the first message
      let chatId = activeChatId;
      const isFollowUp = messages.length > 0;
      if (!chatId) {
        chatId = generateId();
        const newChat: ChatSession = {
          id: chatId,
          title: question.slice(0, 60),
          messages: [],
          createdAt: Date.now(),
        };
        setActiveChatId(chatId);
        setChats((prev) => {
          const updated = [newChat, ...prev];
          saveChats(updated);
          return updated;
        });
      }

      // Build history from existing completed messages for follow-ups
      const history = isFollowUp
        ? messages
            .filter(
              (m) =>
                m.content &&
                m.content !== "(Stopped)" &&
                !m.isStreaming &&
                !m.isThinking
            )
            .map((m) => ({
              role: m.role as "user" | "assistant",
              content: m.content,
            }))
        : [];

      const userMsg: Message = {
        id: nextMsgId(),
        role: "user",
        content: question,
      };
      const assistantId = nextMsgId();
      const assistantMsg: Message = {
        id: assistantId,
        role: "assistant",
        content: "",
        steps: [],
        isThinking: true,
        isStreaming: false,
      };

      setMessages((prev) => [...prev, userMsg, assistantMsg]);
      setIsLoading(true);

      const controller = new AbortController();
      abortRef.current = controller;

      try {
        const res = await analyzeQuestion(question, {
          history,
          signal: controller.signal,
        });
        const reader = res.body?.getReader();
        if (!reader) throw new Error("No response stream available");

        const decoder = new TextDecoder();
        let accumulated = "";
        let steps: StatusStep[] = [];
        let sources: Source[] = [];
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() || "";

          for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed || !trimmed.startsWith("data: ")) continue;

            const data = trimmed.slice(6);
            if (data === "[DONE]") continue;

            try {
              const parsed = JSON.parse(data);

              if (parsed.type === "status") {
                steps = [
                  ...steps,
                  {
                    phase: parsed.phase,
                    detail: parsed.detail,
                    progress: parsed.progress || undefined,
                  },
                ];
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantId
                      ? { ...m, steps: [...steps], isThinking: true }
                      : m
                  )
                );
              } else if (parsed.type === "token" && parsed.token) {
                accumulated += parsed.token;
                const content = accumulated;
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantId
                      ? {
                          ...m,
                          content,
                          isThinking: false,
                          isStreaming: true,
                        }
                      : m
                  )
                );
              } else if (parsed.type === "content_replace") {
                accumulated = parsed.content;
                const replacedContent = accumulated;
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantId
                      ? { ...m, content: replacedContent }
                      : m
                  )
                );
              } else if (parsed.type === "sources") {
                sources = parsed.sources;
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantId
                      ? { ...m, sources: [...sources] }
                      : m
                  )
                );
              } else if (parsed.type === "error") {
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantId
                      ? {
                          ...m,
                          content: `Error: ${parsed.detail}`,
                          isThinking: false,
                          isStreaming: false,
                        }
                      : m
                  )
                );
              }
            } catch {
              // Ignore malformed JSON
            }
          }
        }

        // Stream complete
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? { ...m, isStreaming: false, isThinking: false }
              : m
          )
        );
      } catch (err) {
        // If aborted, just mark as complete with whatever we have
        const isAbort = err instanceof DOMException && err.name === "AbortError";
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? {
                  ...m,
                  content: isAbort
                    ? m.content || "(Stopped)"
                    : err instanceof Error
                      ? err.message
                      : "An error occurred",
                  isThinking: false,
                  isStreaming: false,
                }
              : m
          )
        );
      } finally {
        abortRef.current = null;
        setIsLoading(false);
      }
    },
    [activeChatId, messages]
  );

  const hasMessages = messages.length > 0;

  return (
    <div className="flex h-screen">
      {/* Sidebar overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-30 sm:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Left rail — hidden on mobile when collapsed, visible on sm+ */}
      <div
        className={`${
          sidebarOpen ? "w-64" : "w-0 sm:w-12"
        } fixed sm:static z-40 sm:z-auto h-full bg-[var(--card)] flex flex-col sm:transition-[width] sm:duration-200 overflow-hidden`}
      >
        {/* Top controls — fixed position, no layout shift */}
        <div className="flex flex-col p-2 flex-shrink-0">
          {/* Row 1: Toggle always visible at left; when expanded, logo left + toggle right */}
          <div className="h-8 flex items-center overflow-hidden whitespace-nowrap">
            {sidebarOpen ? (
              <>
                <Link href="/" className="text-base font-bold tracking-tight text-[var(--foreground)] pl-0.5">
                  OpenAlpha
                </Link>
                <button
                  onClick={() => setSidebarOpen(false)}
                  className="ml-auto w-8 h-8 flex items-center justify-center rounded-lg hover:bg-[var(--card-border)] text-[var(--muted)] hover:text-[var(--foreground)] transition-colors flex-shrink-0"
                  title="Close sidebar"
                >
                  <svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" />
                    <line x1="9" y1="3" x2="9" y2="21" />
                  </svg>
                </button>
              </>
            ) : (
              <button
                onClick={() => setSidebarOpen(true)}
                className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-[var(--card-border)] text-[var(--muted)] hover:text-[var(--foreground)] transition-colors flex-shrink-0"
                title="Open sidebar"
              >
                <svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="3" width="18" height="18" rx="2" />
                  <line x1="15" y1="3" x2="15" y2="21" />
                </svg>
              </button>
            )}
          </div>

          {/* Spacer */}
          <div className="h-3" />

          {/* Row 2: New chat — icon always in DOM, text always in DOM, clipped by parent overflow */}
          <button
            onClick={startNewChat}
            className="h-8 flex items-center rounded-lg hover:bg-[var(--card-border)] transition-colors w-full overflow-hidden whitespace-nowrap"
            title="New chat"
          >
            <span className="w-8 h-8 flex items-center justify-center flex-shrink-0">
              <span className="w-[22px] h-[22px] rounded-full bg-[var(--card-border)] flex items-center justify-center">
                <svg className="w-3 h-3 text-[var(--muted)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19" />
                  <line x1="5" y1="12" x2="19" y2="12" />
                </svg>
              </span>
            </span>
            <span className="text-sm text-[var(--foreground)] ml-1.5">New chat</span>
          </button>
        </div>

        {/* Recents — only when expanded */}
        {sidebarOpen && (
          <div className="flex-1 overflow-y-auto px-2 min-h-0">
            <p className="text-[11px] font-semibold uppercase tracking-wider text-[var(--muted)] px-2 pb-1 pt-2">
              Recents
            </p>
            {chats.length === 0 ? (
              <p className="text-xs text-[var(--muted)] px-2 py-2">No conversations yet</p>
            ) : (
              <div className="space-y-0.5">
                {chats.map((chat) => (
                  <div
                    key={chat.id}
                    className={`group flex items-center rounded-lg text-sm cursor-pointer transition-colors ${
                      chat.id === activeChatId
                        ? "bg-[var(--card-border)] text-[var(--foreground)]"
                        : "text-[var(--muted)] hover:bg-[var(--card-border)] hover:text-[var(--foreground)]"
                    }`}
                  >
                    <button
                      onClick={() => loadChat(chat)}
                      className="flex-1 text-left px-2 py-1.5 truncate min-w-0"
                      title={chat.title}
                    >
                      {chat.title}
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteChat(chat.id);
                      }}
                      className="p-1 mr-1 rounded opacity-0 group-hover:opacity-100 hover:bg-[var(--background)] text-[var(--muted)] hover:text-[var(--danger)] transition-all"
                      title="Delete"
                    >
                      <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                        <path
                          fillRule="evenodd"
                          d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Theme toggle — pinned to bottom of left rail */}
        <div className="mt-auto p-2 flex-shrink-0">
          <ThemeToggle />
        </div>
      </div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col min-w-0 relative">

        {/* Mobile menu button — landing page only */}
        {!hasMessages && !sidebarOpen && (
          <button
            onClick={() => setSidebarOpen(true)}
            className="sm:hidden absolute top-3 left-3 z-20 w-8 h-8 flex items-center justify-center rounded-lg bg-[var(--card)] border border-[var(--card-border)] text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
            title="Open menu"
          >
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>
        )}

        {/* Top bar — only visible in chat view */}
        {hasMessages && (
          <div className="flex items-center justify-between px-4 py-2 border-b border-[var(--card-border)] bg-[var(--background)] flex-shrink-0">
            <div className="flex items-center gap-2">
              {!sidebarOpen && (
                <button
                  onClick={() => setSidebarOpen(true)}
                  className="sm:hidden w-8 h-8 flex items-center justify-center rounded-lg hover:bg-[var(--card)] text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
                  title="Open menu"
                >
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="3" y1="6" x2="21" y2="6" />
                    <line x1="3" y1="12" x2="21" y2="12" />
                    <line x1="3" y1="18" x2="21" y2="18" />
                  </svg>
                </button>
              )}
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setDrawerOpen(true)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-[var(--card)] text-xs text-[var(--muted)] hover:text-[var(--foreground)] transition-all"
                title="Trending Topics"
              >
                <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
                </svg>
                Trending
              </button>
            </div>
          </div>
        )}

        {/* Empty state */}
        {!hasMessages && (
          <div className="flex-1 flex flex-col items-center justify-center px-4">
            <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-[var(--foreground)] mb-3">
              Investor Intelligence
            </h1>
            <p className="text-[var(--muted)] text-lg mb-8">
              Ask anything about what top investors are saying.
            </p>
            <div className="w-full max-w-2xl">
              <SearchBar onSubmit={handleSearch} onStop={handleStop} isLoading={isLoading} />
            </div>
            <div className="mt-6 flex flex-wrap justify-center gap-2">
              {[
                "What is Freda's view on Amazon?",
                "Freda's take on AI infrastructure spending",
                "What does Freda think about China tech?",
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => handleSearch(suggestion)}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-[var(--accent)]/8 border border-[var(--accent)]/20 text-[var(--accent)] text-xs font-medium hover:bg-[var(--accent)]/15 hover:border-[var(--accent)]/40 transition-all cursor-pointer"
                >
                  <svg className="w-3 h-3 opacity-60" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
                  </svg>
                  {suggestion}
                </button>
              ))}
            </div>
            <div className="mt-8 w-full max-w-2xl">
              <EntityChips onSelect={handleSearch} />
            </div>
          </div>
        )}

        {/* Chat messages */}
        {hasMessages && (
          <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-6">
            <div className="max-w-3xl mx-auto">
              {messages.map((msg) => (
                <ChatMessage key={msg.id} message={msg} />
              ))}
            </div>
          </div>
        )}

        {/* Bottom input */}
        {hasMessages && (
          <div className="border-t border-[var(--card-border)] bg-[var(--background)] px-4 py-4">
            <div className="max-w-3xl mx-auto">
              <SearchBar onSubmit={handleSearch} onStop={handleStop} isLoading={isLoading} />
            </div>
          </div>
        )}
      </div>

      {/* Entity drawer for chat view */}
      <EntityDrawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        onSelect={handleSearch}
      />
    </div>
  );
}
