import { useState, useRef, useEffect } from "react";
import "./MapPage.css";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking" | "spotdetail";
type Props = { onNavigate: (page: Page) => void };

type Message = { role: "user" | "ai"; text: string };

const SPOTS = [
  {
    tag: "추천" as const,
    title: "속리산 국립공원",
    region: "충북 보은",
    guide: "AI 관광 가이드",
    progress: 92,
  },
  {
    tag: "추천" as const,
    title: "법주사",
    region: "충북 보은",
    guide: "AI 관광 가이드",
    progress: 85,
  },
  {
    tag: "진행 중" as const,
    title: "단양 패러글라이딩",
    region: "충북 단양",
    guide: "AI 관광 가이드",
    progress: 60,
  },
  {
    tag: "진행 중" as const,
    title: "청주 고인쇄박물관",
    region: "충북 청주",
    guide: "AI 관광 가이드",
    progress: 74,
  },
];

const AI_RESPONSES: Record<string, string> = {
  default: "안녕하세요! 충북 관광 AI 가이드입니다. 여행 계획, 관광지 추천, 맛집 정보 등 무엇이든 물어보세요!",
};

function getAIResponse(input: string): string {
  if (input.includes("속리산") || input.includes("국립공원")) {
    return "속리산 국립공원은 충북 보은에 위치한 아름다운 명산입니다. 법주사, 세조길, 문장대 등 볼거리가 많아요. 봄 철쭉과 가을 단풍이 특히 아름답습니다!";
  }
  if (input.includes("법주사")) {
    return "법주사는 신라 시대에 창건된 유서 깊은 사찰입니다. 국보인 쌍사자석등과 팔상전이 있으며, 속리산 국립공원 내에 위치해 있어 함께 방문하기 좋습니다.";
  }
  if (input.includes("맛집") || input.includes("음식")) {
    return "충북의 대표 음식으로는 청주 순대국밥, 단양 마늘요리, 보은 대추 관련 음식이 있습니다. 지역 특산물을 활용한 맛집이 많으니 꼭 방문해 보세요!";
  }
  if (input.includes("추천") || input.includes("어디")) {
    return "충북 여행지로는 속리산 국립공원, 단양 8경, 청주 고인쇄박물관, 청남대를 추천드립니다. 계절에 따라 다양한 매력을 즐길 수 있어요!";
  }
  return "좋은 질문이에요! 충북에는 아름다운 자연과 역사 문화 명소가 가득합니다. 더 구체적인 장소나 활동에 대해 알고 싶으시면 말씀해 주세요.";
}

export default function MapPage({ onNavigate }: Props) {
  const [aiMode, setAiMode] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: "ai", text: AI_RESPONSES.default },
  ]);
  const [input, setInput] = useState("");
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    const trimmed = input.trim();
    if (!trimmed) return;
    const userMsg: Message = { role: "user", text: trimmed };
    const aiMsg: Message = { role: "ai", text: getAIResponse(trimmed) };
    setMessages((prev) => [...prev, userMsg, aiMsg]);
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="map-page">
      {/* Navbar */}
      <nav className="map-nav">
        <div className="map-nav-left">
          <div className="map-nav-brand" onClick={() => onNavigate("landing")}>
            <div className="nav-logo-circle">
              <span className="nav-logo-text">A</span>
            </div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="map-nav-links">
            <a onClick={() => onNavigate("tourinfo")}>관광정보</a>
            <a className="active">관광동선</a>
            <a onClick={() => onNavigate("store")}>스토어</a>
            <a onClick={() => onNavigate("ticket")}>티켓</a>
          </div>
        </div>
        <div className="map-nav-right">
          <div className="map-nav-setting">설정</div>
        </div>
      </nav>

      {/* Hero */}
      <div className="map-hero">
        <img src="/palace.jpg" alt="충북 관광" />
      </div>

      {/* Body */}
      <div className="map-body">
        {/* Left stats */}
        <div className="map-stats">
          <div className="stat-card">
            <div className="stat-card-header">
              <span className="stat-card-title">이번 주 방문객</span>
              <span className="stat-card-menu">···</span>
            </div>
            <div className="stat-num">2,840</div>
            <div className="stat-sub">
              <span className="stat-up">↑ 340명</span>&nbsp;지난주보다 많음
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-card-header">
              <span className="stat-card-title">진행 중인 행사</span>
              <span className="stat-card-menu">···</span>
            </div>
            <div className="stat-num">8</div>
            <div className="stat-sub">
              <span className="stat-up">↑ 2개</span>&nbsp;지난주보다 많음
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-card-header">
              <span className="stat-card-title">등록 관광지</span>
              <span className="stat-card-menu">···</span>
            </div>
            <div className="stat-num">156</div>
            <div className="stat-sub">
              <span>→</span>&nbsp;지난주와 동일
            </div>
          </div>
        </div>

        {/* Center: map with overlaid AI chat */}
        <div className="map-center">
          {aiMode ? (
            <div className="ai-chat-panel">
              <div className="ai-chat-character">
                <img src="/ai-character-male.png" alt="AI 가이드" />
              </div>
              <div className="ai-chat-area">
                <div className="ai-chat-messages">
                  {messages.map((msg, i) => (
                    <div key={i} className={`ai-msg ai-msg--${msg.role}`}>
                      {msg.role === "ai" && (
                        <div className="ai-msg-avatar">AI</div>
                      )}
                      <div className="ai-msg-bubble">{msg.text}</div>
                    </div>
                  ))}
                  <div ref={chatEndRef} />
                </div>
                <div className="ai-chat-input-row">
                  <input
                    className="ai-chat-input"
                    placeholder="관광지, 맛집, 일정 등 무엇이든 물어보세요..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                  />
                  <button className="ai-chat-send" onClick={sendMessage}>
                    전송
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="map-container">
              <button
                className="map-ai-btn"
                onClick={() => setAiMode(true)}
              >
                AI 검색
              </button>
              <iframe
                title="충북 지도"
                src="https://www.openstreetmap.org/export/embed.html?bbox=127.0%2C36.3%2C128.6%2C37.3&layer=mapnik&marker=36.6424%2C127.4890"
              />
            </div>
          )}
        </div>

        {/* Right: spot cards */}
        <div className="map-sidebar">
          {SPOTS.map((s) => (
            <div className="spot-card" key={s.title}>
              <div className={`spot-tag spot-tag--${s.tag === "추천" ? "active" : "progress"}`}>
                {s.tag}
              </div>
              <h3>{s.title}</h3>
              <div className="spot-meta">
                <span>2026</span>
                <div className="spot-meta-dot" />
                <span>{s.region}</span>
              </div>
              <div className="spot-guide">
                <div className="spot-guide-avatar">🗺️</div>
                <div className="spot-guide-info">
                  <span className="spot-guide-role">관광 가이드</span>
                  <span className="spot-guide-name">{s.guide}</span>
                </div>
              </div>
              <div className="spot-progress-row">
                <div className="spot-bar">
                  <div className="spot-bar-fill" style={{ width: `${s.progress}%` }} />
                </div>
                <span className="spot-pct">{s.progress}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
