import reflex as rx
from finance.state import State, TechSignal

POPULAR_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "NVDA",
    "TSLA", "AMZN", "META", "005930.KS",
]

# ── 헤더 ──────────────────────────────────────────────────────────────────────

def header() -> rx.Component:
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "📈 주식 추천 앱",
                    size="8",
                    color="white",
                    font_weight="800",
                ),
                rx.text(
                    "기술적 분석 기반 매수 / 매도 추천 서비스",
                    color="rgba(255,255,255,0.65)",
                    size="3",
                ),
                align="center",
                spacing="2",
                padding_y="2.5em",
            ),
            max_width="1200px",
            margin="0 auto",
        ),
        background="linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
        width="100%",
    )


# ── 검색 섹션 ─────────────────────────────────────────────────────────────────

def search_section() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.input(
                placeholder="종목 코드 입력  (예: AAPL, MSFT, 005930.KS)",
                value=State.ticker_input,
                on_change=State.set_ticker,
                on_key_press=State.handle_key_press,
                size="3",
                width="420px",
            ),
            rx.button(
                "검색",
                on_click=State.search_stock,
                size="3",
                color_scheme="indigo",
                loading=State.loading,
            ),
            spacing="3",
        ),
        rx.hstack(
            rx.text("인기 종목:", color="gray", size="2"),
            *[
                rx.badge(
                    stock,
                    on_click=State.search_stock(stock),
                    cursor="pointer",
                    color_scheme="indigo",
                    variant="soft",
                    size="2",
                    _hover={"opacity": "0.7"},
                )
                for stock in POPULAR_STOCKS
            ],
            wrap="wrap",
            spacing="2",
            align="center",
        ),
        align="center",
        spacing="4",
        padding_y="2em",
    )


# ── 종목 정보 카드 ────────────────────────────────────────────────────────────

def info_item(label: str, value) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="1", color="gray", weight="medium"),
        rx.text(value, size="3", weight="bold"),
        align="center",
        spacing="1",
        padding="0.5em 0.75em",
    )


def stock_info_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(State.company_name, size="5", weight="bold"),
                    rx.badge(
                        State.current_ticker,
                        color_scheme="indigo",
                        variant="surface",
                    ),
                    align="start",
                    spacing="2",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.heading(
                        State.formatted_price,
                        size="7",
                        color=State.price_color,
                        weight="800",
                    ),
                    rx.text(
                        State.formatted_change,
                        color=State.price_color,
                        size="3",
                        weight="medium",
                    ),
                    align="end",
                    spacing="1",
                ),
                width="100%",
                align="start",
            ),
            rx.separator(width="100%"),
            rx.grid(
                info_item("거래량", State.volume),
                info_item("시가총액", State.market_cap),
                info_item("PER", State.pe_ratio),
                info_item("52주 최고", State.formatted_52w_high),
                info_item("52주 최저", State.formatted_52w_low),
                columns="5",
                width="100%",
                gap="2",
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        padding="1.5em",
    )


# ── 주가 차트 ─────────────────────────────────────────────────────────────────

def price_chart() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("📊 주가 차트  (6개월)", size="4", weight="bold"),
            rx.recharts.responsive_container(
                rx.recharts.line_chart(
                    rx.recharts.line(
                        data_key="close",
                        stroke="#6366f1",
                        stroke_width=2,
                        dot=False,
                    ),
                    rx.recharts.x_axis(data_key="date"),
                    rx.recharts.y_axis(domain=["auto", "auto"]),
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3", opacity=0.4),
                    rx.recharts.graphing_tooltip(),
                    data=State.chart_data,
                ),
                width="100%",
                height=300,
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        padding="1.5em",
    )


# ── 기술적 분석 카드 ──────────────────────────────────────────────────────────

def signal_badge(signal: str) -> rx.Component:
    return rx.cond(
        signal == "bullish",
        rx.badge("📈 상승", color_scheme="green", variant="soft"),
        rx.cond(
            signal == "bearish",
            rx.badge("📉 하락", color_scheme="red", variant="soft"),
            rx.badge("➡️ 중립", color_scheme="gray", variant="soft"),
        ),
    )


