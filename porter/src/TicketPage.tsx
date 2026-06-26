import { useState } from "react";
import "./TicketPage.css";
import type { Ticket } from "./BookingPage";
import ChatModal from "./ChatModal";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking";
type Props = { onNavigate: (page: Page) => void; onBook: (ticket: Ticket) => void };

const TICKETS = [
  {
    name: "단양 패러글라이딩 체험",
    region: "충북 단양",
    category: "액티비티",
    price: 80000,
    duration: "약 2시간",
    rating: 4.9,
    reviews: 312,
    img: "https://images.unsplash.com/photo-1601024445121-e5b82f020549?w=600&q=80&fit=crop",
    badge: "인기",
  },
  {
    name: "속리산 가이드 트레킹",
    region: "충북 보은",
    category: "자연탐방",
    price: 35000,
    duration: "약 5시간",
    rating: 4.8,
    reviews: 187,
    img: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=80&fit=crop",
    badge: "추천",
  },
  {
    name: "법주사 문화유산 해설 투어",
    region: "충북 보은",
    category: "문화유산",
    price: 15000,
    duration: "약 2시간",
    rating: 4.7,
    reviews: 243,
    img: "https://images.unsplash.com/photo-1548115184-bc6544d06a58?w=600&q=80&fit=crop",
    badge: "",
  },
  {
    name: "청주 한과 만들기 체험",
    region: "충북 청주",
    category: "음식체험",
    price: 25000,
    duration: "약 1.5시간",
    rating: 4.6,
    reviews: 98,
    img: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80&fit=crop",
    badge: "",
  },
  {
    name: "충주호 유람선 투어",
    region: "충북 충주",
    category: "자연탐방",
    price: 18000,
    duration: "약 1시간",
    rating: 4.5,
    reviews: 156,
    img: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=600&q=80&fit=crop&auto=format",
    badge: "",
  },
  {
    name: "괴산 산막이옛길 트레킹",
    region: "충북 괴산",
    category: "자연탐방",
    price: 20000,
    duration: "약 3시간",
    rating: 4.8,
    reviews: 201,
    img: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&q=80&fit=crop",
    badge: "추천",
  },
];

const CATEGORIES = ["전체", "액티비티", "자연탐방", "문화유산", "음식체험"];

export default function TicketPage({ onNavigate, onBook }: Props) {
  const [chatOpen, setChatOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  return (
    <div className="ticket-page">
      <nav className="tk-nav">
        <div className="tk-nav-left">
          <div className="tk-nav-brand" onClick={() => onNavigate("landing")}>
            <div className="nav-logo-circle"><span className="nav-logo-text">A</span></div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="tk-nav-links">
            <a onClick={() => onNavigate("tourinfo")}>관광정보</a>
            <a onClick={() => onNavigate("map")}>관광동선</a>
            <a onClick={() => onNavigate("store")}>스토어</a>
            <a className="active">티켓</a>
          </div>
        </div>
        <div className="tk-nav-right">
          <button className="tk-hamburger" onClick={() => setMenuOpen(v => !v)} aria-label="메뉴">
            <span /><span /><span />
          </button>
        </div>
      </nav>
      {menuOpen && (
        <div className="tk-mobile-menu">
          <a onClick={() => { onNavigate("tourinfo"); setMenuOpen(false); }}>관광정보</a>
          <a onClick={() => { onNavigate("map"); setMenuOpen(false); }}>관광동선</a>
          <a onClick={() => { onNavigate("store"); setMenuOpen(false); }}>스토어</a>
          <a onClick={() => { onNavigate("ticket"); setMenuOpen(false); }}>티켓</a>
        </div>
      )}

      {/* Hero */}
      <section className="tk-hero">
        <img
          src="https://images.unsplash.com/photo-1601024445121-e5b82f020549?w=1400&q=80&fit=crop"
          alt="체험 티켓"
        />
        <div className="tk-hero-overlay">
          <span className="tk-hero-tag">체험 티켓</span>
          <h1>대한민국의 특별한 순간을<br />예약하세요</h1>
          <p>패러글라이딩부터 문화유산 투어까지, 잊지 못할 전국 여행 경험을 지금 바로 시작하세요</p>
        </div>
      </section>

      {/* Stats */}
      <section className="tk-stats">
        <div className="tk-stat"><strong>6+</strong><span>체험 프로그램</span></div>
        <div className="tk-stat-divider" />
        <div className="tk-stat"><strong>1,197+</strong><span>누적 리뷰</span></div>
        <div className="tk-stat-divider" />
        <div className="tk-stat"><strong>4.7★</strong><span>평균 만족도</span></div>
        <div className="tk-stat-divider" />
        <div className="tk-stat"><strong>즉시</strong><span>예약 확정</span></div>
      </section>

      {/* Category */}
      <section className="tk-body">
        <div className="tk-filter">
          {CATEGORIES.map((c) => (
            <button key={c} className={`tk-filter-btn ${c === "전체" ? "active" : ""}`}>{c}</button>
          ))}
        </div>

        <div className="tk-grid">
          {TICKETS.map((t) => (
            <div className="tk-card" key={t.name}>
              <div className="tk-card-img">
                <img src={t.img} alt={t.name} />
                {t.badge && <span className="tk-badge">{t.badge}</span>}
                <span className="tk-category-tag">{t.category}</span>
              </div>
              <div className="tk-card-body">
                <div className="tk-card-region">{t.region}</div>
                <h3 className="tk-card-name">{t.name}</h3>
                <div className="tk-card-meta">
                  <span className="tk-rating">★ {t.rating}</span>
                  <span className="tk-reviews">({t.reviews})</span>
                  <span className="tk-duration">· {t.duration}</span>
                </div>
                <div className="tk-card-footer">
                  <div className="tk-price">
                    <span className="tk-price-num">{t.price.toLocaleString()}</span>
                    <span className="tk-price-unit">원~</span>
                  </div>
                  <button className="tk-book-btn" onClick={() => onBook(t)}>예약하기</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Banner */}
      <section className="tk-cta">
        <h2>AI에게 맞춤 코스를 추천받으세요</h2>
        <p>여행 날짜, 인원, 관심사를 알려주시면 AI가 최적의 전국 여행 코스를 만들어드립니다.</p>
        <button className="tk-cta-btn" onClick={() => setChatOpen(true)}>AI와 대화하기</button>
      </section>

      <ChatModal open={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  );
}
