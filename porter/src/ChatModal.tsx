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

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  if (!open) return null;

  async function send() {
    const text = input.trim();
    if (!text || loading) return;

    const next: Message[] = [...messages, { role: "user", content: text }];
    setMessages(next);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: next }),
      });
      const data = await res.json();
      setMessages([
        ...next,
        { role: "assistant", content: data.reply ?? data.error ?? "오류가 발생했습니다." },
      ]);
    } catch {
      setMessages([
        ...next,
        { role: "assistant", content: "네트워크 오류가 발생했습니다. 잠시 후 다시 시도해 주세요." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKey(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  return (
    <div className="chat-overlay" onClick={onClose}>
      <div className="chat-modal" onClick={(e) => e.stopPropagation()}>
        <div className="chat-header">
          <div className="chat-header-info">
            <div className="chat-avatar">AI</div>
            <div>
              <div className="chat-title">AI 관광 가이드</div>
              <div className="chat-subtitle">전국 문화유산 · 맛집 · 교통 안내</div>
            </div>
          </div>
          <button className="chat-close" onClick={onClose} aria-label="닫기">✕</button>
        </div>

        <div className="chat-body">
          {messages.map((m, i) => (
            <div key={i} className={`chat-msg chat-msg--${m.role}`}>
              {m.role === "assistant" && <div className="chat-msg-avatar">AI</div>}
              <div className="chat-bubble">{m.content}</div>
            </div>
          ))}
          {loading && (
            <div className="chat-msg chat-msg--assistant">
              <div className="chat-msg-avatar">AI</div>
              <div className="chat-bubble chat-typing">
                <span /><span /><span />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="chat-footer">
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="궁금한 점을 물어보세요... (Enter로 전송)"
            rows={1}
            disabled={loading}
          />
          <button
            className="chat-send"
            onClick={send}
            disabled={!input.trim() || loading}
            aria-label="전송"
          >
            ↑
          </button>
        </div>
      </div>
    </div>
  );
}