def render_signal(signal: TechSignal) -> rx.Component:
    return rx.hstack(
        rx.text(signal.name, size="2", width="11em"),
        rx.text(signal.value, size="2", color="gray", width="8em"),
        signal_badge(signal.signal),
        width="100%",
        padding_y="0.6em",
        border_bottom="1px solid var(--gray-4)",
        align="center",
    )


def tech_analysis_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("🔍 기술적 분석", size="4", weight="bold"),
            rx.separator(width="100%"),
            rx.hstack(
                rx.text("지표", size="1", color="gray", width="11em", weight="bold"),
                rx.text("값", size="1", color="gray", width="8em", weight="bold"),
                rx.text("신호", size="1", color="gray", weight="bold"),
                width="100%",
                padding_bottom="0.4em",
            ),
            rx.foreach(State.tech_signals, render_signal),
            spacing="2",
            width="100%",
        ),
        width="100%",
        padding="1.5em",
        height="100%",
    )


# ── 투자 추천 카드 ────────────────────────────────────────────────────────────

def recommendation_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("💡 투자 추천", size="4", weight="bold"),
            rx.separator(width="100%"),
            rx.center(
                rx.badge(
                    State.recommendation,
                    color_scheme=State.recommendation_color,
                    size="3",
                    variant="solid",
                    padding="0.8em 2.5em",
                    font_size="1.4em",
                    font_weight="800",
                ),
                padding_y="1.5em",
            ),
            rx.text(
                State.recommendation_reason,
                size="3",
                color="gray",
                text_align="center",
                line_height="1.7",
            ),
            rx.separator(width="100%"),
            rx.box(
                rx.text(
                    "⚠️  본 추천은 기술적 분석에 기반한 참고 정보입니다. "
                    "실제 투자 결정은 반드시 본인 판단 하에 이루어져야 하며, "
                    "투자 손실에 대한 책임은 투자자 본인에게 있습니다.",
                    size="1",
                    color="gray",
                    text_align="center",
                    line_height="1.6",
                ),
                background="var(--amber-2)",
                border="1px solid var(--amber-6)",
                border_radius="8px",
                padding="0.8em 1em",
            ),
            spacing="4",
            width="100%",
            align="center",
        ),
        width="100%",
        padding="1.5em",
        height="100%",
    )


# ── 메인 페이지 ───────────────────────────────────────────────────────────────

def index() -> rx.Component:
    return rx.box(
        header(),
        rx.container(
            search_section(),
            # 에러 메시지
            rx.cond(
                State.error != "",
                rx.box(
                    rx.text(f"❌  {State.error}", size="2", color="var(--red-11)"),
                    background="var(--red-2)",
                    border="1px solid var(--red-6)",
                    border_radius="8px",
                    padding="0.8em 1.2em",
                    margin_bottom="1.5em",
                    width="100%",
                ),
                rx.box(),
            ),
            # 메인 콘텐츠
            rx.cond(
                State.loading,
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3"),
                        rx.text("데이터를 불러오는 중...", color="gray", size="3"),
                        align="center",
                        spacing="4",
                    ),
                    padding="5em",
                ),
                rx.cond(
                    State.has_data,
                    rx.vstack(
                        stock_info_card(),
                        price_chart(),
                        rx.grid(
                            tech_analysis_card(),
                            recommendation_card(),
                            columns="2",
                            gap="4",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    # 초기 화면
                    rx.center(
                        rx.vstack(
                            rx.text("🔍", font_size="4em"),
                            rx.text(
                                "종목 코드를 검색하거나 인기 종목을 클릭하세요",
                                color="gray",
                                size="4",
                            ),
                            rx.text(
                                "AAPL, MSFT, 005930.KS 등 글로벌 및 국내 종목 지원",
                                color="gray",
                                size="2",
                            ),
                            align="center",
                            spacing="3",
                        ),
                        padding="5em",
                    ),
                ),
            ),
            max_width="1200px",
            padding="2em",
            margin="0 auto",
        ),
        min_height="100vh",
        background="var(--gray-1)",
    )


# ── 앱 설정 ───────────────────────────────────────────────────────────────────

app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="indigo",
        radius="medium",
    ),
)
app.add_page(index, route="/", title="주식 추천 앱")
