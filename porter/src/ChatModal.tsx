import { useState, useRef, useEffect } from "react";
import "./ChatModal.css";

type Message = { role: "user" | "assistant"; content: string };
type Props = { open: boolean; onClose: () => void };

export default function ChatModal({ open, onClose }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "안녕하세요! 대한민국 관광 AI 가이드입니다 😊\n문화유산, 관광지, 맛집, 교통까지 무엇이든 물어보세요!",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [open]);

  if (!open) return null;

  async function send() {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg: Message = { role: "user", content: text };
    const allMessages = [...messages, userMsg];
    setMessages(allMessages);
    setInput("");
    setLoading(true);

    const firstUserIdx = allMessages.findIndex((m) => m.role === "user");
    const chatPayload = allMessages.slice(firstUserIdx).map((m) => ({
      role: m.role,
      content: m.content,
    }));

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: chatPayload }),
      });

      const data = await res.json() as { reply?: string; error?: string };

      if (!res.ok || data.error) {
        throw new Error(data.error ?? `HTTP ${res.status}`);
      }

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.reply ?? "응답을 받지 못했습니다." },
      ]);
    } catch (e) {
      const msg = e instanceof Error ? e.message : "오류가 발생했습니다.";
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `오류: ${msg}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKey(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      void send();
    }
  }

  return (
    <div className="gchat-overlay" onClick={onClose}>
      <div className="gchat-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="gchat-header">
          <div className="gchat-header-left">
            <div className="gchat-gemini-icon" aria-hidden>
              <svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M14 2C14 8.627 8.627 14 2 14c6.627 0 12 5.373 12 12 0-6.627 5.373-12 12-12-6.627 0-12-5.373-12-12Z"
                  fill="url(#gemini-grad)"
                />
                <defs>
                  <linearGradient id="gemini-grad" x1="2" y1="2" x2="26" y2="26" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#4285F4"/>
                    <stop offset="0.5" stopColor="#9B72CB"/>
                    <stop offset="1" stopColor="#D96570"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div>
              <div className="gchat-title">AI 관광 가이드</div>
              <div className="gchat-subtitle">전국 문화유산 · 맛집 · 교통 안내</div>
            </div>
          </div>
          <button className="gchat-close" onClick={onClose} aria-label="닫기">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
          </button>
        </div>

        {/* Body */}
        <div className="gchat-body">
          {messages.map((m, i) => (
            <div key={i} className={`gchat-row gchat-row--${m.role}`}>
              {m.role === "assistant" && (
                <div className="gchat-ai-avatar" aria-hidden>
                  <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M10 1C10 5.418 6.418 9 2 9c4.418 0 8 3.582 8 8 0-4.418 3.582-8 8-8-4.418 0-8-3.582-8-8Z"
                      fill="url(#g2)"
                    />
                    <defs>
                      <linearGradient id="g2" x1="2" y1="1" x2="18" y2="17" gradientUnits="userSpaceOnUse">
                        <stop stopColor="#4285F4"/>
                        <stop offset="1" stopColor="#9B72CB"/>
                      </linearGradient>
                    </defs>
                  </svg>
                </div>
              )}
              <div className={`gchat-bubble gchat-bubble--${m.role}`}>
                {m.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="gchat-row gchat-row--assistant">
              <div className="gchat-ai-avatar" aria-hidden>
                <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M10 1C10 5.418 6.418 9 2 9c4.418 0 8 3.582 8 8 0-4.418 3.582-8 8-8-4.418 0-8-3.582-8-8Z"
                    fill="url(#g3)"
                  />
                  <defs>
                    <linearGradient id="g3" x1="2" y1="1" x2="18" y2="17" gradientUnits="userSpaceOnUse">
                      <stop stopColor="#4285F4"/>
                      <stop offset="1" stopColor="#9B72CB"/>
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <div className="gchat-bubble gchat-bubble--assistant gchat-typing">
                <span /><span /><span />
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Footer */}
        <div className="gchat-footer">
          <div className="gchat-input-wrap">
            <textarea
              ref={inputRef}
              className="gchat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="메시지를 입력하세요..."
              rows={1}
              disabled={loading}
            />
            <button
              className="gchat-send"
              onClick={() => void send()}
              disabled={!input.trim() || loading}
              aria-label="전송"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M12 5v14M5 12l7-7 7 7" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
          <p className="gchat-hint">Enter로 전송 · Shift+Enter로 줄바꿈</p>
        </div>
      </div>
    </div>
  );
}
