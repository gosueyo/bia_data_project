"""
여러 화면(pages_logic)에서 공통으로 쓰이는 데이터 처리 함수 모음.

- classify_columns: 숫자형/범주형 컬럼 구분
- get_missing_summary: 컬럼별 결측치 개수/비율 계산
"""

import pandas as pd


def classify_columns(df: pd.DataFrame):
    """
    DataFrame의 컬럼을 숫자형과 범주형(그 외)으로 나눠서 반환한다.

    반환값: (numeric_cols, categorical_cols)
    """
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = [c for c in df.columns if c not in numeric_cols]
    return numeric_cols, categorical_cols


def get_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    컬럼별 결측치 개수와 비율(%)을 정리한 요약 표를 반환한다.
    """
    missing_count = df.isnull().sum()
    missing_ratio = (missing_count / len(df) * 100).round(2)

    summary = pd.DataFrame(
        {
            "컬럼명": df.columns,
            "결측치 개수": missing_count.values,
            "결측치 비율(%)": missing_ratio.values,
        }
    )
    return summary


def get_descriptive_stats(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    선택한 숫자형 컬럼의 기술통계(개수/평균/중앙값/표준편차/최소/최대)를 반환한다.
    결측치는 자동으로 제외하고 계산한다 (pandas 기본 동작).
    """
    series = df[column].dropna()

    stats = {
        "개수(결측 제외)": series.count(),
        "평균": series.mean(),
        "중앙값": series.median(),
        "표준편차": series.std(),
        "최소값": series.min(),
        "최대값": series.max(),
    }

    stats_df = pd.DataFrame(stats, index=[column]).round(2)
    return stats_df


def detect_id_time_candidates(df: pd.DataFrame):
    """
    컬럼명을 기준으로 ID(대상자 식별) 후보와 측정일/측정차수 후보 컬럼을 추정한다.
    이름에 특정 키워드가 포함되어 있는지로 판단하는 '추정'이며, 100% 정확하지 않을 수 있다.
    날짜형(datetime) 타입인 컬럼은 이름과 무관하게 시간 후보로 포함한다.

    반환값: (id_candidates, time_candidates) - 둘 다 컬럼명 리스트
    """
    id_keywords = ["id", "아이디", "대상자", "환자", "subject", "피험자", "참가자", "번호"]
    time_keywords = ["date", "time", "일자", "날짜", "visit", "week", "회차", "측정일", "시점", "기간"]

    id_candidates = []
    time_candidates = []

    for col in df.columns:
        col_lower = str(col).lower()

        if any(keyword in col_lower for keyword in id_keywords):
            id_candidates.append(col)

        if any(keyword in col_lower for keyword in time_keywords):
            time_candidates.append(col)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            time_candidates.append(col)

    return id_candidates, time_candidates


def get_dtype_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    컬럼별 데이터 타입, 고유값 개수를 정리한 요약 표를 반환한다.
    """
    summary = pd.DataFrame(
        {
            "컬럼명": df.columns,
            "데이터 타입": [str(dtype) for dtype in df.dtypes],
            "고유값 개수": [df[c].nunique() for c in df.columns],
        }
    )
    return summary
