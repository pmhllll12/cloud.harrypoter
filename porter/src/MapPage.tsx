import "./MapPage.css";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket";
type Props = { onNavigate: (page: Page) => void };

const SPOTS = [
  {
    tag: "추천" as const,
    title: "속리산 국립공원",
    region: "보은",
    guide: "AI 관광 가이드",
    progress: 92,
  },
  {
    tag: "추천" as const,
    title: "법주사",
    region: "보은",
    guide: "AI 관광 가이드",
    progress: 85,
  },
  {
    tag: "진행 중" as const,
    title: "단양 패러글라이딩",
    region: "단양",
    guide: "AI 관광 가이드",
    progress: 60,
  },
  {
    tag: "진행 중" as const,
    title: "청주 고인쇄박물관",
    region: "청주",
    guide: "AI 관광 가이드",
    progress: 74,
  },
];

export default function MapPage({ onNavigate }: Props) {
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
        <img src="/palace.jpg" alt="한국 관광" />
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

        {/* Center: search + map */}
        <div className="map-center">
          <div className="map-search-row">
            <span className="map-search-label">관광지 검색</span>
            <input className="map-search-input" placeholder="검색..." />
            <button className="map-filter-btn">필터</button>
          </div>
          <div className="map-container">
            <iframe
              title="한국 지도"
              src="https://www.openstreetmap.org/export/embed.html?bbox=127.0%2C36.3%2C128.6%2C37.3&layer=mapnik&marker=36.6424%2C127.4890"
            />
          </div>
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
