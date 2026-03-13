================================================================================
  주식 추천 앱 (Stock Recommendation App)
  기술적 분석 기반 매수/매도 추천 + 전고점/VWAP 돌파 스캐너
================================================================================

1. 개요
--------------------------------------------------------------------------------
Python 풀스택 웹프레임워크 Reflex로 구축한 주식 분석 웹앱.
Yahoo Finance(yfinance) 에서 데이터를 가져와 기술적 지표를 계산하고,
개별 종목 분석과 종목 스캔 두 가지 기능을 제공한다.

  실행:  cd C:\project\finance
         C:\Users\Administrator\miniconda3\Scripts\reflex.exe run
  접속:  http://localhost:3000  (포트 충돌 시 3001, 3002... 순으로 증가)


2. 기술 스택
--------------------------------------------------------------------------------
  - Python 환경  : C:\Users\Administrator\miniconda3\python.exe
  - 프레임워크   : Reflex 0.8.x  (Radix UI 기반, Python으로 프론트/백엔드 통합)
  - 주가 데이터  : yfinance 1.2.x  (Yahoo Finance API 래퍼)
  - 차트         : Reflex recharts (내장 Recharts 바인딩)
  - 데이터 출처  : Yahoo Finance 1곳  (종목 정보 + 과거 가격 모두 동일 소스)


3. 프로젝트 구조
--------------------------------------------------------------------------------
  C:\project\finance\
  ├── rxconfig.py          Reflex 앱 설정  (app_name="finance")
  ├── requirements.txt     의존 패키지 목록
  ├── .gitignore
  ├── README.txt           ← 이 파일
  └── finance\
      ├── __init__.py      (빈 파일)
      ├── state.py         상태 관리 + 비즈니스 로직 (데이터 수집, 지표 계산)
      └── finance.py       UI 컴포넌트 + 페이지 정의


4. state.py  —  상태 및 로직
--------------------------------------------------------------------------------

[ 데이터 클래스 (rx.Base 서브클래스) ]

  TechSignal
    기술적 지표 한 줄을 표현하는 단순 DTO.
    필드: name(지표명), value(수치 문자열), signal("bullish"/"bearish"/"neutral")

  BreakoutResult
    전고점 돌파 스캐너 결과 한 종목.
    필드: ticker, name, formatted_price, formatted_prev_high,
           formatted_breakout_pct, formatted_change_pct,
           change_positive(등락 방향), breakout_date(최초 돌파일)
    ※ 모든 수치는 표시용 문자열로 미리 포맷팅 (Reflex Var에서 f-string 불가)

  VWAPResult
    VWAP 돌파 스캐너 결과 한 종목.
    필드: ticker, name, formatted_price, formatted_vwap, formatted_vwap_pct,
           formatted_change_pct, change_positive, crossover_date(교차일)

[ 종목 목록 상수 ]

  KOSPI200_LIST   약 160개 코스피200 종목 티커 (섹터별 주석 포함)
  DEFAULT_SCAN_LIST = 미국 주요주 16개 + KOSPI200_LIST  (스캐너 기본 대상)

