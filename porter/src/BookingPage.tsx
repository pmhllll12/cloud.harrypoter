import { useState } from "react";
import "./BookingPage.css";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking";

export type Ticket = {
  name: string;
  region: string;
  category: string;
  price: number;
  duration: string;
  rating: number;
  reviews: number;
  img: string;
  badge: string;
};

type Props = {
  onNavigate: (page: Page) => void;
  ticket: Ticket;
  allTickets: Ticket[];
};

const CATEGORIES = ["전체", "액티비티", "자연탐방", "문화유산", "음식체험"];

const RESULT_CATS = [
  { label: "관광지",   category: "자연탐방", icon: "🏔️", color: "#2E7D52", bg: "#F0F7F4" },
  { label: "문화유산", category: "문화유산", icon: "🏛️", color: "#7D4A4A", bg: "#FAF5F0" },
  { label: "액티비티", category: "액티비티", icon: "🪂", color: "#2A6EA4", bg: "#F0F5FA" },
  { label: "음식점",   category: "음식체험", icon: "🍽️", color: "#8B5E1A", bg: "#FAF7EF" },
];

export default function BookingPage({ onNavigate, ticket, allTickets }: Props) {
  const [activeCategory, setActiveCategory] = useState("전체");
  const [guests, setGuests] = useState(2);
  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = () => {
    setSearched(true);
    setActiveCategory("전체");
  };

  const filtered = allTickets.filter((t) => {
    if (activeCategory !== "전체" && t.category !== activeCategory) return false;
    if (minPrice && t.price < Number(minPrice)) return false;
    if (maxPrice && t.price > Number(maxPrice)) return false;
    return true;
  });

  return (
    <div className="bk-page">
      {/* Navbar */}
      <nav className="bk-nav">
        <div className="bk-nav-left">
          <div className="bk-nav-brand" onClick={() => onNavigate("landing")}>
            <div className="nav-logo-circle"><span className="nav-logo-text">A</span></div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="bk-nav-links">
            <a onClick={() => onNavigate("tourinfo")}>관광정보</a>
            <a onClick={() => onNavigate("map")}>관광동선</a>
            <a onClick={() => onNavigate("store")}>스토어</a>
            <a className="active" onClick={() => onNavigate("ticket")}>티켓</a>
          </div>
        </div>
        <div className="bk-nav-right">
          <div className="bk-nav-setting">설정</div>
          <button className="bk-hamburger" onClick={() => setMenuOpen(v => !v)} aria-label="메뉴">
            <span /><span /><span />
          </button>
        </div>
      </nav>
      {menuOpen && (
        <div className="bk-mobile-menu">
          <a onClick={() => { onNavigate("tourinfo"); setMenuOpen(false); }}>관광정보</a>
          <a onClick={() => { onNavigate("map"); setMenuOpen(false); }}>관광동선</a>
          <a onClick={() => { onNavigate("store"); setMenuOpen(false); }}>스토어</a>
          <a onClick={() => { onNavigate("ticket"); setMenuOpen(false); }}>티켓</a>
          <a onClick={() => setMenuOpen(false)}>설정</a>
        </div>
      )}

      {/* Search bar */}
      <div className="bk-search-bar">
        <div className="bk-search-field">
          <span className="bk-search-label">장소</span>
          <span className="bk-search-value">{ticket.region}</span>
        </div>
        <div className="bk-search-divider" />
        <div className="bk-search-field">
          <span className="bk-search-label">방문일</span>
          <input
            className="bk-search-input"
            type="date"
            value={checkIn}
            onChange={(e) => setCheckIn(e.target.value)}
          />
        </div>
        <div className="bk-search-divider" />
        <div className="bk-search-field">
          <span className="bk-search-label">방문 종료</span>
          <input
            className="bk-search-input"
            type="date"
            value={checkOut}
            onChange={(e) => setCheckOut(e.target.value)}
          />
        </div>
        <div className="bk-search-divider" />
        <div className="bk-search-field">
          <span className="bk-search-label">인원</span>
          <div className="bk-guests-ctrl">
            <button onClick={() => setGuests((g) => Math.max(1, g - 1))}>−</button>
            <span>{guests}명</span>
            <button onClick={() => setGuests((g) => g + 1)}>+</button>
          </div>
        </div>
        <button className="bk-search-btn" onClick={handleSearch}>검색</button>
      </div>

      {/* 검색 후 카테고리 선택 화면 */}
      {searched && activeCategory === "전체" && (
        <section className="bk-result-cats-section">
          <div className="bk-result-cats-header">
            <span className="bk-result-cats-region"><strong>{ticket.region}</strong> 검색 결과</span>
            <span className="bk-result-cats-total">총 {allTickets.length}개의 체험</span>
          </div>
          <div className="bk-result-cats-grid">
            {RESULT_CATS.map(({ label, category, icon, color, bg }) => {
              const count = allTickets.filter((t) => t.category === category).length;
              return (
                <button
                  key={label}
                  className="bk-result-cat-card"
                  style={{ background: bg, borderColor: color + "44" }}
                  onClick={() => setActiveCategory(category)}
                >
                  <span className="bk-result-cat-icon">{icon}</span>
                  <span className="bk-result-cat-label" style={{ color }}>{label}</span>
                  <span className="bk-result-cat-count" style={{ color }}>{count}개</span>
                </button>
              );
            })}
          </div>
        </section>
      )}

      {/* 카테고리 선택 후 목록 */}
      {(!searched || activeCategory !== "전체") && (
      <>

      {/* Results header */}
      <div className="bk-results-header">
        {searched && (
          <button className="bk-back-btn" onClick={() => setActiveCategory("전체")}>
            ← 카테고리
          </button>
        )}
        <span className="bk-results-count">
          <strong>{ticket.region}</strong> 근처에서 <strong>{filtered.length}개</strong>의 체험을 찾았습니다
        </span>
        <div className="bk-view-btns">
          <button className="bk-view-btn">필터</button>
          <button className="bk-view-btn active">목록 보기</button>
        </div>
      </div>

      {/* Category tabs */}
      <div className="bk-category-tabs">
        {CATEGORIES.map((c) => (
          <button
            key={c}
            className={`bk-cat-tab${activeCategory === c ? " active" : ""}`}
            onClick={() => setActiveCategory(c)}
          >
            {c}
          </button>
        ))}
      </div>

      {/* Main: grid + filter */}
      <div className="bk-main">
        {/* Card grid */}
        <div className="bk-grid">
          {filtered.map((t) => (
            <div className={`bk-card${t.name === ticket.name ? " bk-card--selected" : ""}`} key={t.name}>
              <div className="bk-card-img">
                <img src={t.img} alt={t.name} />
                {t.badge && <span className="bk-badge">{t.badge}</span>}
                <span className="bk-cat-tag">{t.category}</span>
              </div>
              <div className="bk-card-body">
                <div className="bk-card-region">{t.region}</div>
                <div className="bk-card-name">{t.name}</div>
                <div className="bk-card-meta">
                  <span className="bk-star">★ {t.rating}</span>
                  <span className="bk-review">({t.reviews})</span>
                  <span className="bk-dur">· {t.duration}</span>
                </div>
                <div className="bk-card-footer">
                  <span className="bk-price">
                    <strong>{t.price.toLocaleString()}</strong>원~
                  </span>
                  <button
                    className={`bk-select-btn${t.name === ticket.name ? " bk-select-btn--active" : ""}`}
                  >
                    {t.name === ticket.name ? "선택됨" : "선택하기"}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Filter panel */}
        <aside className="bk-filter-panel">
          <div className="bk-filter-header">
            <span>필터</span>
            <button className="bk-filter-clear">전체 초기화</button>
          </div>

          <div className="bk-filter-section">
            <div className="bk-filter-title">가격 범위</div>
            <p className="bk-filter-desc">1인 기준 체험 가격</p>
            <div className="bk-price-inputs">
              <div className="bk-price-box">
                <span className="bk-price-box-label">최소</span>
                <input
                  className="bk-price-input"
                  placeholder="0"
                  value={minPrice}
                  onChange={(e) => setMinPrice(e.target.value)}
                />
                <span>원</span>
              </div>
              <div className="bk-price-box">
                <span className="bk-price-box-label">최대</span>
                <input
                  className="bk-price-input"
                  placeholder="100,000"
                  value={maxPrice}
                  onChange={(e) => setMaxPrice(e.target.value)}
                />
                <span>원</span>
              </div>
            </div>
          </div>

          <div className="bk-filter-section">
            <div className="bk-filter-title">체험 유형</div>
            <div className="bk-checkbox-grid">
              {["액티비티", "자연탐방", "문화유산", "음식체험"].map((cat) => (
                <label key={cat} className="bk-checkbox-label">
                  <input
                    type="checkbox"
                    checked={activeCategory === cat || activeCategory === "전체"}
                    onChange={() => setActiveCategory(activeCategory === cat ? "전체" : cat)}
                  />
                  <span>{cat}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="bk-filter-section">
            <div className="bk-filter-title">소요시간</div>
            <div className="bk-duration-btns">
              {["전체", "1시간", "2시간", "3시간 이상"].map((d) => (
                <button key={d} className="bk-dur-btn">{d}</button>
              ))}
            </div>
          </div>

          <div className="bk-filter-section">
            <div className="bk-filter-title">평점</div>
            <div className="bk-duration-btns">
              {["전체", "4.5+", "4.7+", "4.9+"].map((r) => (
                <button key={r} className="bk-dur-btn">{r}</button>
              ))}
            </div>
          </div>

          <button className="bk-confirm-btn" onClick={() => alert(`${ticket.name} 예약이 완료되었습니다!`)}>
            예약 확정하기
          </button>
        </aside>
      </div>

      </> /* end (!searched || activeCategory !== "전체") */
      )}
    </div>
  );
}
