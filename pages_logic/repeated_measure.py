"""
3단계: 반복측정 분석 (구조 확인 전용)

이번 단계에서 구현하는 것:
- ID(대상자 식별) 컬럼과 측정일/측정차수 컬럼이 존재하는지 확인
- 존재하면, 동일 대상자가 2회 이상 측정되었는지 확인하여
  반복측정 분석이 가능한 구조인지 안내
- 존재하지 않거나 반복 측정이 없으면
  "현재 데이터 구조에서는 개인별 변화량 분석을 수행할 수 없습니다." 안내

이번 단계에서 구현하지 않는 것 (다음 단계 예정):
- 실제 Δ(변화량) 계산
- trajectory 시각화
- 반복측정 통계분석
"""

import streamlit as st

from utils.data_utils import detect_id_time_candidates


def render():
    st.header("6. 반복측정 분석 (구조 확인)")

    df = st.session_state.get("df")

    if df is None:
        st.info("먼저 '데이터 업로드' 메뉴에서 파일을 업로드해주세요.")
        return

    st.write(
        "이 화면은 현재 데이터가 '반복측정 분석이 가능한 구조'인지만 확인합니다. "
        "실제 변화량(Δ) 계산이나 시계열 그래프는 다음 단계에서 추가될 예정입니다."
    )

    id_candidates, time_candidates = detect_id_time_candidates(df)

    all_cols = df.columns.tolist()
    id_options = ["(선택 안 함)"] + all_cols
    time_options = ["(선택 안 함)"] + all_cols

    default_id_index = id_options.index(id_candidates[0]) if id_candidates else 0
    default_time_index = time_options.index(time_candidates[0]) if time_candidates else 0

    st.subheader("ID / 측정일(또는 측정차수) 컬럼 확인")

    if id_candidates or time_candidates:
        st.caption(
            f"컬럼명을 기준으로 자동 감지된 후보 — "
            f"ID 후보: {id_candidates if id_candidates else '없음'}, "
            f"측정일/측정차수 후보: {time_candidates if time_candidates else '없음'}"
        )
    else:
        st.caption("컬럼명을 기준으로 자동 감지된 후보가 없습니다. 직접 선택해주세요.")

    col1, col2 = st.columns(2)
    with col1:
        selected_id_col = st.selectbox("ID(대상자 식별) 컬럼", id_options, index=default_id_index)
    with col2:
        selected_time_col = st.selectbox("측정일 또는 측정차수 컬럼", time_options, index=default_time_index)

    # ID 또는 시간 컬럼이 선택되지 않은 경우
    if selected_id_col == "(선택 안 함)" or selected_time_col == "(선택 안 함)":
        st.warning("현재 데이터 구조에서는 개인별 변화량 분석을 수행할 수 없습니다.")
        st.caption("ID와 측정일(또는 측정차수) 컬럼을 모두 선택해야 반복측정 구조를 확인할 수 있습니다.")
        return

    # 동일 ID가 2회 이상 측정되었는지 확인
    id_counts = df[selected_id_col].value_counts()
    n_subjects = id_counts.shape[0]
    n_with_repeats = int((id_counts >= 2).sum())
    max_repeats = int(id_counts.max())
    avg_repeats = round(id_counts.mean(), 2)

    if n_with_repeats == 0:
        st.warning("현재 데이터 구조에서는 개인별 변화량 분석을 수행할 수 없습니다.")
        st.caption(
            f"선택한 '{selected_id_col}' 컬럼 기준으로, 동일 대상자가 2회 이상 측정된 경우가 없습니다 "
            "(모든 대상자가 1회만 측정됨)."
        )
        return

    # 반복측정 구조가 확인된 경우
    st.success("반복측정 분석이 가능한 데이터 구조로 보입니다.")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("전체 대상자 수", n_subjects)
    m2.metric("2회 이상 측정된 대상자 수", n_with_repeats)
    m3.metric("평균 측정 횟수", avg_repeats)
    m4.metric("최대 측정 횟수", max_repeats)

    st.subheader("대상자별 측정 횟수 (상위 10명)")
    preview = id_counts.reset_index()
    preview.columns = [selected_id_col, "측정 횟수"]
    st.dataframe(preview.head(10), use_container_width=True)

    st.info(
        "이번 단계에서는 데이터 구조 확인까지만 제공됩니다. "
        "실제 변화량(Δ) 계산, 개인별/그룹별 trajectory 시각화 등은 다음 단계에서 구현될 예정입니다."
    )
