import { useState, useEffect, useRef } from "react";
import { MapContainer, TileLayer, useMap, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./MapPage.css";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking" | "spotdetail";
type Props = { onNavigate: (page: Page) => void };

type Festival = {
  name: string;
  period: string;
  location: string;
  desc: string;
};

type Spot = {
  tag: "추천" | "진행 중";
  title: string;
  region: string;
  province: string;
  guide: string;
  progress: number;
  category: string;
  year: number;
  theme: string;
  era: string;
  method: string;
  provider: string;
  overview: string;
  description: string;
  coordinates: [number, number];
  images: string[];
  vrSrc?: string;
  festivals: Festival[];
};

type Message = { role: "user" | "ai"; text: string };

const REGIONS: string[] = [
  "강원도", "경기도", "경상남도", "경상북도", "광주광역시",
  "대구광역시", "대전광역시", "부산광역시", "서울특별시", "세종특별자치시",
  "울산광역시", "인천광역시", "전라남도", "전북특별자치도", "제주특별자치도",
  "충청남도", "충청북도",
];

const SPOTS: Spot[] = [
  {
    tag: "추천",
    title: "속리산 국립공원",
    region: "충북 보은",
    province: "충청북도",
    coordinates: [36.5427, 127.8905],
    guide: "AI 관광 가이드",
    progress: 92,
    category: "국립공원",
    year: 2026,
    theme: "자연생태·산악",
    era: "현대",
    method: "현장탐방, 트레킹",
    provider: "국립공원공단",
    overview: "속리산 국립공원은 충청북도 보은군에 위치한 대한민국 제6호 국립공원입니다. 천왕봉(1,058m)을 주봉으로 비로봉, 길상봉 등 8개 봉우리로 이루어진 산으로 법주사, 세조길 등 다양한 역사·문화 자원을 품고 있습니다.",
    description: "속리산은 1970년 국립공원으로 지정되었으며, 우리나라에서 손꼽히는 명산으로 '속세를 벗어난 산'이라는 뜻을 지니고 있습니다. 화강암 암봉과 울창한 산림이 조화를 이루며, 봄에는 진달래와 철쭉, 가을에는 단풍이 절경을 이룹니다. 정이품송(천연기념물 제103호)을 비롯해 천연기념물과 명승지가 다수 포함되어 있으며, 연간 200만 명 이상의 탐방객이 방문하는 충청도 대표 관광지입니다.",
    images: [
      "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Songnisan.jpg/1280px-Songnisan.jpg",
      "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1542086094-a61c1ab7c4b8?w=900&q=80&fit=crop",
    ],
    festivals: [
      {
        name: "속리산 철쭉제",
        period: "5월 초·중순",
        location: "충북 보은군 속리산면",
        desc: "속리산 천왕봉 일대에 피어나는 철쭉을 주제로 한 봄 축제. 등산 대회, 사생 대회, 지역 특산물 장터가 함께 열립니다.",
      },
      {
        name: "보은 대추 축제",
        period: "10월 초·중순",
        location: "충북 보은군 보은읍",
        desc: "보은 대추는 왕실 진상품으로 유명합니다. 대추 따기 체험, 다양한 대추 가공 식품 시식, 지역 문화 공연을 즐길 수 있습니다.",
      },
      {
        name: "속리산 단풍 축제",
        period: "10월 하순 ~ 11월 초",
        location: "충북 보은군 속리산면",
        desc: "천왕봉과 법주사 주변을 물들이는 단풍 절경을 감상하는 가을 축제. 야간 단풍 투어와 포토존이 인기입니다.",
      },
    ],
  },
  {
    tag: "추천",
    title: "법주사",
    region: "충북 보은",
    province: "충청북도",
    coordinates: [36.5410, 127.8985],
    guide: "AI 관광 가이드",
    progress: 85,
    category: "사적",
    year: 2026,
    theme: "불교문화·건축",
    era: "삼국시대",
    method: "고증, 원형",
    provider: "문화재청",
    overview: "법주사는 충청북도 보은군 속리산에 위치한 신라시대 고찰로, 553년(진흥왕 14)에 의신조사가 창건한 사찰입니다. 팔상전(국보 제55호)을 비롯해 대웅보전, 원통보전 등 다수의 국보·보물이 보존되어 있습니다.",
    description: "법주사는 '부처님의 법이 머무는 곳'이라는 뜻으로, 신라 진흥왕 14년(553년) 의신조사에 의해 창건되었습니다. 우리나라 유일의 목조 5층 탑인 팔상전(국보 제55호)이 있으며, 거대한 금동미륵대불(33m)로도 유명합니다. 경내에는 석련지(국보 제64호), 쌍사자석등(국보 제5호) 등 국보 3점과 다수의 보물이 보존되어 있어 한국 불교 문화의 정수를 만날 수 있습니다. 2018년 유네스코 세계유산 '산사, 한국의 산지승원' 7개소 중 하나로 등재되었습니다.",
    images: [
      "https://images.unsplash.com/photo-1548115184-bc6544d06a58?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1684134549350-be5fd0d8feaa?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1638964663550-e2123ac8900b?w=900&q=80&fit=crop",
    ],
    festivals: [
      {
        name: "법주사 연등 축제",
        period: "5월 (부처님 오신 날 전후)",
        location: "충북 보은군 법주사",
        desc: "경내를 가득 채우는 연등 행렬과 소원 연등 달기 행사. 야간에 수천 개의 연등이 켜지면 환상적인 분위기를 연출합니다.",
      },
      {
        name: "보은 속리산 문화제",
        period: "10월 중순",
        location: "충북 보은군 보은읍·속리산",
        desc: "지역 전통문화와 민속 공연, 향토 음식 체험이 어우러진 종합 문화 행사. 속리산 트레킹과 연계 운영됩니다.",
      },
      {
        name: "세계유산 산사 문화제",
        period: "연중 (계절별)",
        location: "전국 7개 산사 (법주사 포함)",
        desc: "유네스코 세계유산 등재 기념으로 열리는 산사 문화 체험 프로그램. 템플스테이, 불교 미술 전시, 명상 체험 등을 운영합니다.",
      },
    ],
  },
  {
    tag: "진행 중",
    title: "단양 패러글라이딩",
    region: "충북 단양",
    province: "충청북도",
    coordinates: [36.9879, 128.3707],
    guide: "AI 관광 가이드",
    progress: 60,
    category: "레저스포츠",
    year: 2026,
    theme: "레저·액티비티",
    era: "현대",
    method: "체험형",
    provider: "단양군청",
    overview: "단양 소백산 패러글라이딩은 소백산 국립공원을 배경으로 단양강(남한강)의 절경을 하늘에서 감상할 수 있는 레저 스포츠 체험입니다. 도담삼봉, 구담봉 등 단양 8경을 조망하며 비행하는 특별한 경험을 제공합니다.",
    description: "충청북도 단양군은 남한강과 소백산이 어우러진 천혜의 경관을 자랑합니다. 패러글라이딩 이륙장에서 도약하면 도담삼봉, 석문, 구담봉 등 단양 8경을 한눈에 조망할 수 있습니다. 전문 조종사와 함께 탑승하는 2인 탠덤 비행으로 누구나 안전하게 즐길 수 있으며, 약 10~20분간의 비행 코스를 운영합니다. 봄·가을이 최고 성수기이며, 맑은 날에는 소백산 능선과 굽이치는 단양강의 절경이 장관을 이룹니다.",
    images: [
      "https://images.unsplash.com/photo-1601024445121-e5b82f020549?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1533240332313-0db49b459ad6?w=900&q=80&fit=crop",
    ],
    festivals: [
      {
        name: "단양 소백산 철쭉제",
        period: "5월 중·하순",
        location: "충북 단양군 소백산 비로봉",
        desc: "소백산 비로봉 일대를 분홍빛으로 뒤덮는 철쭉 군락을 감상하는 봄 축제. 산신제, 가요제, 포토 경연 대회가 함께 열립니다.",
      },
      {
        name: "단양 마늘 축제",
        period: "6월 초·중순",
        location: "충북 단양군 단양읍",
        desc: "단양의 특산물 마늘을 주제로 한 특산물 축제. 마늘 떡메치기, 마늘 요리 경연, 마늘 테마 체험 부스가 운영됩니다.",
      },
      {
        name: "온달 문화 축제",
        period: "10월 초·중순",
        location: "충북 단양군 영춘면 온달산성",
        desc: "고구려 장수 온달과 평강공주 설화를 테마로 한 역사문화 축제. 마상 무예 공연, 온달관광지 투어, 남한강 뗏목 체험이 인기입니다.",
      },
    ],
  },
  {
    tag: "추천",
    title: "종묘",
    region: "서울 종로",
    province: "서울특별시",
    coordinates: [37.5747, 126.9945],
    guide: "AI 관광 가이드",
    progress: 95,
    category: "세계유산",
    year: 2026,
    theme: "왕실문화·제례",
    era: "조선시대",
    method: "원형보존, 현장탐방",
    provider: "문화재청",
    overview: "종묘는 조선 역대 왕과 왕비의 신주를 봉안한 왕실 사당으로, 1995년 유네스코 세계유산에 등재되었습니다. 서울 종로구에 위치하며, 정전(국보 제227호)과 영녕전(보물 제821호)으로 구성됩니다.",
    description: "종묘는 1394년 조선 태조가 한양 천도와 함께 창건한 왕실 사당으로, 조선 왕조 519년의 역사를 관통하는 성소(聖所)입니다. 정전에는 49위, 영녕전에는 34위의 신주가 봉안되어 있습니다. 매년 5월 첫째 일요일에 거행되는 종묘제례(국가무형문화재 제56호)와 종묘제례악(유네스코 인류무형문화유산)은 조선 왕실 의례의 정수를 현재까지 이어오고 있습니다. 정전은 단일 목조 건물로 세계 최장(101m)에 속하며, 엄숙한 수평선이 강조된 건축미가 독보적입니다. 2001년에는 종묘제례악이 유네스코 인류무형문화유산에 등재되었습니다.",
    images: [
      "https://images.unsplash.com/photo-1575034176396-66241b37d3d2?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1638964663550-e2123ac8900b?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=900&q=80&fit=crop",
    ],
    vrSrc: "/vr/jongmyo.html",
    festivals: [
      {
        name: "종묘제례",
        period: "5월 첫째 일요일",
        location: "서울 종로구 종묘",
        desc: "조선 역대 왕과 왕비의 신위에 올리는 국가 제례. 종묘제례악(유네스코 인류무형문화유산) 연주와 일무(佾舞)가 함께 펼쳐지며, 조선 왕실 의례를 온전히 재현합니다.",
      },
      {
        name: "종묘 야간 개장",
        period: "봄·가을 (4~5월, 10월)",
        location: "서울 종로구 종묘",
        desc: "야간 조명 아래 고요한 종묘 정전을 탐방하는 특별 프로그램. 낮과 전혀 다른 엄숙하고 신비로운 분위기를 경험할 수 있습니다.",
      },
      {
        name: "궁중문화축전",
        period: "4월 말 ~ 5월 초",
        location: "서울 4대 궁궐 및 종묘",
        desc: "경복궁·창덕궁·덕수궁·경희궁·종묘를 무대로 펼쳐지는 궁중 문화 축제. 수문장 교대식, 왕실 복식 체험, 전통 공연이 연계 운영됩니다.",
      },
    ],
  },
  {
    tag: "추천",
    title: "문묘 및 성균관",
    region: "서울 종로",
    province: "서울특별시",
    coordinates: [37.5889, 126.9979],
    guide: "AI 관광 가이드",
    progress: 82,
    category: "사적",
    year: 2026,
    theme: "유교문화·교육",
    era: "조선시대",
    method: "고증, 원형보존",
    provider: "성균관",
    overview: "문묘는 공자를 비롯한 유교 성현들의 위패를 봉안한 사당이며, 성균관은 조선시대 최고 국립 교육기관입니다. 사적 제143호로 지정되어 있으며 현재 성균관대학교 내에 보존되어 있습니다.",
    description: "성균관은 고려 충렬왕 때(1298년) 설치된 국자감을 계승해 1398년(태조 7) 조선이 한양에 건립한 최고 국립 대학입니다. 문묘는 공자·맹자 등 유교 성현 133위의 위패를 모신 사당으로, 대성전(보물 제141호)과 동·서무로 구성됩니다. 성균관 명륜당(보물 제141호)은 유생들이 강학하던 강당으로, 조선 성리학 교육의 중심지였습니다. 현재도 매년 봄·가을 석전대제를 봉행하며 유교 전통을 계승하고 있습니다. 은행나무(서울시 기념물 제5호) 두 그루가 수백 년의 역사를 묵묵히 증언하고 있습니다.",
    images: [
      "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1539635278303-d4002c07eae3?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=900&q=80&fit=crop",
    ],
    vrSrc: "/vr/munmyo.html",
    festivals: [
      {
        name: "석전대제",
        period: "봄(음력 2월) · 가을(음력 8월) 상정일(上丁日)",
        location: "서울 종로구 성균관 문묘",
        desc: "공자를 비롯한 유교 성현들에게 올리는 제향. 국가무형문화재 제85호로 지정되어 있으며, 일무(佾舞)와 문묘제례악이 수반됩니다.",
      },
      {
        name: "성균관 유교문화 축제",
        period: "5월 중순",
        location: "서울 종로구 성균관대학교",
        desc: "조선시대 과거 시험 재현, 유생 복식 체험, 전통 다례 시연 등 유교 문화를 체험하는 행사. 명륜당과 대성전 일원에서 진행됩니다.",
      },
      {
        name: "인문학 야행",
        period: "10월 중순",
        location: "서울 종로구 일원",
        desc: "종묘·성균관·창덕궁을 잇는 야간 인문학 탐방 프로그램. 전문 해설사와 함께 조선 유교 문화의 흐름을 걸으며 탐구합니다.",
      },
    ],
  },
  {
    tag: "진행 중",
    title: "청주 고인쇄박물관",
    region: "충북 청주",
    province: "충청북도",
    coordinates: [36.6369, 127.4754],
    guide: "AI 관광 가이드",
    progress: 74,
    category: "박물관",
    year: 2026,
    theme: "역사·인쇄문화",
    era: "고려시대",
    method: "전시, 체험",
    provider: "청주시",
    overview: "청주 고인쇄박물관은 세계 최초의 금속활자본인 직지심체요절(1377년)이 인쇄된 청주 흥덕사지에 건립된 박물관입니다. 고인쇄 문화의 역사와 가치를 체계적으로 보존·전시하고 있습니다.",
    description: "청주 고인쇄박물관은 1992년 흥덕사지 발굴 이후 1992년 개관한 박물관으로, '직지심체요절'의 인쇄지인 흥덕사지(사적 제315호)에 위치합니다. 직지심체요절은 1377년 청주 흥덕사에서 금속활자로 인쇄된 세계 최고(最古)의 금속활자 인쇄물로 2001년 유네스코 세계기록유산에 등재되었습니다. 박물관에서는 금속활자 제작 과정, 목판·금속활자 인쇄 시연, 직접 인쇄를 체험하는 교육 프로그램을 운영합니다. 매년 9~10월에는 '직지코리아 국제페스티벌'이 개최됩니다.",
    images: [
      "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=900&q=80&fit=crop",
      "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=900&q=80&fit=crop",
    ],
    festivals: [
      {
        name: "직지코리아 국제 페스티벌",
        period: "9월 하순 ~ 10월 초",
        location: "충북 청주시 흥덕구 일원",
        desc: "세계 최초 금속활자본 직지를 기념하는 국제 행사. 활자 인쇄 체험, 국제 학술 심포지엄, 미디어아트 전시, 북 페어가 함께 열립니다.",
      },
      {
        name: "청주 공예 비엔날레",
        period: "격년제 (홀수년 9~10월)",
        location: "충북 청주시 문화제조창",
        desc: "세계 유일의 공예 전문 국제 비엔날레. 50여 개국 작가들의 현대 공예 작품과 전통 공예 재현 전시가 함께 진행됩니다.",
      },
      {
        name: "청주 가경 어울마당",
        period: "10월 중순",
        location: "충북 청주시 가경동 일원",
        desc: "시민 참여형 지역 문화 축제. 전통 놀이, 지역 예술가 공연, 향토 음식 마당이 열리며 가족 단위 방문객에게 인기입니다.",
      },
    ],
  },
];


const spotIcon = L.divIcon({
  className: "",
  html: `<div class="spot-pin"></div>`,
  iconSize: [22, 22],
  iconAnchor: [11, 22],
  popupAnchor: [0, -24],
});

function MapController({ spot }: { spot: Spot | null }) {
  const map = useMap();
  useEffect(() => {
    if (spot) {
      map.flyTo(spot.coordinates, 14, { duration: 1.2 });
    }
  }, [spot, map]);
  return null;
}

function SpotMarker({ spot, onDetail }: { spot: Spot; onDetail: () => void }) {
  const markerRef = useRef<L.Marker>(null);

  useEffect(() => {
    markerRef.current?.openPopup();
  }, [spot]);

  return (
    <Marker ref={markerRef} position={spot.coordinates} icon={spotIcon}>
      <Popup className="spot-popup">
        <div className="spot-popup-inner">
          <span className={`spot-popup-tag spot-popup-tag--${spot.tag === "추천" ? "active" : "progress"}`}>
            {spot.tag}
          </span>
          <strong className="spot-popup-title">{spot.title}</strong>
          <span className="spot-popup-region">{spot.region}</span>
          <button className="spot-popup-btn" onClick={onDetail}>
            자세히 보기 →
          </button>
        </div>
      </Popup>
    </Marker>
  );
}

function LocateButton() {
  const map = useMap();
  const locate = () => {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        map.flyTo([latitude, longitude], 13, { duration: 1.2 });
        L.circleMarker([latitude, longitude], {
          radius: 8,
          fillColor: "#2A6EA4",
          color: "#fff",
          weight: 2,
          fillOpacity: 1,
        }).addTo(map).bindPopup("현재 위치").openPopup();
      },
      () => alert("위치 정보를 가져올 수 없습니다.")
    );
  };
  return (
    <div className="map-locate-btn-wrap">
      <button className="map-locate-btn" onClick={locate} title="내 위치">
        ⊕
      </button>
    </div>
  );
}

