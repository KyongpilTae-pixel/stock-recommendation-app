import reflex as rx
from typing import List


class TechSignal(rx.Base):
    name: str = ""
    value: str = ""
    signal: str = ""  # "bullish", "bearish", "neutral"


class BreakoutResult(rx.Base):
    ticker: str = ""
    name: str = ""
    formatted_price: str = ""
    formatted_prev_high: str = ""
    formatted_breakout_pct: str = ""
    formatted_change_pct: str = ""
    change_positive: bool = True
    breakout_date: str = ""  # 전고점 최초 돌파일


class VWAPResult(rx.Base):
    ticker: str = ""
    name: str = ""
    formatted_price: str = ""
    formatted_vwap: str = ""
    formatted_vwap_pct: str = ""   # VWAP 대비 %
    formatted_change_pct: str = ""
    change_positive: bool = True
    crossover_date: str = ""       # VWAP 상단 돌파일


KOSPI200_LIST = [
    # IT / 반도체
    "005930.KS",  # 삼성전자
    "000660.KS",  # SK하이닉스
    "009150.KS",  # 삼성전기
    "066570.KS",  # LG전자
    "011070.KS",  # LG이노텍
    "034220.KS",  # LG디스플레이
    "018260.KS",  # 삼성SDS
    "042700.KS",  # 한미반도체
    "000990.KS",  # DB하이텍
    "240810.KS",  # 원익IPS
    "036570.KS",  # 엔씨소프트
    "259960.KS",  # 크래프톤
    "263750.KS",  # 펄어비스
    "058470.KS",  # 리노공업
    # 인터넷 / 플랫폼 / 엔터
    "035420.KS",  # NAVER
    "035720.KS",  # 카카오
    "352820.KS",  # 하이브
    "041510.KS",  # SM엔터테인먼트
    "035900.KS",  # JYP엔터테인먼트
    "122870.KS",  # 와이지엔터테인먼트
    "030000.KS",  # 제일기획
    # 바이오 / 헬스케어
    "207940.KS",  # 삼성바이오로직스
    "068270.KS",  # 셀트리온
    "000100.KS",  # 유한양행
    "128940.KS",  # 한미약품
    "326030.KS",  # SK바이오팜
    "302440.KS",  # SK바이오사이언스
    "006280.KS",  # 녹십자
    "145020.KS",  # 휴젤
    "091990.KS",  # 셀트리온헬스케어
    "196170.KS",  # 알테오젠
    "141080.KS",  # 레고켐바이오
    "185750.KS",  # 종근당
    "170900.KS",  # 동아쏘시오홀딩스
    "097890.KS",  # 한미사이언스
    # 자동차
    "005380.KS",  # 현대차
    "000270.KS",  # 기아
    "012330.KS",  # 현대모비스
    "086280.KS",  # 현대글로비스
    "004020.KS",  # 현대제철
    "241560.KS",  # 두산밥캣
    "018880.KS",  # 한온시스템
    "161390.KS",  # 한국타이어앤테크놀로지
    "064350.KS",  # 현대로템
    # 에너지 / 2차전지
    "051910.KS",  # LG화학
    "006400.KS",  # 삼성SDI
    "373220.KS",  # LG에너지솔루션
    "247540.KS",  # 에코프로비엠
    "086520.KS",  # 에코프로
    "010950.KS",  # S-Oil
    "096770.KS",  # SK이노베이션
    "011170.KS",  # 롯데케미칼
    "003670.KS",  # 포스코퓨처엠
    "009830.KS",  # 한화솔루션
    "285130.KS",  # SK케미칼
    "011790.KS",  # SKC
    "014680.KS",  # 한솔케미칼
    "011780.KS",  # 금호석유
    # 철강 / 소재
    "005490.KS",  # POSCO홀딩스
    "010130.KS",  # 고려아연
    "103140.KS",  # 풍산
    "004490.KS",  # 세방전지
    "298050.KS",  # 효성중공업
    "120110.KS",  # 코오롱인더
    # 금융
    "105560.KS",  # KB금융
    "055550.KS",  # 신한지주
    "086790.KS",  # 하나금융지주
    "316140.KS",  # 우리금융지주
    "032830.KS",  # 삼성생명
    "000810.KS",  # 삼성화재
    "088350.KS",  # 한화생명
    "071050.KS",  # 한국금융지주
    "175330.KS",  # JB금융지주
    "024110.KS",  # 기업은행
    "005940.KS",  # NH투자증권
    "008560.KS",  # 메리츠증권
    "006800.KS",  # 미래에셋증권
    "039490.KS",  # 키움증권
    "001450.KS",  # 현대해상
    "000060.KS",  # 메리츠화재
    # 통신
    "017670.KS",  # SK텔레콤
    "030200.KS",  # KT
    "032640.KS",  # LG유플러스
    # 조선 / 중공업 / 방산
    "329180.KS",  # HD현대중공업
    "267250.KS",  # HD현대
    "009540.KS",  # HD한국조선해양
    "010140.KS",  # 삼성중공업
    "042660.KS",  # 한화오션
    "047810.KS",  # 한국항공우주
    "012450.KS",  # 한화에어로스페이스
    "272210.KS",  # 한화시스템
    "079550.KS",  # LIG넥스원
    "010620.KS",  # 현대미포조선
    # 건설 / 인프라
    "000720.KS",  # 현대건설
    "047040.KS",  # 대우건설
    "006360.KS",  # GS건설
    "294870.KS",  # HDC현대산업개발
    "012630.KS",  # HDC
    # 지주 / 복합
    "034730.KS",  # SK
    "000880.KS",  # 한화
    "003550.KS",  # LG
    "028260.KS",  # 삼성물산
    "078930.KS",  # GS
    "001040.KS",  # CJ
    "002380.KS",  # KCC
    "010060.KS",  # OCI홀딩스
    # 유통 / 소비재
    "004170.KS",  # 신세계
    "023530.KS",  # 롯데쇼핑
    "139480.KS",  # 이마트
    "007070.KS",  # GS리테일
    "282330.KS",  # BGF리테일
    "069960.KS",  # 현대백화점
    "057050.KS",  # 현대홈쇼핑
    "033780.KS",  # KT&G
    "021240.KS",  # 코웨이
    "090430.KS",  # 아모레퍼시픽
    "002790.KS",  # 아모레G
    "008770.KS",  # 호텔신라
    "007310.KS",  # 오뚜기
    "003230.KS",  # 삼양식품
    "271560.KS",  # 오리온
    "145990.KS",  # 삼양사
    "000080.KS",  # 하이트진로
    # 식품 / 필수소비재
    "097950.KS",  # CJ제일제당
    "024720.KS",  # 코스맥스
    # 운송 / 물류
    "003490.KS",  # 대한항공
    "011200.KS",  # HMM
    "000120.KS",  # CJ대한통운
    # 에너지 / 전력
    "015760.KS",  # 한국전력
    "036460.KS",  # 한국가스공사
    "051600.KS",  # 한전KPS
    # 기타 제조
    "058430.KS",  # 포스코인터내셔널
    "012750.KS",  # 에스원
    "267270.KS",  # HD현대건설기계
    "100840.KS",  # SNT에너지
]

