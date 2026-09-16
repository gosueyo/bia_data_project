"""
4단계: 문헌 기반 분석 후보 화면

기능:
- 선행연구 10편의 핵심 정보(변수, 분석 유형, 문헌 결과, 필요한 추가 데이터, 주의사항)를 안내
- 데이터가 업로드되어 있으면, 논문에서 사용된 변수 키워드와
  실제 업로드된 컬럼명을 대략적으로 비교하여 참고 정보로 표시
- 이 화면은 실제 분석을 수행하지 않으며, "이런 분석을 문헌에서 확인했고
  우리 데이터에 이런 변수가 있는 것 같다"는 참고 정보만 제공한다.
"""

import streamlit as st

from utils.literature_map import PAPERS


def render():
    st.header("7. 문헌 기반 분석 후보")

    st.write(
        """
        아래 내용은 BIA/BIS 관련 선행연구 10편에서 확인한 분석 방법을 정리한 것입니다.
        문헌에서 보고된 결과와, 우리 데이터에서 탐색해볼 수 있는 아이디어를 구분해서 표시합니다.

        - 문헌에서 사용된 cutoff/OR/HR 등은 해당 연구 내에서 도출된 값이며, 회사 데이터의 진단 기준으로 사용하지 않습니다.
        - 아래 '매칭된 컬럼'은 컬럼명을 단순 비교한 참고 정보이며, 실제 분석 가능 여부를 보장하지 않습니다.
        """
    )

    df = st.session_state.get("df")

    if df is None:
        st.info(
            "데이터를 업로드하면, 각 문헌에서 사용된 변수와 현재 데이터의 컬럼명을 "
            "간단히 비교해서 보여드립니다. (지금은 문헌 목록만 표시됩니다.)"
        )

    # 분류별 필터
    categories = ["전체"] + sorted({p["분류"] for p in PAPERS})
    selected_category = st.selectbox("질환/분류 필터", categories)

    filtered_papers = [p for p in PAPERS if selected_category == "전체" or p["분류"] == selected_category]

    for paper in filtered_papers:
        title_line = f"[논문 {paper['번호']}] {paper['분류']} — {paper['제목']}"
        with st.expander(title_line):
            st.caption(f"DOI: {paper['doi']}")
            st.write(f"**분석 유형 (문헌에서 실제 수행한 분석):** {paper['분석_유형']}")
            st.write(f"**문헌에서 보고된 결과:** {paper['문헌_결과_요약']}")
            st.write(f"**문헌에서 사용된 변수:** {', '.join(paper['문헌_사용_변수'])}")

            if df is not None:
                matched_cols = _find_matching_columns(df.columns, paper["매칭_키워드"])
                if matched_cols:
                    st.write(f"**현재 데이터에서 매칭된 컬럼(참고용):** {', '.join(matched_cols)}")
                    st.caption("실제로 이 컬럼들이 문헌의 변수와 같은 의미인지는 반드시 직접 확인해주세요.")
                else:
                    st.write("**현재 데이터에서 매칭된 컬럼:** 없음")

            st.write(f"**분석을 확장하려면 추가로 필요한 데이터:** {', '.join(paper['추가_필요_데이터'])}")

            if paper["주의사항"]:
                st.warning(paper["주의사항"])

    st.caption(
        "이 화면은 문헌 조사 내용을 정리한 참고 자료이며, 이 화면 자체가 "
        "통계 분석이나 진단을 수행하지는 않습니다."
    )


def _find_matching_columns(df_columns, keywords):
    """
    데이터의 컬럼명과 문헌 변수 키워드를 대략적으로(부분 문자열 포함 여부) 비교한다.
    공백, 언더스코어(_), 하이픈(-), 슬래시(/)는 무시하고 소문자로 변환하여 비교한다.
    """
    matched = []
    for col in df_columns:
        col_norm = _normalize(col)
        for keyword in keywords:
            keyword_norm = _normalize(keyword)
            if keyword_norm and keyword_norm in col_norm:
                matched.append(col)
                break
    return matched


def _normalize(text: str) -> str:
    """비교를 위해 소문자로 바꾸고 공백/구분기호를 제거한다."""
    text = str(text).lower()
    for ch in [" ", "_", "-", "/"]:
        text = text.replace(ch, "")
    return text
