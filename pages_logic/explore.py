"""
1-4단계: 변수 탐색 화면

기능:
- 업로드된 데이터가 없으면 안내 메시지만 표시
- 숫자형 변수 중 하나를 선택
- 기술통계(개수/평균/중앙값/표준편차/최소/최대) 표시
- Histogram, Boxplot 표시 (Plotly)
"""

import plotly.express as px
import streamlit as st

from utils.data_utils import classify_columns, get_descriptive_stats


def render():
    st.header("3. 변수 탐색")

    df = st.session_state.get("df")

    if df is None:
        st.info("먼저 '데이터 업로드' 메뉴에서 파일을 업로드해주세요.")
        return

    numeric_cols, _ = classify_columns(df)

    if not numeric_cols:
        st.warning("현재 데이터에 숫자형 변수가 없어 변수 탐색을 진행할 수 없습니다.")
        return

    selected_col = st.selectbox("탐색할 숫자형 변수를 선택하세요", numeric_cols)

    # 결측치 안내
    n_missing = df[selected_col].isnull().sum()
    if n_missing > 0:
        st.caption(f"'{selected_col}' 변수에는 결측치 {n_missing}개가 있습니다. 통계 계산 시 자동으로 제외됩니다.")

    # 기술통계 표
    st.subheader("기술통계")
    stats_df = get_descriptive_stats(df, selected_col)
    st.dataframe(stats_df, use_container_width=True)

    # 분포 시각화 (결측치는 제외하고 그림)
    plot_data = df[[selected_col]].dropna()

    if plot_data.empty:
        st.warning("유효한 값이 없어 그래프를 표시할 수 없습니다.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("분포 (Histogram)")
        fig_hist = px.histogram(plot_data, x=selected_col)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.subheader("분포 (Boxplot)")
        fig_box = px.box(plot_data, y=selected_col, points="all")
        st.plotly_chart(fig_box, use_container_width=True)

    st.caption("위 결과는 탐색적 분석 결과이며, 정상/비정상 여부를 판정하는 기준이 아닙니다.")
