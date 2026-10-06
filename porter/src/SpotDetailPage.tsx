import { useState } from "react";
import "./SpotDetailPage.css";
import { DETAIL_DATA } from "./spotDetailData";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking" | "spotdetail";

export type Spot = {
  name: string;
  region: string;
  category: string;
  desc: string;
  img: string;
};

type Props = {
  onNavigate: (page: Page) => void;
  spot: Spot;
};

const TABS = ["개요", "위치", "주요시설", "FAQ"];

export default function SpotDetailPage({ onNavigate, spot }: Props) {
  const [activeTab, setActiveTab] = useState("개요");
  const [menuOpen, setMenuOpen] = useState(false);
  const [reviewsOpen, setReviewsOpen] = useState(false);
  const detail = DETAIL_DATA[spot.name] ?? DETAIL_DATA["속리산 국립공원"];

  const renderTabContent = () => {
    if (activeTab === "개요") {
      return (
        <div className="sd-tab-content">
          <div>
            <h2 className="sd-section-title">이런 분께 추천해요</h2>
            <p className="sd-section-text">{detail.overview}</p>
          </div>
          <div>
            <h2 className="sd-features-title">주요 시설</h2>
            <div className="sd-features-grid">
              {detail.features.map((f) => (
                <div className="sd-feature-item" key={f.label}>
                  <span className="sd-feature-icon">{f.icon}</span>
                  <span>{f.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      );
    }
    if (activeTab === "위치") {
      return (
        <div className="sd-tab-content">
          <div>
            <h2 className="sd-section-title">위치 정보</h2>
            <div className="sd-location-addr">
              <span>📍</span>
              <span>{detail.address}</span>
            </div>
            <div className="sd-map-wrap">
              <iframe
                title="지도"
                src="https://www.openstreetmap.org/export/embed.html?bbox=127.0%2C36.3%2C128.6%2C37.3&layer=mapnik"
              />
            </div>
          </div>
        </div>
      );
    }
    if (activeTab === "주요시설") {
      return (
        <div className="sd-tab-content">
          <div>
            <h2 className="sd-features-title">시설 및 특징</h2>
            <div className="sd-features-grid">
              {detail.features.map((f) => (
                <div className="sd-feature-item" key={f.label}>
                  <span className="sd-feature-icon">{f.icon}</span>
                  <span>{f.label}</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h2 className="sd-section-title">운영 정보</h2>
            <p className="sd-section-text">운영 시간: {detail.hours}</p>
          </div>
        </div>
      );
    }
    if (activeTab === "FAQ") {
      return (
        <div className="sd-tab-content">
          <h2 className="sd-section-title">자주 묻는 질문</h2>
          {detail.faq.map((item) => (
            <div className="sd-faq-item" key={item.q}>
              <div className="sd-faq-q">Q. {item.q}</div>
              <div className="sd-faq-a">A. {item.a}</div>
            </div>
          ))}
        </div>
      );
    }
  };

  return (
    <div className="sd-page">
      {/* Navbar */}
      <nav className="sd-nav">
        <div className="sd-nav-left">
          <div className="sd-nav-brand" onClick={() => onNavigate("landing")}>
            <div className="nav-logo-circle"><span className="nav-logo-text">A</span></div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="sd-nav-links">
            <a className="active" onClick={() => onNavigate("tourinfo")}>관광정보</a>
            <a onClick={() => onNavigate("map")}>관광동선</a>
            <a onClick={() => onNavigate("store")}>스토어</a>
            <a onClick={() => onNavigate("ticket")}>티켓</a>
          </div>
        </div>
        <div className="sd-nav-right">
          <button className="sd-hamburger" onClick={() => setMenuOpen(v => !v)} aria-label="메뉴">
            <span /><span /><span />
          </button>
        </div>
      </nav>

      {/* 모바일 드롭다운 메뉴 */}
      {menuOpen && (
        <div className="sd-mobile-menu">
          <a onClick={() => { onNavigate("tourinfo"); setMenuOpen(false); }}>관광정보</a>
          <a onClick={() => { onNavigate("map"); setMenuOpen(false); }}>관광동선</a>
          <a onClick={() => { onNavigate("store"); setMenuOpen(false); }}>스토어</a>
          <a onClick={() => { onNavigate("ticket"); setMenuOpen(false); }}>티켓</a>
        </div>
      )}

      {/* Hero: full-height, card on left */}
      <div className="sd-hero">
        <img className="sd-hero-bg" src={spot.img.replace("w=600", "w=1400").replace("q=80", "q=90")} alt={spot.name} />
        <div className="sd-hero-card">
          <span className="sd-hero-category">{spot.category}</span>
          <h1 className="sd-hero-title">{spot.name}</h1>
          <p className="sd-hero-desc">{spot.desc}</p>
          <div className="sd-hero-meta">
            <div className="sd-meta-row">
              <span>📍</span>
              <span>{detail.address}</span>
            </div>
            <div className="sd-meta-row">
              <span>⭐</span>
              <span>{detail.rating} ({detail.reviewCount.toLocaleString()}개 리뷰)</span>
            </div>
            <div className="sd-meta-row">
              <span>🕐</span>
              <span>{detail.hours}</span>
            </div>
            <div className="sd-meta-row">
              <span>🗺️</span>
              <span>{detail.guide}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs + Review */}
      <div className="sd-body">
        <div className="sd-left">
          <div className="sd-tabs">
            {TABS.map((t) => (
              <button
                key={t}
                className={`sd-tab-btn${activeTab === t ? " active" : ""}`}
                onClick={() => setActiveTab(t)}
              >
                {t}
              </button>
            ))}
          </div>
          {renderTabContent()}
        </div>

        {/* Reviews */}
        <aside className="sd-review-panel">
          <div className="sd-review-header">리뷰 및 평점</div>
          <div className="sd-review-score">
            <span className="sd-score-num">{detail.rating}</span>
            <div>
              <div className="sd-stars">{"★".repeat(Math.round(detail.rating))}{"☆".repeat(5 - Math.round(detail.rating))}</div>
              <div className="sd-score-sub">{detail.reviewCount.toLocaleString()}개 리뷰 기준</div>
            </div>
          </div>
          <div className="sd-breakdown">
            {detail.ratingBreakdown.map((r) => (
              <div className="sd-breakdown-row" key={r.label}>
                <span className="sd-breakdown-label">{r.label}</span>
                <div className="sd-breakdown-bar">
                  <div className="sd-breakdown-fill" style={{ width: `${(r.score / 5) * 100}%` }} />
                </div>
                <span className="sd-breakdown-score">{r.score}</span>
              </div>
            ))}
          </div>
          <div className={`sd-review-list${reviewsOpen ? " sd-review-list--open" : ""}`}>
            {detail.reviews.slice(0, 2).map((rv) => (
              <div className="sd-review-item" key={rv.name + rv.date}>
                <div className="sd-review-top">
                  <div className="sd-reviewer-avatar">{rv.name[0]}</div>
                  <div>
                    <div className="sd-reviewer-name">{rv.name}</div>
                    <div className="sd-reviewer-date">{rv.date}</div>
                  </div>
                  <div className="sd-reviewer-stars">{"★".repeat(rv.rating)}</div>
                </div>
                <p className="sd-review-text">{rv.text}</p>
              </div>
            ))}
          </div>
          <button className="sd-see-reviews-btn" onClick={() => setReviewsOpen(v => !v)}>
            {reviewsOpen ? "리뷰 접기" : "리뷰 보기"}
          </button>
        </aside>
      </div>
    </div>
  );
}