[ State 클래스 (rx.State 서브클래스) ]

  ── 종목 분석 상태 변수 ─────────────────────────────────────────────────────
  ticker_input      입력창 문자열
  company_name      회사명
  current_ticker    현재 조회 중인 티커
  price             현재가 (float)
  change            전일 대비 등락 (float)
  change_pct        등락률 (float)
  volume            거래량 (포맷팅 문자열)
  market_cap        시가총액 (포맷팅 문자열)
  pe_ratio          PER (포맷팅 문자열)
  week_52_high/low  52주 최고/최저가 (float)
  currency          통화 코드 ("KRW"/"USD")
  chart_data        6개월 일봉 리스트  [{date, close, ma20, ma50, vwap}, ...]
  tech_signals      TechSignal 리스트 (MA20, MA50, 골든크로스, RSI, MACD)
  recommendation    최종 추천 문자열 ("강력 매수" ~ "강력 매도")
  recommendation_reason  추천 근거 텍스트
  loading / error / has_data  UI 상태 플래그

  ── 전고점 돌파 스캐너 상태 변수 ────────────────────────────────────────────
  scan_stocks       스캔 대상 티커 리스트 (기본 DEFAULT_SCAN_LIST)
  scan_input        종목 추가 입력창
  scan_results      BreakoutResult 리스트 (스캔 결과)
  scanning          스캔 진행 중 여부
  scan_progress     처리 완료 종목 수
  scan_total        전체 대상 종목 수
  scan_done         스캔 완료 여부
  scan_period_months  전고점 분석 기간 (1~12개월, 기본 6)
  scan_recent_days  최근 N 거래일 이내 돌파만 인정 (기본 15)

  ── VWAP 스캐너 상태 변수 ───────────────────────────────────────────────────
  vwap_scan_results   VWAPResult 리스트
  vwap_scanning       스캔 진행 중 여부
  vwap_scan_progress / vwap_scan_total / vwap_scan_done
  vwap_period_months  VWAP 계산 기간 (1~12개월, 기본 3)
  vwap_crossover_days 돌파 시점 제한 (캘린더일, 기본 7일 = 1주일)

  ── 탭 상태 ─────────────────────────────────────────────────────────────────
  active_tab        현재 활성 탭 ("analysis" / "scanner")
                    스캐너 결과 클릭 시 프로그래밍으로 전환

  ── Computed vars (@rx.var) ─────────────────────────────────────────────────
  price_color              등락에 따른 색상 ("green"/"red")
  formatted_price          통화 기호 포함 가격 문자열
  formatted_change         등락 포맷 문자열
  formatted_52w_high/low   52주 최고/최저 포맷 문자열
  recommendation_color     추천 등급에 따른 색상 테마
  scan_progress_pct        전고점 스캔 진행률 0~100
  scan_status_text         진행 상태 메시지
  scan_period_label        "N개월" 문자열
  scan_stock_count         스캔 대상 종목 수
  has_scan_results / scan_result_count
  vwap_progress_pct        VWAP 스캔 진행률
  vwap_status_text
  vwap_period_label        "N개월"
  vwap_crossover_label     "1주일" / "N일" 등
  has_vwap_results / vwap_result_count

  ── Event Handlers ──────────────────────────────────────────────────────────
  set_ticker(value)           입력창 동기화
  handle_key_press(key)       Enter → search_stock 호출
  quick_search(ticker)        인기 종목 배지 클릭 → 검색
  open_stock_from_scanner(ticker)
      스캐너 결과 카드 클릭 시 active_tab="analysis" 전환 후 검색

  search_stock()  [async]
      1. yf.Ticker(ticker).info  → 현재가, 회사명, 거래량, 시총, PER
      2. ticker.history(period="6mo")  → 6개월 일봉
      3. 차트 데이터 생성: close + MA20 + MA50 + VWAP(누적) 시리즈 포함
      4. 기술적 지표 계산:
           MA20, MA50  —  rolling(20/50).mean()
           골든/데드크로스  —  MA20 vs MA50 대소 비교
           RSI(14)  —  gain/loss rolling 평균, RS = gain/loss
           MACD  —  EMA(12) - EMA(26), Signal = EMA(9)
      5. score 합산 → 5단계 추천 (강력매수/매수/중립/매도/강력매도)

  set_scan_period / set_vwap_period / set_vwap_crossover_days
      슬라이더 on_change 핸들러 (value: list 수신)
  add_scan_stock / remove_scan_stock / reset_scan
      스캔 대상 종목 목록 편집

  run_breakout_scan()  [async generator]
      1. yf.download(모든 티커, period) — 단일 배치 요청
      2. 각 티커 반복:
           close_s[-scan_recent_days:] 를 제외한 이전 구간의 max(High) = 전고점
           현재가 > 전고점  →  돌파 확인
           돌파 첫 날 = crossover[crossover].index[-1]
           yf.Ticker(ticker).info 로 회사명/통화 조회 (돌파 종목만)
      3. 돌파율 내림차순 정렬 → scan_results

  run_vwap_scan()  [async generator]
      1. yf.download(모든 티커, period) — 단일 배치 요청
      2. 각 티커 반복:
           VWAP = Σ((고+저+종)/3 × 거래량) / Σ(거래량)  [기간 전체 단일값]
           현재가 <= VWAP 이면 스킵
           above = close_s > vwap  (불리언 시리즈)
           crossover = above & (~above.shift(1))  →  교차 날짜 목록
           마지막 교차일 ≤ vwap_crossover_days 이내이면 포함
           yf.Ticker(ticker).info 로 회사명/통화 조회
      3. VWAP 대비 % 내림차순 정렬 → vwap_scan_results


5. finance.py  —  UI 컴포넌트
--------------------------------------------------------------------------------

[ 공통 ]
  header()              상단 그라디언트 헤더 (제목 + 부제)