function KoreaMask() {
  const map = useMap();

  useEffect(() => {
    let maskLayer: L.GeoJSON | undefined;

    fetch("/korea-outline.json")
      .then((r) => r.json())
      .then((data) => {
        const feature = data.features[0];
        // shapely unary_union 결과: MultiPolygon (진짜 외곽선, 내부 경계 없음)
        // 각 폴리곤의 외곽 링을 구멍으로 사용
        const koreaPolygons: number[][][][] = feature.geometry.type === "MultiPolygon"
          ? feature.geometry.coordinates
          : [feature.geometry.coordinates];

        const maskGeoJSON = {
          type: "Feature",
          geometry: {
            type: "Polygon",
            coordinates: [
              // 세계 외곽 링
              [[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]],
              // 한국 각 섬/본토의 외곽 링을 구멍으로
              ...koreaPolygons.map((poly) => poly[0]),
            ],
          },
          properties: {},
        };

        maskLayer = L.geoJSON(maskGeoJSON as any, {
          style: {
            fillColor: "#555555",
            fillOpacity: 0.97,
            color: "transparent",
            weight: 0,
            fillRule: "evenodd",
          } as any,
        }).addTo(map);
      });

    return () => {
      if (maskLayer) map.removeLayer(maskLayer);
    };
  }, [map]);

  return null;
}

