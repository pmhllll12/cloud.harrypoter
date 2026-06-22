import { useCallback, useEffect, useRef, useState, type FormEvent } from "react";
import "./App.css";

type ChatMessage = {
  id: string;
  role: "user" | "model";
  text: string;
  pending?: boolean;
};

type MyselfResponse = {
  id: number;
  name: string;
};

type ProfessorChatResponse = {
  reply: string;
  model: string;
};

function uid(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return (await res.json()) as T;
}

async function postProfessorChat(message: string): Promise<ProfessorChatResponse> {
  const res = await fetch("/harry-poter/professor/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return (await res.json()) as ProfessorChatResponse;
}

const WELCOME =
  "안녕하세요! 저는 서울의 수호신 해치예요. 경복궁, 남대문, 한강진까지 — 서울 곳곳의 문화유산 이야기를 무엇이든 물어보세요.";

export default function App() {
  const [harryName, setHarryName] = useState<string | null>(null);
  const [professorName, setProfessorName] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: "welcome", role: "model", text: WELCOME },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getJson<MyselfResponse>("/harry-poter/harry/myself")
      .then((r) => setHarryName(r.name))
      .catch(() => setHarryName(null));
    getJson<MyselfResponse>("/harry-poter/professor/myself")
      .then((r) => setProfessorName(r.name))
      .catch(() => setProfessorName(null));
  }, []);

  useEffect(() => {
    const el = listRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages]);

  const send = useCallback(async () => {
    const text = input.trim();
    if (!text || loading) return;

    setError(null);
    setInput("");

    const userMsg: ChatMessage = { id: uid(), role: "user", text };
    const pendingId = uid();
    setMessages((prev) => [
      ...prev,
      userMsg,
      { id: pendingId, role: "model", text: "…해치가 생각하는 중이에요.", pending: true },
    ]);
    setLoading(true);
    try {
      const { reply } = await postProfessorChat(text);
      setMessages((prev) =>
        prev.map((m) => (m.id === pendingId ? { ...m, text: reply, pending: false } : m)),
      );
    } catch (e) {
      setMessages((prev) => prev.filter((m) => m.id !== pendingId));
      setError(e instanceof Error ? e.message : "알 수 없는 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  }, [input, loading]);

  const onSubmit = (e: FormEvent) => {
    e.preventDefault();
    void send();
  };

  return (
    <main className="page">
      <header className="hero">
        <div className="mascot" aria-hidden="true">
          🦁
        </div>
        <div>
          <h1>해치와 함께하는 서울 문화유산 어드벤처</h1>
          <p className="tagline">
            전설의 수호신 <strong>해치</strong>가 안내하는 서울 문화유산 이야기 데모
          </p>
        </div>
      </header>

      {error ? <div className="error">{error}</div> : null}

      <div className="chat" ref={listRef}>
        {messages.map((m) => (
          <div key={m.id} className={`bubble bubble--${m.role}`}>
            <span className="who-tag">{m.role === "user" ? "나" : "해치"}</span>
            <p>{m.text}</p>
          </div>
        ))}
      </div>

      <form className="form" onSubmit={onSubmit}>
        <input
          type="text"
          placeholder="예: 경복궁에 대해 알려줘"
          value={input}
          disabled={loading}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? "물어보는 중…" : "물어보기"}
        </button>
      </form>

      <p className="footnote">
        데모 엔진 캐릭터: {harryName ?? "..."} · {professorName ?? "..."}
      </p>
    </main>
  );
}