[ 종목 분석 탭 (value="analysis") ]
  search_section()      검색 입력창 + 인기 종목 배지 (AAPL, MSFT, GOOGL ...)
  stock_info_card()     현재가, 등락, 거래량, 시총, PER, 52주 고/저
  price_chart()         6개월 라인 차트 (종가/MA20/MA50/VWAP 4개 라인)
                        색상: 종가=인디고, MA20=앰버, MA50=빨강, VWAP=초록
  tech_analysis_card()  기술적 지표 테이블 (rx.foreach(tech_signals))
  recommendation_card() 추천 배지 + 근거 텍스트 + 면책 안내
  analysis_tab()        위 컴포넌트 조합 + 로딩/에러/빈 상태 처리

[ 스캐너 탭 (value="scanner") ]
  scan_stock_list_card()      스캔 대상 종목 목록 카드
                              배지로 표시, × 버튼으로 제거, 입력창으로 추가
  render_scan_stock_badge()   종목 배지 단위 컴포넌트

  ── 전고점 돌파 서브탭 ────────────────────────────────────────────────────
  breakout_scan_section()     기간 슬라이더(1~12개월) + 스캔 버튼 + 결과 목록
  render_breakout_card()      결과 카드 1개
                              클릭 → open_stock_from_scanner() → 분석 탭 이동
                              hover 시 인디고 테두리

  ── VWAP 돌파 서브탭 ─────────────────────────────────────────────────────
  vwap_scan_section()         VWAP 계산 기간 슬라이더(1~12개월)
                              + 돌파 시점 제한 슬라이더(1~30일, 기본 7일)
                              + VWAP 공식 설명
                              + 스캔 버튼 + 결과 목록
  render_vwap_card()          결과 카드 1개 (바이올렛 색상)
                              클릭 → open_stock_from_scanner() → 분석 탭 이동

  _scan_progress_card()       재사용 진행률 카드 (spinner + progress bar)
  scanner_tab()               scan_stock_list_card + 서브탭(breakout/vwap)

[ 페이지 조립 ]
  index()     외부 탭 루트 (value=State.active_tab, on_change=State.set_active_tab)
              → "종목 분석" 탭 / "전고점 돌파 스캐너" 탭

  app = rx.App(...)
  app.add_page(index, route="/", title="주식 추천 앱")


6. 데이터 흐름
--------------------------------------------------------------------------------

  [사용자 입력]
       │
       ▼
  Event Handler (state.py)
       │  yf.Ticker / yf.download  (Yahoo Finance — 단일 출처)
       │
       ▼
  State 변수 업데이트
       │  Reflex 자동 WebSocket 동기화
       │
       ▼
  UI 컴포넌트 재렌더링 (finance.py)

  스캐너는 async generator 방식으로 yield마다 진행률이 실시간 갱신됨.
  배치 다운로드(yf.download) 1회로 전 종목 OHLCV 수집 후
  돌파 확정된 종목만 yf.Ticker(t).info 를 개별 호출하여 API 요청 최소화.


7. 기술적 지표 계산 요약
--------------------------------------------------------------------------------

  MA20 / MA50   closes.rolling(N).mean()
  골든크로스    MA20 > MA50
  데드크로스    MA20 < MA50
  RSI(14)       delta = close.diff()
                gain = delta.clip(lower=0).rolling(14).mean()
                loss = (-delta.clip(upper=0)).rolling(14).mean()
                RSI = 100 - 100 / (1 + gain/loss)
  MACD          EMA(12) - EMA(26);  Signal = EMA(9)
                MACD > Signal  → 상승 신호
  VWAP (차트)   cumsum(TP×Vol) / cumsum(Vol)  — 기간 시작부터 일별 누적
  VWAP (스캐너) sum(TP×Vol) / sum(Vol)  — 기간 전체 단일 수치

  추천 점수 기준 (score):
    +1: 현재가 > MA20,  +1: 현재가 > MA50,  +1: 골든크로스
    +1: RSI < 70 (과매수 아님),  +1: MACD > Signal
    (반대 조건은 각 -1)
    score >= 3  → 강력 매수
    score == 2  → 매수
    score == 0 or 1  → 중립
    score == -1 or -2  → 매도
    score <= -3  → 강력 매도


8. GitHub
--------------------------------------------------------------------------------
  저장소: https://github.com/KyongpilTae-pixel/stock-recommendation-app
  브랜치: main
  푸시:   git push origin main


================================================================================
