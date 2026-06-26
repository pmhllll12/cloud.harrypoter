import { useState } from "react";
import "./StorePage.css";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking" | "spotdetail";
type Props = { onNavigate: (page: Page) => void };

const PRODUCTS = [
  {
    name: "Cheongju Market",
    img: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80&fit=crop",
  },
  {
    name: "Café Sori",
    img: "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600&q=80&fit=crop",
  },
  {
    name: "Maison Boeun",
    img: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&q=80&fit=crop",
  },
  {
    name: "Danyang Table",
    img: "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&q=80&fit=crop",
  },
];

export default function StorePage({ onNavigate }: Props) {
  const [menuOpen, setMenuOpen] = useState(false);
  return (
    <div className="store-page">
      {/* Navbar */}
      <nav className="store-nav">
        <div className="store-nav-left">
          <div className="store-nav-brand" onClick={() => onNavigate("landing")}>
            <div className="nav-logo-circle">
              <span className="nav-logo-text">A</span>
            </div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="store-nav-links">
            <a onClick={() => onNavigate("tourinfo")}>관광정보</a>
            <a onClick={() => onNavigate("map")}>관광동선</a>
            <a className="active">스토어</a>
            <a onClick={() => onNavigate("ticket")}>티켓</a>
          </div>
        </div>
        <div className="store-nav-right">
          <button className="store-hamburger" onClick={() => setMenuOpen(v => !v)} aria-label="메뉴">
            <span /><span /><span />
          </button>
        </div>
      </nav>
      {menuOpen && (
        <div className="store-mobile-menu">
          <a onClick={() => { onNavigate("tourinfo"); setMenuOpen(false); }}>관광정보</a>
          <a onClick={() => { onNavigate("map"); setMenuOpen(false); }}>관광동선</a>
          <a onClick={() => { onNavigate("store"); setMenuOpen(false); }}>스토어</a>
          <a onClick={() => { onNavigate("ticket"); setMenuOpen(false); }}>티켓</a>
        </div>
      )}

      {/* Hero */}
      <section className="store-hero">
        <img src="/store-hero.jpg" alt="스토어" />
        <div className="store-hero-overlay">
          <h1>스토어</h1>
          <p>전국의 특별한 경험을 담은 상품과 투어 티켓을 만나보세요</p>
          <a href="#products" className="store-hero-btn">상품 보기</a>
        </div>
      </section>

      {/* Products */}
      <section className="store-products" id="products">
        <div className="store-section-header">
          <h2>Korea Store</h2>
          <div className="store-arrows">
            <button className="store-arrow-btn">←</button>
            <button className="store-arrow-btn">→</button>
          </div>
        </div>
        <div className="product-grid">
          {PRODUCTS.map((p) => (
            <div className="product-card" key={p.name}>
              <div className="product-img-wrap">
                <img src={p.img} alt={p.name} className="product-photo" />
              </div>
              <p className="product-name">{p.name}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Featured */}
      <section className="store-featured">
        <div className="store-featured-img">
          <img src="/store-featured.jpg" alt="속리산 트레킹" />
        </div>
        <div className="store-featured-content">
          <span className="featured-tag">대표 상품</span>
          <h2>속리산에서 만나는<br />최고의 트레킹 경험</h2>
          <p>
            천년의 역사를 품은 법주사와 웅장한 속리산 국립공원을 전문 가이드와 함께 탐험해보세요.
            해발 1,058m의 장엄한 봉우리와 울창한 원시림이 만들어내는 절경은 대한민국 최고의 자연 명소입니다.
          </p>
          <p>
            당일 코스부터 1박 2일 심화 트레킹까지 다양한 프로그램으로 운영됩니다.
            법주사 팔상전과 미륵대불을 포함한 문화유산 해설도 함께 제공되어,
            자연과 역사를 동시에 즐길 수 있는 특별한 경험이 될 것입니다.
          </p>
          <a href="#products" className="store-featured-btn">상품 보기</a>
        </div>
      </section>
    </div>
  );
}