DEFAULT_SCAN_LIST = [
    # 미국 대형주
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA",
    "META", "JPM", "V", "MA", "UNH", "COST",
    "AVGO", "NFLX", "ADBE", "AMD",
] + KOSPI200_LIST


class State(rx.State):
    # ── 종목 분석 ──────────────────────────────────────────────────────────────
    ticker_input: str = ""

    company_name: str = ""
    current_ticker: str = ""
    price: float = 0.0
    change: float = 0.0
    change_pct: float = 0.0
    volume: str = ""
    market_cap: str = ""
    pe_ratio: str = ""
    week_52_high: float = 0.0
    week_52_low: float = 0.0
    currency: str = "USD"

    chart_data: list = []
    tech_signals: List[TechSignal] = []
    recommendation: str = ""
    recommendation_reason: str = ""

    loading: bool = False
    error: str = ""
    has_data: bool = False

    # ── 전고점 돌파 스캐너 ─────────────────────────────────────────────────────
    scan_stocks: list = DEFAULT_SCAN_LIST
    scan_input: str = ""
    scan_results: List[BreakoutResult] = []
    scanning: bool = False
    scan_progress: int = 0
    scan_total: int = 0
    scan_done: bool = False
    scan_period_months: int = 6   # 전고점 분석 기간 (1~12개월)
    scan_recent_days: int = 15    # 최근 N 거래일 내 돌파 인정

    # ── VWAP 스캐너 ────────────────────────────────────────────────────────────
    vwap_scan_results: List[VWAPResult] = []
    vwap_scanning: bool = False
    vwap_scan_progress: int = 0
    vwap_scan_total: int = 0
    vwap_scan_done: bool = False
    vwap_period_months: int = 3   # VWAP 계산 기간 (기본 3개월)
    vwap_crossover_days: int = 7  # 돌파 시점 제한 (캘린더일, 기본 1주일)

    # ── 탭 상태 ─────────────────────────────────────────────────────────────────
    active_tab: str = "analysis"

    # ── Computed vars (분석) ──────────────────────────────────────────────────

    @rx.var
    def price_color(self) -> str:
        return "green" if self.change >= 0 else "red"

    @rx.var
    def recommendation_color(self) -> str:
        return {
            "강력 매수": "green",
            "매수": "teal",
            "중립": "amber",
            "매도": "orange",
            "강력 매도": "red",
        }.get(self.recommendation, "gray")

    @rx.var
    def formatted_price(self) -> str:
        if self.currency == "KRW":
            return f"₩{self.price:,.0f}"
        return f"${self.price:,.2f}"

    @rx.var
    def formatted_change(self) -> str:
        prefix = "+" if self.change >= 0 else ""
        if self.currency == "KRW":
            return f"{prefix}{self.change:,.0f}  ({prefix}{self.change_pct:.2f}%)"
        return f"{prefix}{self.change:.2f}  ({prefix}{self.change_pct:.2f}%)"

    @rx.var
    def formatted_52w_high(self) -> str:
        if self.currency == "KRW":
            return f"₩{self.week_52_high:,.0f}"
        return f"${self.week_52_high:.2f}"

    @rx.var
    def formatted_52w_low(self) -> str:
        if self.currency == "KRW":
            return f"₩{self.week_52_low:,.0f}"
        return f"${self.week_52_low:.2f}"

    # ── Computed vars (스캐너) ────────────────────────────────────────────────

    @rx.var
    def scan_progress_pct(self) -> int:
        if self.scan_total == 0:
            return 0
        return int(self.scan_progress / self.scan_total * 100)

    @rx.var
    def scan_status_text(self) -> str:
        if self.scan_progress == 0:
            return "Yahoo Finance 데이터 다운로드 중..."
        return f"종목 분석 중... ({self.scan_progress} / {self.scan_total})"

    @rx.var
    def scan_period_label(self) -> str:
        return f"{self.scan_period_months}개월"

    @rx.var
    def vwap_progress_pct(self) -> int:
        if self.vwap_scan_total == 0:
            return 0
        return int(self.vwap_scan_progress / self.vwap_scan_total * 100)

    @rx.var
    def vwap_status_text(self) -> str:
        if self.vwap_scan_progress == 0:
            return "Yahoo Finance 데이터 다운로드 중..."
        return f"VWAP 분석 중... ({self.vwap_scan_progress} / {self.vwap_scan_total})"

    @rx.var
    def vwap_period_label(self) -> str:
        return f"{self.vwap_period_months}개월"

    @rx.var
    def chart_vwap_label(self) -> str:
        return "VWAP (6개월 누적)"

    @rx.var
    def vwap_crossover_label(self) -> str:
        d = self.vwap_crossover_days
        if d == 7:
            return "1주일"
        if d == 14:
            return "2주일"
        if d % 7 == 0:
            return f"{d // 7}주일"
        return f"{d}일"

    @rx.var
    def has_vwap_results(self) -> bool:
        return len(self.vwap_scan_results) > 0

    @rx.var
    def vwap_result_count(self) -> int:
        return len(self.vwap_scan_results)

    @rx.var
    def scan_result_count(self) -> int:
        return len(self.scan_results)

    @rx.var
    def scan_stock_count(self) -> int:
        return len(self.scan_stocks)

    @rx.var
    def has_scan_results(self) -> bool:
        return len(self.scan_results) > 0

    # ── Event handlers (분석) ─────────────────────────────────────────────────

    def set_ticker(self, value: str):
        self.ticker_input = value.upper()

    def handle_key_press(self, key: str):
        if key == "Enter":
            return State.search_stock

    def quick_search(self, ticker: str):
        self.ticker_input = ticker.upper()
        return State.search_stock

    def open_stock_from_scanner(self, ticker: str):
        """스캐너 결과 클릭 시 종목 분석 탭으로 이동"""
        self.active_tab = "analysis"
        self.ticker_input = ticker.upper()
        return State.search_stock

    async def search_stock(self):
        """종목 검색 및 기술적 분석 수행"""
        if not self.ticker_input.strip():
            self.error = "종목 코드를 입력해주세요"
            return

        self.loading = True
        self.error = ""
        self.has_data = False
        yield

        try:
            import yfinance as yf

            ticker = yf.Ticker(self.ticker_input.strip())
            info = ticker.info

            price = (
                info.get("regularMarketPrice")
                or info.get("currentPrice")
                or info.get("ask")
                or 0
            )

            if not price:
                self.error = f"'{self.ticker_input}' 종목을 찾을 수 없습니다. 종목 코드를 확인해주세요."
                self.loading = False
                return

            prev_close = (
                info.get("regularMarketPreviousClose")
                or info.get("previousClose")
                or price
            )
            change = price - prev_close
            change_pct = (change / prev_close * 100) if prev_close else 0

            mc = info.get("marketCap") or 0
            if mc >= 1e12:
                mc_str = f"{mc / 1e12:.2f}T"
            elif mc >= 1e9:
                mc_str = f"{mc / 1e9:.2f}B"
            elif mc >= 1e6:
                mc_str = f"{mc / 1e6:.2f}M"
            elif mc > 0:
                mc_str = f"{mc:,.0f}"
            else:
                mc_str = "N/A"

            vol = info.get("regularMarketVolume") or info.get("volume") or 0
            if vol >= 1e9:
                vol_str = f"{vol / 1e9:.2f}B"
            elif vol >= 1e6:
                vol_str = f"{vol / 1e6:.2f}M"
            elif vol >= 1e3:
                vol_str = f"{vol / 1e3:.1f}K"
            elif vol > 0:
                vol_str = str(vol)
            else:
                vol_str = "N/A"

            pe = info.get("trailingPE")
            pe_str = f"{pe:.2f}" if pe else "N/A"

            self.company_name = (
                info.get("longName") or info.get("shortName") or self.ticker_input
            )
            self.current_ticker = self.ticker_input
            self.price = float(price)
            self.change = float(change)
            self.change_pct = float(change_pct)
            self.volume = vol_str
            self.market_cap = mc_str
            self.pe_ratio = pe_str
            self.week_52_high = float(info.get("fiftyTwoWeekHigh") or 0)
            self.week_52_low = float(info.get("fiftyTwoWeekLow") or 0)
            self.currency = info.get("currency") or "USD"

            hist = ticker.history(period="6mo")
            if hist.empty:
                self.error = "과거 데이터를 가져올 수 없습니다."
                self.loading = False
                return

            closes = hist["Close"]
            highs = hist["High"]
            lows = hist["Low"]
            volumes = hist["Volume"]

            ma20_series = closes.rolling(20).mean()
            ma50_series = closes.rolling(50).mean()
            typical = (highs + lows + closes) / 3
            cum_tp_vol = (typical * volumes).cumsum()
            cum_vol = volumes.cumsum()
            vwap_series = cum_tp_vol / cum_vol

            def _fmt(v):
                return round(float(v), 2) if not (v != v) else None  # NaN → None

            self.chart_data = [
                {
                    "date": idx.strftime("%m/%d"),
                    "close": round(float(row["Close"]), 2),
                    "ma20": _fmt(ma20_series.loc[idx]),
                    "ma50": _fmt(ma50_series.loc[idx]),
                    "vwap": _fmt(vwap_series.loc[idx]),
                }
                for idx, row in hist.iterrows()
            ]

            ma20 = float(ma20_series.iloc[-1])
            ma50 = float(ma50_series.iloc[-1])
            current = float(closes.iloc[-1])

            delta = closes.diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            loss_val = float(loss.iloc[-1])
            gain_val = float(gain.iloc[-1])
            rs = gain_val / loss_val if loss_val != 0 else 0
            rsi = float(100 - (100 / (1 + rs))) if rs else 50.0

            ema12 = closes.ewm(span=12, adjust=False).mean()
            ema26 = closes.ewm(span=26, adjust=False).mean()
            macd_line = ema12 - ema26
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            macd_val = float(macd_line.iloc[-1])
            sig_val = float(signal_line.iloc[-1])

            signals: list = []
            score = 0

            if current > ma20:
                signals.append(TechSignal(name="MA20 (20일 이평)", value=f"{ma20:.2f}", signal="bullish"))
                score += 1
            else:
                signals.append(TechSignal(name="MA20 (20일 이평)", value=f"{ma20:.2f}", signal="bearish"))
                score -= 1

            if current > ma50:
                signals.append(TechSignal(name="MA50 (50일 이평)", value=f"{ma50:.2f}", signal="bullish"))
                score += 1
            else:
                signals.append(TechSignal(name="MA50 (50일 이평)", value=f"{ma50:.2f}", signal="bearish"))
                score -= 1

            if ma20 > ma50:
                signals.append(TechSignal(name="이평 교차 신호", value="골든 크로스", signal="bullish"))
                score += 1
            else:
                signals.append(TechSignal(name="이평 교차 신호", value="데드 크로스", signal="bearish"))
                score -= 1

            rsi_r = round(rsi, 1)
            if rsi < 30:
                signals.append(TechSignal(name="RSI (14일)", value=str(rsi_r), signal="bullish"))
                score += 2
            elif rsi > 70:
                signals.append(TechSignal(name="RSI (14일)", value=str(rsi_r), signal="bearish"))
                score -= 2
            else:
                signals.append(TechSignal(name="RSI (14일)", value=str(rsi_r), signal="neutral"))

            if macd_val > sig_val:
                signals.append(TechSignal(name="MACD", value=f"{macd_val:.4f}", signal="bullish"))
                score += 1
            else:
                signals.append(TechSignal(name="MACD", value=f"{macd_val:.4f}", signal="bearish"))
                score -= 1

            self.tech_signals = signals

            if score >= 3:
                self.recommendation = "강력 매수"
                self.recommendation_reason = (
                    "대부분의 기술적 지표가 강한 상승 신호를 나타내고 있습니다. "
                    "적극적인 매수를 고려해볼 수 있습니다."
                )
            elif score >= 1:
                self.recommendation = "매수"
                self.recommendation_reason = (
                    "기술적 지표가 전반적으로 긍정적입니다. "
                    "분할 매수 전략을 고려해볼 수 있습니다."
                )
            elif score == 0:
                self.recommendation = "중립"
                self.recommendation_reason = (
                    "상승과 하락 신호가 혼재되어 있습니다. "
                    "추이를 지켜보며 추가 모니터링이 필요합니다."
                )
            elif score >= -2:
                self.recommendation = "매도"
                self.recommendation_reason = (
                    "기술적 지표가 부정적인 신호를 보이고 있습니다. "
                    "리스크 관리와 손절 전략을 고려해보세요."
                )
            else:
                self.recommendation = "강력 매도"
                self.recommendation_reason = (
                    "대부분의 기술적 지표가 강한 하락 신호를 나타내고 있습니다. "
                    "손절 또는 비중 축소를 강력히 고려해보세요."
                )

            self.has_data = True

        except Exception as e:
            self.error = f"오류가 발생했습니다: {str(e)}"
        finally:
            self.loading = False

    # ── Event handlers (스캐너) ───────────────────────────────────────────────

    def set_scan_input(self, value: str):
        self.scan_input = value.upper()

    def handle_scan_key(self, key: str):
        if key == "Enter":
            return State.add_scan_stock

    def add_scan_stock(self):
        ticker = self.scan_input.strip()
        if ticker and ticker not in self.scan_stocks:
            self.scan_stocks = list(self.scan_stocks) + [ticker]
        self.scan_input = ""

    def remove_scan_stock(self, ticker: str):
        self.scan_stocks = [s for s in self.scan_stocks if s != ticker]

    def reset_scan(self):
        self.scan_stocks = list(DEFAULT_SCAN_LIST)
        self.scan_results = []
        self.scan_done = False

    def set_scan_period(self, value: list):
        """전고점 분석 기간 슬라이더"""
        if value:
            self.scan_period_months = int(value[0])

    async def run_breakout_scan(self):
        """전고점 돌파 종목 스캔 (배치 다운로드 - Yahoo Finance 1회 요청)"""
        if self.scanning:
            return

        self.scanning = True
        self.scan_results = []
        self.scan_done = False
        self.scan_progress = 0
        self.scan_total = len(self.scan_stocks)
        yield

        import yfinance as yf

        tickers = list(self.scan_stocks)
        period_str = "1y" if self.scan_period_months >= 12 else f"{self.scan_period_months}mo"

        # ── 1회 배치 다운로드 (Yahoo Finance 단일 요청) ──────────────────────
        try:
            raw = yf.download(
                tickers,
                period=period_str,
                auto_adjust=True,
                progress=False,
            )
        except Exception:
            self.scanning = False
            self.scan_done = True
            return

        is_multi = len(tickers) > 1
        results = []

        for i, ticker in enumerate(tickers):
            self.scan_progress = i + 1
            yield

            try:
                if is_multi:
                    if ticker not in raw["Close"].columns:
                        continue
                    close_s = raw["Close"][ticker].dropna()
                    high_s = raw["High"][ticker].dropna()
                else:
                    close_s = raw["Close"].dropna()
                    high_s = raw["High"].dropna()

                if len(close_s) < 10:
                    continue

                lookback = max(len(close_s) - self.scan_recent_days, 5)
                prev_high = float(high_s.iloc[:lookback].max())
                current = float(close_s.iloc[-1])

                if current > prev_high:
                    # 최초 돌파일 탐색
                    recent_closes = close_s.iloc[lookback:]
                    crossed = recent_closes[recent_closes > prev_high]
                    breakout_date = crossed.index[0].strftime("%Y.%m.%d") if not crossed.empty else "-"

                    prev_close = float(close_s.iloc[-2]) if len(close_s) > 1 else current
                    change_pct = (current - prev_close) / prev_close * 100
                    breakout_pct = (current - prev_high) / prev_high * 100

                    # .KS/.KQ면 KRW, 나머지 USD (info 호출 최소화)
                    is_kr = ticker.endswith(".KS") or ticker.endswith(".KQ")
                    currency = "KRW" if is_kr else "USD"

                    # 돌파 종목만 info 요청 (2번째 데이터 소스: Yahoo Finance info)
                    try:
                        info = yf.Ticker(ticker).info
                        name = info.get("longName") or info.get("shortName") or ticker
                        currency = info.get("currency") or currency
                    except Exception:
                        name = ticker

                    if currency == "KRW":
                        fmt_price = f"₩{current:,.0f}"
                        fmt_high = f"₩{prev_high:,.0f}"
                    else:
                        fmt_price = f"${current:.2f}"
                        fmt_high = f"${prev_high:.2f}"

                    bp_sign = "+" if breakout_pct >= 0 else ""
                    cp_sign = "+" if change_pct >= 0 else ""

                    results.append(BreakoutResult(
                        ticker=ticker,
                        name=name,
                        formatted_price=fmt_price,
                        formatted_prev_high=fmt_high,
                        formatted_breakout_pct=f"{bp_sign}{breakout_pct:.2f}%",
                        formatted_change_pct=f"{cp_sign}{change_pct:.2f}%",
                        change_positive=change_pct >= 0,
                        breakout_date=breakout_date,
                    ))

            except Exception:
                pass

        # 돌파율 내림차순 정렬
        self.scan_results = sorted(results, key=lambda r: r.formatted_breakout_pct, reverse=True)
        self.scanning = False
        self.scan_done = True

    # ── VWAP 스캐너 ───────────────────────────────────────────────────────────

    def set_vwap_period(self, value: list):
        if value:
            self.vwap_period_months = int(value[0])

    def set_vwap_crossover_days(self, value: list):
        if value:
            self.vwap_crossover_days = int(value[0])

    async def run_vwap_scan(self):
        """VWAP 상단 돌파 종목 스캔 (배치 다운로드 - Yahoo Finance 1회 요청)"""
        if self.vwap_scanning:
            return

        self.vwap_scanning = True
        self.vwap_scan_results = []
        self.vwap_scan_done = False
        self.vwap_scan_progress = 0
        self.vwap_scan_total = len(self.scan_stocks)
        yield

        import yfinance as yf

        tickers = list(self.scan_stocks)
        period_str = "1y" if self.vwap_period_months >= 12 else f"{self.vwap_period_months}mo"

        # ── 1회 배치 다운로드 ─────────────────────────────────────────────────
        try:
            raw = yf.download(
                tickers,
                period=period_str,
                auto_adjust=True,
                progress=False,
            )
        except Exception:
            self.vwap_scanning = False
            self.vwap_scan_done = True
            return

        is_multi = len(tickers) > 1
        results = []

        for i, ticker in enumerate(tickers):
            self.vwap_scan_progress = i + 1
            yield

            try:
                if is_multi:
                    if ticker not in raw["Close"].columns:
                        continue
                    close_s = raw["Close"][ticker].dropna()
                    high_s  = raw["High"][ticker].dropna()
                    low_s   = raw["Low"][ticker].dropna()
                    vol_s   = raw["Volume"][ticker].dropna()
                else:
                    close_s = raw["Close"].dropna()
                    high_s  = raw["High"].dropna()
                    low_s   = raw["Low"].dropna()
                    vol_s   = raw["Volume"].dropna()

                if len(close_s) < 10 or vol_s.sum() == 0:
                    continue

                # ── VWAP 계산: Σ(TP × Volume) / Σ(Volume) ──────────────────
                typical = (high_s + low_s + close_s) / 3
                vwap = float((typical * vol_s).sum() / vol_s.sum())
                current = float(close_s.iloc[-1])

                # 현재가가 VWAP 아래면 스킵
                if current <= vwap:
                    continue

                # ── VWAP 상단 교차일 탐색 (아래→위 교차) ────────────────────
                above = close_s > vwap
                prev_above = above.shift(1).fillna(False)
                crossover = above & (~prev_above)
                crossed_dates = crossover[crossover]

                if crossed_dates.empty:
                    # 기간 내 내내 위에 있었으면 스킵 (최근 돌파 아님)
                    continue

                last_cross_idx = crossed_dates.index[-1]
                crossover_date = last_cross_idx.strftime("%Y.%m.%d")

                # 설정된 캘린더일 이내 돌파만 포함
                days_since = (close_s.index[-1] - last_cross_idx).days
                if days_since > self.vwap_crossover_days:
                    continue

                vwap_pct = (current - vwap) / vwap * 100
                prev_close = float(close_s.iloc[-2]) if len(close_s) > 1 else current
                change_pct = (current - prev_close) / prev_close * 100

                is_kr = ticker.endswith(".KS") or ticker.endswith(".KQ")
                currency = "KRW" if is_kr else "USD"

                # 돌파 종목만 info 요청
                try:
                    info = yf.Ticker(ticker).info
                    name = info.get("longName") or info.get("shortName") or ticker
                    currency = info.get("currency") or currency
                except Exception:
                    name = ticker

                if currency == "KRW":
                    fmt_price = f"₩{current:,.0f}"
                    fmt_vwap  = f"₩{vwap:,.0f}"
                else:
                    fmt_price = f"${current:.2f}"
                    fmt_vwap  = f"${vwap:.2f}"

                vp_sign = "+" if vwap_pct >= 0 else ""
                cp_sign = "+" if change_pct >= 0 else ""

                results.append(VWAPResult(
                    ticker=ticker,
                    name=name,
                    formatted_price=fmt_price,
                    formatted_vwap=fmt_vwap,
                    formatted_vwap_pct=f"{vp_sign}{vwap_pct:.2f}%",
                    formatted_change_pct=f"{cp_sign}{change_pct:.2f}%",
                    change_positive=change_pct >= 0,
                    crossover_date=crossover_date,
                ))

            except Exception:
                pass

        # VWAP 대비 % 내림차순 정렬
        self.vwap_scan_results = sorted(results, key=lambda r: r.formatted_vwap_pct, reverse=True)
        self.vwap_scanning = False
        self.vwap_scan_done = True
