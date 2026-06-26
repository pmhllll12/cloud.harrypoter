import { useState, useRef, useEffect } from "react";
import "./AIChatPage.css";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking" | "spotdetail" | "ai";
type Props = { onNavigate: (page: Page) => void };
type Message = { role: "user" | "assistant"; content: string };

const SUGGESTIONS = ["속리산 추천 코스", "서울 1박2일 여행", "제주 맛집 추천", "경복궁 관람 정보"];

export default function AIChatPage({ onNavigate }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async (text?: string) => {
    const trimmed = (text ?? input).trim();
    if (!trimmed || loading) return;
    const newMessages: Message[] = [...messages, { role: "user", content: trimmed }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: newMessages }),
      });
      const data = await res.json();
      setMessages(prev => [
        ...prev,
        { role: "assistant", content: data.reply || "오류가 발생했습니다. 다시 시도해주세요." },
      ]);
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: "연결 오류가 발생했습니다." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="aichat-page">
      <nav className="aichat-nav">
        <button className="aichat-back" onClick={() => onNavigate("landing")}>←</button>
        <span className="aichat-nav-title">AI 여행 가이드</span>
        <div className="aichat-nav-spacer" />
      </nav>

      {messages.length === 0 ? (
        <div className="aichat-welcome">
          <div className="aichat-welcome-icon">✦</div>
          <h2 className="aichat-welcome-title">무엇이든 물어보세요</h2>
          <p className="aichat-welcome-desc">
            관광지, 맛집, 교통, 문화유산까지<br />AI가 친절하게 안내해드립니다
          </p>
          <div className="aichat-suggestions">
            {SUGGESTIONS.map(s => (
              <button key={s} className="aichat-chip" onClick={() => sendMessage(s)}>
                {s}
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="aichat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`aichat-row aichat-row--${msg.role}`}>
              {msg.role === "assistant" && <div className="aichat-avatar">AI</div>}
              <div className={`aichat-bubble aichat-bubble--${msg.role}`}>{msg.content}</div>
            </div>
          ))}
          {loading && (
            <div className="aichat-row aichat-row--assistant">
              <div className="aichat-avatar">AI</div>
              <div className="aichat-bubble aichat-bubble--assistant aichat-bubble--loading">
                <span /><span /><span />
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
      )}

      <div className="aichat-input-area">
        <input
          className="aichat-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="여행에 대해 무엇이든 물어보세요..."
          disabled={loading}
        />
        <button className="aichat-send" onClick={() => sendMessage()} disabled={loading || !input.trim()}>
          전송
        </button>
      </div>
    </div>
  );
}
