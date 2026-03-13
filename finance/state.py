import reflex as rx
from typing import List


class TechSignal(rx.Base):
    name: str = ""
    value: str = ""
    signal: str = ""  # "bullish", "bearish", "neutral"


class State(rx.State):
    # 검색 입력
    ticker_input: str = ""

    # 종목 정보 (flat 구조)
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

    # 차트 & 기술적 분석
    chart_data: list = []
    tech_signals: List[TechSignal] = []
    recommendation: str = ""
    recommendation_reason: str = ""

    # UI 상태
    loading: bool = False
    error: str = ""
    has_data: bool = False

    # ── Computed vars ─────────────────────────────────────────────────────────

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

    # ── Event handlers ────────────────────────────────────────────────────────

    def set_ticker(self, value: str):
        self.ticker_input = value.upper()

    def handle_key_press(self, key: str):
        if key == "Enter":
            return State.search_stock

    async def search_stock(self, quick_ticker: str = ""):
        """종목 검색 및 기술적 분석 수행"""
        if quick_ticker:
            self.ticker_input = quick_ticker.upper()

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

            # 시가총액 포맷
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

            # 거래량 포맷
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

            # 과거 데이터 (6개월)
            hist = ticker.history(period="6mo")
            if hist.empty:
                self.error = "과거 데이터를 가져올 수 없습니다."
                self.loading = False
                return

            self.chart_data = [
                {
                    "date": idx.strftime("%m/%d"),
                    "close": round(float(row["Close"]), 2),
                }
                for idx, row in hist.iterrows()
            ]

            # ── 기술적 지표 계산 ───────────────────────────────────────────
            closes = hist["Close"]
            ma20 = float(closes.rolling(20).mean().iloc[-1])
            ma50 = float(closes.rolling(50).mean().iloc[-1])
            current = float(closes.iloc[-1])

            # RSI (14일)
            delta = closes.diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            loss_val = float(loss.iloc[-1])
            gain_val = float(gain.iloc[-1])
            rs = gain_val / loss_val if loss_val != 0 else 0
            rsi = float(100 - (100 / (1 + rs))) if rs else 50.0

            # MACD
            ema12 = closes.ewm(span=12, adjust=False).mean()
            ema26 = closes.ewm(span=26, adjust=False).mean()
            macd_line = ema12 - ema26
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            macd_val = float(macd_line.iloc[-1])
            sig_val = float(signal_line.iloc[-1])

            signals: list = []
            score = 0

            # MA20
            if current > ma20:
                signals.append(TechSignal(name="MA20 (20일 이평)", value=f"{ma20:.2f}", signal="bullish"))
                score += 1
            else:
                signals.append(TechSignal(name="MA20 (20일 이평)", value=f"{ma20:.2f}", signal="bearish"))
                score -= 1

            # MA50
            if current > ma50:
                signals.append(TechSignal(name="MA50 (50일 이평)", value=f"{ma50:.2f}", signal="bullish"))
                score += 1
            else:
                signals.append(TechSignal(name="MA50 (50일 이평)", value=f"{ma50:.2f}", signal="bearish"))
                score -= 1

            # 골든/데드 크로스
            if ma20 > ma50:
                signals.append(TechSignal(name="이평 교차 신호", value="골든 크로스", signal="bullish"))
                score += 1
            else:
                signals.append(TechSignal(name="이평 교차 신호", value="데드 크로스", signal="bearish"))
                score -= 1

            # RSI
            rsi_r = round(rsi, 1)
            if rsi < 30:
                signals.append(TechSignal(name="RSI (14일)", value=str(rsi_r), signal="bullish"))
                score += 2
            elif rsi > 70:
                signals.append(TechSignal(name="RSI (14일)", value=str(rsi_r), signal="bearish"))
                score -= 2
            else:
                signals.append(TechSignal(name="RSI (14일)", value=str(rsi_r), signal="neutral"))

            # MACD
            if macd_val > sig_val:
                signals.append(TechSignal(name="MACD", value=f"{macd_val:.4f}", signal="bullish"))
                score += 1
            else:
                signals.append(TechSignal(name="MACD", value=f"{macd_val:.4f}", signal="bearish"))
                score -= 1

            self.tech_signals = signals

            # ── 투자 추천 결정 ─────────────────────────────────────────────
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
