import "./TourInfoPage.css";
import type { Spot } from "./SpotDetailPage";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking" | "spotdetail";
type Props = { onNavigate: (page: Page) => void; onViewSpot: (spot: Spot) => void };

const SPOTS = [
  {
    name: "속리산 국립공원",
    region: "충북 보은",
    category: "자연",
    desc: "해발 1,058m의 장엄한 봉우리와 울창한 원시림. 법주사, 세조길 등 자연과 역사가 공존하는 충북 대표 명소.",
    img: "https://images.unsplash.com/photo-1542223616-9de9adb5e3e8?w=1400&q=90&fit=crop",
  },
  {
    name: "단양 도담삼봉",
    region: "충북 단양",
    category: "자연",
    desc: "남한강 한가운데 솟아오른 세 개의 봉우리. 조선 시대부터 단양팔경의 으뜸으로 꼽히는 절경.",
    img: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1400&q=90&fit=crop",
  },
  {
    name: "법주사",
    region: "충북 보은",
    category: "역사문화",
    desc: "553년 창건된 천년 고찰. 국보 팔상전과 33m 청동 미륵대불이 있는 유네스코 세계유산.",
    img: "https://images.unsplash.com/photo-1548115184-bc6544d06a58?w=1400&q=90&fit=crop",
  },
  {
    name: "청주 고인쇄박물관",
    region: "충북 청주",
    category: "역사문화",
    desc: "세계 최초 금속활자본 직지심체요절의 고향. 금속활자 인쇄술의 역사를 직접 체험할 수 있는 박물관.",
    img: "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1400&q=90&fit=crop",
  },
  {
    name: "괴산 산막이옛길",
    region: "충북 괴산",
    category: "자연",
    desc: "괴산호수를 따라 이어지는 4km 호반 산책로. 기암절벽과 맑은 호수가 빚어내는 사계절 풍경.",
    img: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1400&q=90&fit=crop",
  },
  {
    name: "수안보 온천",
    region: "충북 충주",
    category: "힐링",
    desc: "우리나라 최초의 자연 용출 온천. 53°C의 알칼리성 온천수가 피로를 녹여주는 힐링 명소.",
    img: "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=1400&q=90&fit=crop",
  },
];

const CATEGORIES = ["전체", "자연", "역사문화", "힐링"];

export default function TourInfoPage({ onNavigate, onViewSpot }: Props) {
  return (
    <div className="tourinfo-page">
      <nav className="ti-nav">
        <div className="ti-nav-left">
          <div className="ti-nav-brand" onClick={() => onNavigate("landing")}>
            <div className="nav-logo-circle"><span className="nav-logo-text">A</span></div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="ti-nav-links">
            <a className="active">관광정보</a>
            <a onClick={() => onNavigate("map")}>관광동선</a>
            <a onClick={() => onNavigate("store")}>스토어</a>
            <a onClick={() => onNavigate("ticket")}>티켓</a>
          </div>
        </div>
        <div className="ti-nav-setting">설정</div>
      </nav>

      {/* Hero */}
      <section className="ti-hero">
        <img
          src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1400&q=80&fit=crop"
          alt="충북 관광"
        />
        <div className="ti-hero-overlay">
          <span className="ti-hero-tag">충청북도 관광정보</span>
          <h1>자연과 역사가 숨쉬는<br />충청북도</h1>
          <p>청주부터 단양까지, 충북의 숨겨진 보석 같은 명소를 AI와 함께 탐험하세요</p>
        </div>
      </section>

      {/* Category Filter */}
      <section className="ti-filter">
        {CATEGORIES.map((c) => (
          <button key={c} className={`ti-filter-btn ${c === "전체" ? "active" : ""}`}>{c}</button>
        ))}
      </section>

      {/* Spots Grid */}
      <section className="ti-spots">
        <div className="ti-spots-header">
          <h2>충북 추천 명소</h2>
          <span className="ti-spots-count">{SPOTS.length}곳</span>
        </div>
        <div className="ti-grid">
          {SPOTS.map((s) => (
            <div className="ti-card" key={s.name}>
              {s.name === "법주사" && (
                <div className="ti-event-badge">
                  <span className="ti-event-badge-label">· EVENT ·</span>
                  <span className="ti-event-badge-pct">50%</span>
                  <span className="ti-event-badge-off">OFF</span>
                </div>
              )}
              <div className="ti-card-img">
                <img src={s.img} alt={s.name} />
                <span className="ti-card-category">{s.category}</span>
              </div>
              <div className="ti-card-body">
                <div className="ti-card-region">{s.region}</div>
                <h3 className="ti-card-name">{s.name}</h3>
                <p className="ti-card-desc">{s.desc}</p>
                <button className="ti-card-btn" onClick={() => onViewSpot(s)}>AI 가이드 보기</button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* AI Banner */}
      <section className="ti-ai-banner">
        <div className="ti-ai-content">
          <h2>AI와 함께하는 스마트 관광</h2>
          <p>원하는 명소에 대해 궁금한 점을 AI에게 물어보세요.<br />역사, 교통, 맛집까지 실시간으로 안내해드립니다.</p>
          <button className="ti-ai-btn">AI와 대화하기</button>
        </div>
      </section>
    </div>
  );
}
