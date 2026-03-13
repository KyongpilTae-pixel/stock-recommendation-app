import reflex as rx
from finance.state import State, TechSignal, BreakoutResult, VWAPResult, DEFAULT_SCAN_LIST

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
                    "기술적 분석 기반 매수 / 매도 추천  |  전고점 돌파 스캐너",
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


# ── 종목 분석 탭 ───────────────────────────────────────────────────────────────

def search_section() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.input(
                placeholder="종목 코드 입력  (예: AAPL, MSFT, 005930.KS)",
                value=State.ticker_input,
                on_change=State.set_ticker,
                on_key_down=State.handle_key_press,
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
                    on_click=State.quick_search(stock),
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
                    rx.badge(State.current_ticker, color_scheme="indigo", variant="surface"),
                    align="start",
                    spacing="2",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.heading(
                        State.formatted_price,
                        size="7",
                        color=State.price_color,
                        weight="bold",
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
                    "실제 투자 결정은 반드시 본인 판단 하에 이루어져야 합니다.",
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


def analysis_tab() -> rx.Component:
    return rx.vstack(
        search_section(),
        rx.cond(
            State.error != "",
            rx.box(
                rx.text("❌  " + State.error, size="2", color="var(--red-11)"),
                background="var(--red-2)",
                border="1px solid var(--red-6)",
                border_radius="8px",
                padding="0.8em 1.2em",
                margin_bottom="1.5em",
                width="100%",
            ),
            rx.box(),
        ),
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
        width="100%",
        spacing="0",
    )


# ── 스캐너 공통 컴포넌트 ────────────────────────────────────────────────────────

def render_scan_stock_badge(stock: str) -> rx.Component:
    return rx.hstack(
        rx.text(stock, size="1", weight="medium"),
        rx.text(
            "×",
            size="1",
            color="var(--red-9)",
            cursor="pointer",
            on_click=State.remove_scan_stock(stock),
            _hover={"color": "var(--red-11)"},
            font_weight="bold",
        ),
        align="center",
        background="var(--gray-3)",
        border_radius="999px",
        padding="0.25em 0.7em",
        spacing="1",
    )


def scan_stock_list_card() -> rx.Component:
    """스캔 대상 종목 목록 카드 (전고점 / VWAP 공유)"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("스캔 대상 종목", size="4", weight="bold"),
                rx.badge(State.scan_stock_count, color_scheme="gray", variant="surface"),
                rx.spacer(),
                rx.button(
                    "초기화",
                    on_click=State.reset_scan,
                    size="1",
                    variant="ghost",
                    color_scheme="gray",
                ),
                align="center",
                width="100%",
            ),
            rx.separator(width="100%"),
            rx.box(
                rx.foreach(State.scan_stocks, render_scan_stock_badge),
                display="flex",
                flex_wrap="wrap",
                gap="0.5em",
                width="100%",
                padding_y="0.5em",
            ),
            rx.separator(width="100%"),
            rx.hstack(
                rx.input(
                    placeholder="종목 추가  (예: INTC, 삼성전자: 005930.KS)",
                    value=State.scan_input,
                    on_change=State.set_scan_input,
                    on_key_down=State.handle_scan_key,
                    size="2",
                    width="320px",
                ),
                rx.button(
                    "추가",
                    on_click=State.add_scan_stock,
                    size="2",
                    color_scheme="gray",
                    variant="soft",
                ),
                spacing="2",
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        padding="1.5em",
    )


def render_breakout_card(result: BreakoutResult) -> rx.Component:
    return rx.card(
        rx.hstack(
            # 왼쪽: 종목 정보
            rx.vstack(
                rx.hstack(
                    rx.badge(result.ticker, color_scheme="indigo", variant="surface", size="2"),
                    rx.badge(
                        result.formatted_change_pct,
                        color_scheme=rx.cond(result.change_positive, "green", "red"),
                        variant="soft",
                        size="2",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.text(result.name, size="2", color="gray"),
                rx.hstack(
                    rx.text("돌파일:", size="1", color="gray"),
                    rx.text(result.breakout_date, size="1", weight="medium", color="var(--indigo-11)"),
                    spacing="1",
                ),
                spacing="2",
                align="start",
            ),
            rx.spacer(),
            # 오른쪽: 가격 및 돌파 정보
            rx.vstack(
                rx.text(result.formatted_price, size="5", weight="bold"),
                rx.hstack(
                    rx.text("전고점", size="1", color="gray"),
                    rx.text(result.formatted_prev_high, size="1", color="gray", weight="medium"),
                    spacing="1",
                ),
                rx.badge(
                    "🚀 " + result.formatted_breakout_pct + " 돌파",
                    color_scheme="green",
                    variant="solid",
                    size="2",
                ),
                align="end",
                spacing="1",
            ),
            width="100%",
            align="center",
            padding="0.5em",
        ),
        width="100%",
    )


def render_vwap_card(result: VWAPResult) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.badge(result.ticker, color_scheme="violet", variant="surface", size="2"),
                    rx.badge(
                        result.formatted_change_pct,
                        color_scheme=rx.cond(result.change_positive, "green", "red"),
                        variant="soft",
                        size="2",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.text(result.name, size="2", color="gray"),
                rx.hstack(
                    rx.text("돌파일:", size="1", color="gray"),
                    rx.text(result.crossover_date, size="1", weight="medium", color="var(--violet-11)"),
                    spacing="1",
                ),
                spacing="2",
                align="start",
            ),
            rx.spacer(),
            rx.vstack(
                rx.text(result.formatted_price, size="5", weight="bold"),
                rx.hstack(
                    rx.text("VWAP", size="1", color="gray"),
                    rx.text(result.formatted_vwap, size="1", color="gray", weight="medium"),
                    spacing="1",
                ),
                rx.badge(
                    "📊 VWAP +" + result.formatted_vwap_pct,
                    color_scheme="violet",
                    variant="solid",
                    size="2",
                ),
                align="end",
                spacing="1",
            ),
            width="100%",
            align="center",
            padding="0.5em",
        ),
        width="100%",
    )


def _scan_progress_card(scanning, status_text, progress_pct) -> rx.Component:
    return rx.cond(
        scanning,
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.spinner(size="2"),
                    rx.text(status_text, size="3"),
                    spacing="3",
                    align="center",
                ),
                rx.progress(value=progress_pct, width="100%"),
                spacing="3",
                width="100%",
            ),
            width="100%",
            padding="1.5em",
        ),
        rx.box(),
    )


def breakout_scan_section() -> rx.Component:
    return rx.vstack(
        # 기간 슬라이더
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.text("📅 전고점 분석 기간", size="3", weight="bold"),
                    rx.badge(State.scan_period_label, color_scheme="indigo", variant="surface"),
                    spacing="3",
                    align="center",
                ),
                rx.slider(
                    min=1, max=12, step=1,
                    value=[State.scan_period_months],
                    on_change=State.set_scan_period,
                    width="100%",
                ),
                rx.hstack(
                    rx.text("1개월", size="1", color="gray"),
                    rx.spacer(),
                    rx.text("최근 15거래일 내 돌파만 인정", size="1", color="gray"),
                    rx.spacer(),
                    rx.text("12개월", size="1", color="gray"),
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            width="100%",
            padding="1.5em",
        ),
        # 스캔 버튼
        rx.center(
            rx.button(
                "🚀  전고점 돌파 스캔 시작",
                on_click=State.run_breakout_scan,
                loading=State.scanning,
                size="3",
                color_scheme="indigo",
                width="320px",
            ),
            width="100%",
        ),
        # 진행률
        _scan_progress_card(State.scanning, State.scan_status_text, State.scan_progress_pct),
        # 결과
        rx.cond(
            State.scan_done,
            rx.cond(
                State.has_scan_results,
                rx.vstack(
                    rx.hstack(
                        rx.heading("🎯 전고점 돌파 종목", size="4", weight="bold"),
                        rx.badge(State.scan_result_count, color_scheme="green", variant="solid", size="2"),
                        rx.text("개 발견", size="3", color="gray"),
                        align="center",
                        spacing="2",
                    ),
                    rx.text(
                        "최근 15거래일 이내 전고점을 돌파한 종목 · 돌파율 순 정렬",
                        size="2", color="gray",
                    ),
                    rx.foreach(State.scan_results, render_breakout_card),
                    spacing="3",
                    width="100%",
                ),
                rx.center(
                    rx.vstack(
                        rx.text("😔", font_size="3em"),
                        rx.text("전고점 돌파 종목이 없습니다.", size="4", color="gray"),
                        align="center", spacing="3",
                    ),
                    padding="4em",
                ),
            ),
            rx.cond(
                State.scanning,
                rx.box(),
                rx.center(
                    rx.vstack(
                        rx.text("🔭", font_size="3em"),
                        rx.text("스캔 버튼을 클릭하면 전고점 돌파 종목을 찾아드립니다", color="gray", size="3"),
                        align="center", spacing="3",
                    ),
                    padding="4em",
                ),
            ),
        ),
        spacing="4",
        width="100%",
        padding_top="1.5em",
    )


def vwap_scan_section() -> rx.Component:
    return rx.vstack(
        # VWAP 기간 슬라이더
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.text("📅 VWAP 계산 기간", size="3", weight="bold"),
                    rx.badge(State.vwap_period_label, color_scheme="violet", variant="surface"),
                    spacing="3",
                    align="center",
                ),
                rx.slider(
                    min=1, max=12, step=1,
                    value=[State.vwap_period_months],
                    on_change=State.set_vwap_period,
                    width="100%",
                ),
                rx.hstack(
                    rx.text("1개월", size="1", color="gray"),
                    rx.spacer(),
                    rx.text("기간 내 거래량 가중 평균가격 기준", size="1", color="gray"),
                    rx.spacer(),
                    rx.text("12개월", size="1", color="gray"),
                    width="100%",
                ),
                rx.box(
                    rx.text(
                        "💡  VWAP = Σ(고가+저가+종가)/3 × 거래량) / Σ(거래량)  "
                        "· 최근 30일 이내 VWAP 하단→상단 교차 종목만 표시",
                        size="1",
                        color="gray",
                    ),
                    background="var(--violet-2)",
                    border="1px solid var(--violet-5)",
                    border_radius="6px",
                    padding="0.6em 0.8em",
                ),
                spacing="3",
                width="100%",
            ),
            width="100%",
            padding="1.5em",
        ),
        # 스캔 버튼
        rx.center(
            rx.button(
                "📊  VWAP 돌파 스캔 시작",
                on_click=State.run_vwap_scan,
                loading=State.vwap_scanning,
                size="3",
                color_scheme="violet",
                width="320px",
            ),
            width="100%",
        ),
        # 진행률
        _scan_progress_card(State.vwap_scanning, State.vwap_status_text, State.vwap_progress_pct),
        # 결과
        rx.cond(
            State.vwap_scan_done,
            rx.cond(
                State.has_vwap_results,
                rx.vstack(
                    rx.hstack(
                        rx.heading("📊 VWAP 상단 돌파 종목", size="4", weight="bold"),
                        rx.badge(State.vwap_result_count, color_scheme="violet", variant="solid", size="2"),
                        rx.text("개 발견", size="3", color="gray"),
                        align="center",
                        spacing="2",
                    ),
                    rx.text(
                        "최근 30일 이내 VWAP 하단→상단 교차 종목 · VWAP 대비 % 순 정렬",
                        size="2", color="gray",
                    ),
                    rx.foreach(State.vwap_scan_results, render_vwap_card),
                    spacing="3",
                    width="100%",
                ),
                rx.center(
                    rx.vstack(
                        rx.text("😔", font_size="3em"),
                        rx.text("VWAP 돌파 종목이 없습니다.", size="4", color="gray"),
                        align="center", spacing="3",
                    ),
                    padding="4em",
                ),
            ),
            rx.cond(
                State.vwap_scanning,
                rx.box(),
                rx.center(
                    rx.vstack(
                        rx.text("📊", font_size="3em"),
                        rx.text("스캔 버튼을 클릭하면 VWAP 돌파 종목을 찾아드립니다", color="gray", size="3"),
                        align="center", spacing="3",
                    ),
                    padding="4em",
                ),
            ),
        ),
        spacing="4",
        width="100%",
        padding_top="1.5em",
    )


def scanner_tab() -> rx.Component:
    return rx.vstack(
        # 공유: 스캔 대상 종목 목록
        scan_stock_list_card(),
        # 서브탭: 전고점 돌파 / VWAP 돌파
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("📈  전고점 돌파", value="breakout"),
                rx.tabs.trigger("📊  VWAP 돌파", value="vwap"),
                size="2",
            ),
            rx.tabs.content(breakout_scan_section(), value="breakout"),
            rx.tabs.content(vwap_scan_section(), value="vwap"),
            default_value="breakout",
            width="100%",
        ),
        spacing="4",
        width="100%",
        padding_y="2em",
    )


# ── 메인 페이지 ───────────────────────────────────────────────────────────────

def index() -> rx.Component:
    return rx.box(
        header(),
        rx.container(
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("📊  종목 분석", value="analysis"),
                    rx.tabs.trigger("🚀  전고점 돌파 스캐너", value="scanner"),
                    size="2",
                ),
                rx.tabs.content(analysis_tab(), value="analysis"),
                rx.tabs.content(scanner_tab(), value="scanner"),
                default_value="analysis",
                width="100%",
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
