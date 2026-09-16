"""
1-3단계: 데이터 구조 확인 화면

기능:
- 업로드된 데이터가 없으면 안내 메시지만 표시
- 행 수 / 열 수
- 컬럼별 데이터 타입, 고유값 개수
- 컬럼별 결측치 개수/비율
- 숫자형 변수 목록 / 범주형(그 외) 변수 목록
- 데이터 미리보기
"""

import streamlit as st

from utils.data_utils import classify_columns, get_dtype_summary, get_missing_summary


def render():
    st.header("2. 데이터 구조 확인")

    df = st.session_state.get("df")

    if df is None:
        st.info("먼저 '데이터 업로드' 메뉴에서 파일을 업로드해주세요.")
        return

    file_name = st.session_state.get("file_name", "업로드된 파일")
    st.caption(f"현재 분석 중인 파일: {file_name}")

    # 1) 기본 크기 정보
    n_rows, n_cols = df.shape
    col1, col2 = st.columns(2)
    col1.metric("행(row) 수", n_rows)
    col2.metric("열(column) 수", n_cols)

    # 2) 컬럼별 데이터 타입 / 고유값
    st.subheader("컬럼별 데이터 타입 및 고유값 개수")
    dtype_summary = get_dtype_summary(df)
    st.dataframe(dtype_summary, use_container_width=True)

    # 3) 결측치 요약
    st.subheader("결측치 현황")
    missing_summary = get_missing_summary(df)
    st.dataframe(missing_summary, use_container_width=True)

    total_missing = df.isnull().sum().sum()
    if total_missing == 0:
        st.success("결측치가 없습니다.")
    else:
        st.warning(f"전체 결측치 개수: {total_missing}개. 결측치가 많은 변수는 분석 시 주의가 필요합니다.")

    # 4) 숫자형 / 범주형 변수 구분
    numeric_cols, categorical_cols = classify_columns(df)

    st.subheader("변수 구분")
    col3, col4 = st.columns(2)
    with col3:
        st.write(f"숫자형 변수 ({len(numeric_cols)}개)")
        st.write(numeric_cols if numeric_cols else "없음")
    with col4:
        st.write(f"범주형(그 외) 변수 ({len(categorical_cols)}개)")
        st.write(categorical_cols if categorical_cols else "없음")

    # 5) 데이터 미리보기
    st.subheader("데이터 미리보기 (상위 10행)")
    st.dataframe(df.head(10), use_container_width=True)

    # 표본 수 관련 주의 문구 (원칙 9: 표본 수가 적으면 주의사항 표시)
    if n_rows < 30:
        st.warning(
            "현재 데이터의 행(표본) 수가 적습니다. "
            "이후 상관분석이나 그룹 비교 결과를 해석할 때 주의가 필요합니다."
        )
