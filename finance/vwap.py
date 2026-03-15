"""VWAP 관련 데이터 클래스 및 순수 계산 함수 모음"""
import reflex as rx


# ── 데이터 클래스 ──────────────────────────────────────────────────────────────

class VWAPResult(rx.Base):
    ticker: str = ""
    name: str = ""
    formatted_price: str = ""
    formatted_vwap: str = ""
    formatted_vwap_pct: str = ""   # VWAP 대비 %
    formatted_change_pct: str = ""
    change_positive: bool = True
    crossover_date: str = ""       # VWAP 상단 돌파일


# ── 차트용 계산 ────────────────────────────────────────────────────────────────

def calc_chart_vwap(closes, highs, lows, volumes):
    """6개월 차트용 누적 VWAP 시리즈 반환 (pandas Series).

    기간 시작부터 매 거래일까지 누적 계산하여 일별 곡선으로 표시된다.
    공식: cumsum(TP × Volume) / cumsum(Volume)
          TP(Typical Price) = (고가 + 저가 + 종가) / 3
    """
    typical = (highs + lows + closes) / 3
    return (typical * volumes).cumsum() / volumes.cumsum()


# ── 스캐너용 계산 ──────────────────────────────────────────────────────────────

def calc_single_vwap(close_s, high_s, low_s, vol_s) -> float:
    """스캐너용 기간 전체 단일 VWAP 값 반환.

    기간 내 전체 거래량 가중 평균가격을 하나의 수치로 계산한다.
    공식: Σ(TP × Volume) / Σ(Volume)
    """
    typical = (high_s + low_s + close_s) / 3
    return float((typical * vol_s).sum() / vol_s.sum())


def find_vwap_crossover(close_s, vwap: float):
    """VWAP 하단 → 상단 교차일 탐색.

    Returns:
        (crossover_date: str, days_since: int)  — 교차 발생 시
        (None, None)                             — 기간 내 교차 없음
    """
    above = close_s > vwap
    prev_above = above.shift(1).fillna(False)
    crossover = above & (~prev_above)
    crossed_dates = crossover[crossover]

    if crossed_dates.empty:
        return None, None

    last_cross_idx = crossed_dates.index[-1]
    days_since = (close_s.index[-1] - last_cross_idx).days
    crossover_date = last_cross_idx.strftime("%Y.%m.%d")
    return crossover_date, days_since