function FestivalPopup({
  festival,
  onClose,
}: {
  festival: Festival;
  onClose: () => void;
}) {
  return (
    <div className="festival-popup-overlay" onClick={onClose}>
      <div className="festival-popup" onClick={(e) => e.stopPropagation()}>
        <button className="festival-popup-close" onClick={onClose}>✕</button>
        <div className="festival-popup-period">{festival.period}</div>
        <h3 className="festival-popup-name">{festival.name}</h3>
        <p className="festival-popup-location">📍 {festival.location}</p>
        <p className="festival-popup-desc">{festival.desc}</p>
      </div>
    </div>
  );
}

function TouristDetail({
  spot,
  onClose,
}: {
  spot: Spot;
  onClose: () => void;
}) {
  const [imgIdx, setImgIdx] = useState(0);
  const [imgError, setImgError] = useState<Record<number, boolean>>({});
  const [activeFestival, setActiveFestival] = useState<Festival | null>(null);

  const totalSlides = spot.images.length + (spot.vrSrc ? 1 : 0);
  const isVrSlide = spot.vrSrc != null && imgIdx === spot.images.length;

  const prev = () => setImgIdx((i) => (i - 1 + totalSlides) % totalSlides);
  const next = () => setImgIdx((i) => (i + 1) % totalSlides);

  return (
    <div className="detail-overlay" onClick={onClose}>
      <div className="detail-modal" onClick={(e) => e.stopPropagation()}>
        <button className="detail-close" onClick={onClose}>✕</button>

        {/* Left: image / VR carousel */}
        <div className="detail-image-col">
          <div className="detail-image-wrap">
            {isVrSlide ? (
              <iframe
                src={spot.vrSrc}
                className="detail-vr-frame"
                title="VR 탐방"
                allowFullScreen
              />
            ) : imgError[imgIdx] ? (
              <div className="detail-image-fallback">
                <span>{spot.title}</span>
              </div>
            ) : (
              <img
                src={spot.images[imgIdx]}
                alt={spot.title}
                onError={() => setImgError((e) => ({ ...e, [imgIdx]: true }))}
              />
            )}
          </div>
          <div className="detail-image-nav">
            <button onClick={prev} disabled={totalSlides <= 1}>‹</button>
            <span>
              {isVrSlide ? "VR" : imgIdx + 1} / {totalSlides}
              {isVrSlide && <span className="detail-vr-badge">3D 탐방</span>}
            </span>
            <button onClick={next} disabled={totalSlides <= 1}>›</button>
          </div>
        </div>

        {/* Right: info */}
        <div className="detail-info-col">
          <div className="detail-info-top">
            <span className={`detail-badge detail-badge--${spot.tag === "추천" ? "active" : "progress"}`}>
              {spot.category}
            </span>
            <span className="detail-year">제작년도 {spot.year}</span>
          </div>

          <h2 className="detail-title">{spot.title}</h2>

          <table className="detail-table">
            <tbody>
              <tr>
                <th>테마</th>
                <td>{spot.theme}</td>
                <th>시대</th>
                <td>{spot.era}</td>
              </tr>
              <tr>
                <th>제작방식</th>
                <td>{spot.method}</td>
                <th>제공기관</th>
                <td>{spot.provider}</td>
              </tr>
              <tr>
                <th>제작개요</th>
                <td colSpan={3}>{spot.overview}</td>
              </tr>
            </tbody>
          </table>

          <p className="detail-desc">{spot.description}</p>

          {/* Nearby events section */}
          <div className="detail-festival">
            <div className="detail-festival-header">
              <span className="detail-festival-icon">🗓️</span>
              <span className="detail-festival-title">주변 행사</span>
            </div>
            <div className="detail-festival-grid">
              {spot.festivals.map((f) => (
                <div
                  className="festival-card"
                  key={f.name}
                  onClick={() => setActiveFestival(f)}
                >
                  <div className="festival-card-top">
                    <span className="festival-name">{f.name}</span>
                    <span className="festival-period">{f.period}</span>
                  </div>
                  <span className="festival-location">📍 {f.location}</span>
                  <p className="festival-desc">{f.desc}</p>
                  <span className="festival-more">자세히 보기 →</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {activeFestival && (
        <FestivalPopup
          festival={activeFestival}
          onClose={() => setActiveFestival(null)}
        />
      )}
    </div>
  );
}

export default function MapPage({ onNavigate }: Props) {
  const [focusedSpot, setFocusedSpot] = useState<Spot | null>(null);
  const [selectedSpot, setSelectedSpot] = useState<Spot | null>(null);
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null);
  const [regionOpen, setRegionOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  const filteredSpots = selectedRegion
    ? SPOTS.filter((s) => s.province === selectedRegion)
    : SPOTS;

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
          <button className="map-hamburger" onClick={() => setMenuOpen(v => !v)} aria-label="메뉴">
            <span /><span /><span />
          </button>
        </div>
        {menuOpen && (
          <div className="map-mobile-menu">
            <a onClick={() => { onNavigate("tourinfo"); setMenuOpen(false); }}>관광정보</a>
            <a onClick={() => { onNavigate("map"); setMenuOpen(false); }}>관광동선</a>
            <a onClick={() => { onNavigate("store"); setMenuOpen(false); }}>스토어</a>
            <a onClick={() => { onNavigate("ticket"); setMenuOpen(false); }}>티켓</a>
            <a onClick={() => setMenuOpen(false)}>설정</a>
          </div>
        )}
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

        {/* Center: map with overlaid AI chat */}
        <div className="map-center">
          <div className="map-search-row">
            <span className="map-search-label">관광지 검색</span>
            <input className="map-search-input" placeholder="검색..." />
            <button className="map-filter-btn">필터</button>
          </div>
          <div className="map-container">
            <MapContainer
              center={[35.0, 127.8]}
              zoom={7}
              minZoom={7}
              maxZoom={13}
              maxBounds={[[32.0, 123.5], [39.8, 132.8]]}
              maxBoundsViscosity={1.0}
              style={{ width: "100%", height: "100%" }}
              zoomControl={true}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              />
              <KoreaMask />
              <LocateButton />
              <MapController spot={focusedSpot} />
              {focusedSpot && (
                <SpotMarker
                  spot={focusedSpot}
                  onDetail={() => setSelectedSpot(focusedSpot)}
                />
              )}
            </MapContainer>
          </div>
        </div>

        {/* Right: spot cards */}
        <div className="map-sidebar">
          {/* Region selector */}
          <div className="region-selector">
            <button
              className="region-selector-btn"
              onClick={() => setRegionOpen((o) => !o)}
            >
              <span>{selectedRegion ?? "지역 선택"}</span>
              <span className="region-selector-arrow">{regionOpen ? "▲" : "▼"}</span>
            </button>
            {regionOpen && (
              <>
                <div className="region-overlay" onClick={() => setRegionOpen(false)} />
                <div className="region-dropdown">
                  <button
                    className={`region-btn-all ${selectedRegion === null ? "active" : ""}`}
                    onClick={() => { setSelectedRegion(null); setRegionOpen(false); }}
                  >
                    전체
                  </button>
                  <div className="region-group-btns">
                    {REGIONS.map((r) => (
                      <button
                        key={r}
                        className={`region-btn ${selectedRegion === r ? "active" : ""}`}
                        onClick={() => { setSelectedRegion(r); setRegionOpen(false); }}
                      >
                        {r}
                      </button>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>

          {filteredSpots.length === 0 && (
            <div className="region-empty">추후 추가 예정입니다.</div>
          )}

          {filteredSpots.map((s) => (
            <div
              className={`spot-card${focusedSpot?.title === s.title ? " spot-card--focused" : ""}`}
              key={s.title}
              onClick={() => setFocusedSpot(s)}
            >
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

      {/* Detail modal */}
      {selectedSpot && (
        <TouristDetail spot={selectedSpot} onClose={() => setSelectedSpot(null)} />
      )}
    </div>
  );
}
