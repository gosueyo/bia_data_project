"""
BIA/BIS 관련 선행연구 10편의 핵심 정보를 정리한 참고 데이터.

이 파일은 '문헌 기반 분석 후보' 화면(literature_reference.py)에서 사용된다.
여기 적힌 cutoff, OR, HR 등은 해당 논문 내에서 도출된 값이며,
회사 데이터의 진단 기준으로 사용하지 않는다.

각 항목의 '매칭_키워드'는 실제 업로드된 데이터의 컬럼명과
대략적으로 비교(부분 문자열 포함 여부)하기 위한 용도이며,
정확한 매칭을 보장하지 않는다. 최종 판단은 사용자가 직접 확인해야 한다.
"""

PAPERS = [
    {
        "번호": 1,
        "분류": "당뇨병",
        "제목": "Independent Association of Phase Angle with Fasting Blood Glucose and Hemoglobin A1c in Korean Type 2 Diabetes Patients",
        "doi": "10.7762/cnr.2020.9.3.205",
        "분석_유형": "상관/회귀 분석",
        "문헌_결과_요약": (
            "50kHz Phase Angle(PhA)이 공복혈당(FPG), HbA1c와 독립적으로 연관되어 있었다는 것이 "
            "이 문헌에서 보고된 결과입니다."
        ),
        "문헌_사용_변수": ["Phase Angle(PhA)", "BCM", "ECM", "Lean mass", "ICW", "ECW", "TBW"],
        "매칭_키워드": ["phase angle", "pha", "bcm", "ecm", "lean", "icw", "ecw", "tbw", "체지방률", "골격근"],
        "추가_필요_데이터": ["공복혈당(FPG)", "HbA1c", "당뇨병 여부/유형"],
        "주의사항": None,
    },
    {
        "번호": 2,
        "분류": "당뇨병",
        "제목": "Analysis of body composition characteristics in patients with type 1 diabetes mellitus: a case–control study",
        "doi": "10.3389/fmed.2026.1776074",
        "분석_유형": "Case-control 그룹 비교",
        "문헌_결과_요약": (
            "제1형 당뇨병군에서 대조군 대비 체지방/내장지방 관련 지표가 낮고 일부 근육 지표가 높은 경향이 "
            "성별에 따라 다르게 관찰되었다는 것이 이 문헌에서 보고된 결과입니다."
        ),
        "문헌_사용_변수": ["Body fat", "Body fat %", "Skeletal muscle/SMI", "ICW", "FFM", "VAT"],
        "매칭_키워드": ["bmi", "체지방", "fat", "골격근", "smi", "내장지방", "visceral", "icw", "ffm"],
        "추가_필요_데이터": ["당뇨병 여부/유형", "성별", "연령(가능하면)"],
        "주의사항": None,
    },
    {
        "번호": 3,
        "분류": "림프부종",
        "제목": "Reference values of bioelectrical impedance analysis for detecting breast cancer-related lymphedema",
        "doi": "10.1097/MD.0000000000012945",
        "분석_유형": "ROC 분석 (그룹 구분)",
        "문헌_결과_요약": (
            "환측/건측 ECF ratio 등을 이용해 유방암 관련 림프부종(BCRL)을 구분하는 ROC 분석을 수행했다는 "
            "것이 이 문헌에서 보고된 내용입니다."
        ),
        "문헌_사용_변수": ["ECF ratio", "Segmental impedance", "1kHz/5kHz resistance ratio"],
        "매칭_키워드": ["ecw", "impedance", "ratio", "resistance"],
        "추가_필요_데이터": ["림프부종 여부", "환측/건측 정보"],
        "주의사항": "이 문헌의 cutoff(ECF ratio 1.010)는 해당 연구 내에서 도출된 값이며, 회사 데이터의 진단 기준으로 사용하지 않습니다.",
    },
    {
        "번호": 4,
        "분류": "림프부종",
        "제목": "Screening for Breast Cancer-Related Lymphedema Development Using Extracellular Water Ratio",
        "doi": "10.1089/lrb.2022.0060",
        "분석_유형": "ROC 분석 (그룹 구분)",
        "문헌_결과_요약": (
            "환측 팔의 %ECW가 건측 및 대조군보다 높게 나타났으며, ROC 분석에서 AUC 0.982가 보고되었다는 것이 "
            "이 문헌에서 보고된 내용입니다."
        ),
        "문헌_사용_변수": ["Upper-extremity %ECW", "ECW/TBW"],
        "매칭_키워드": ["ecw", "tbw", "ratio"],
        "추가_필요_데이터": ["림프부종 여부", "환측/건측 정보"],
        "주의사항": "이 문헌의 cutoff(%ECW 38.5%)는 해당 연구 내에서 도출된 값이며, 회사 데이터의 진단 기준으로 사용하지 않습니다.",
    },
    {
        "번호": 5,
        "분류": "시니어/근감소증",
        "제목": "Longitudinal study on ECW distribution changes and muscle mass in severe sarcopenia patients (BIA + Phase Angle)",
        "doi": "10.1007/s41999-025-01383-w",
        "분석_유형": "종단 연구 / 변화량(Δ) 분석",
        "문헌_결과_요약": (
            "12개월 추적 관찰에서 PhA 감소와 ECW/TBW 변화가 근육량 감소와 함께 관찰되었으며, "
            "BIA 변화가 근육량 감소보다 먼저 나타날 가능성이 제시되었다는 것이 이 문헌에서 보고된 내용입니다."
        ),
        "문헌_사용_변수": ["Skeletal muscle mass", "ECW", "ECW/TBW", "Phase Angle"],
        "매칭_키워드": ["phase angle", "pha", "ecw", "tbw", "골격근", "muscle"],
        "추가_필요_데이터": ["동일 대상자 반복 측정값", "측정 날짜", "측정 간격", "근감소증/기능 관련 임상정보"],
        "주의사항": None,
    },
    {
        "번호": 6,
        "분류": "시니어/쇠약",
        "제목": "Total Body Water and Intracellular Water Relationships with Muscle Strength, Frailty and Functional Performance in an Elderly Population",
        "doi": "10.1007/s12603-018-1129-y",
        "분석_유형": "상관/회귀 분석",
        "문헌_결과_요약": (
            "ICW가 높을수록 근력과 기능적 수행능력이 좋은 경향이 있었으며 쇠약과의 관계도 분석되었다는 것이 "
            "이 문헌에서 보고된 내용입니다."
        ),
        "문헌_사용_변수": ["TBW", "ICW", "Fat mass", "Lean mass", "Muscle mass"],
        "매칭_키워드": ["tbw", "icw", "ecw", "골격근", "fat", "lean", "muscle"],
        "추가_필요_데이터": ["악력", "보행속도", "ADL 또는 기능평가", "Frailty 여부"],
        "주의사항": "이 문헌은 'ICW/TBW 50% 미만' 같은 진단 cutoff를 제시한 것이 아닙니다. 임의의 50% 기준을 이 논문 결과로 사용하지 않습니다.",
    },
    {
        "번호": 7,
        "분류": "신부전/혈액투석",
        "제목": "Greater fluid overload and lower interdialytic weight gain are independently associated with mortality in a large international hemodialysis population",
        "doi": "10.1093/ndt/gfy083",
        "분석_유형": "생존분석 (Hazard Ratio)",
        "문헌_결과_요약": (
            "체액 과다(Fluid Overload)와 낮은 투석간 체중증가(IDWG)의 조합이 사망 위험과 관련되는 패턴을 보였다는 "
            "것이 이 문헌에서 보고된 내용입니다."
        ),
        "문헌_사용_변수": ["Fluid Overload(FO)", "체수분 지표", "투석 전후 체중", "IDWG"],
        "매칭_키워드": ["ecw", "tbw", "체중", "weight"],
        "추가_필요_데이터": ["투석 여부", "투석 전/후 체중", "IDWG", "사망/추적 결과", "투석 기간"],
        "주의사항": None,
    },
    {
        "번호": 8,
        "분류": "신부전/혈액투석",
        "제목": "Monitoring Volume Status Using Bioelectrical Impedance Analysis in Chronic Hemodialysis Patients",
        "doi": "10.1097/MAT.0000000000000619",
        "분석_유형": "반복 측정 / 생존분석",
        "문헌_결과_요약": (
            "ECW/TBW가 지속적으로 높은 상태인 환자군과 임상 outcome의 관계를 분석했다는 것이 "
            "이 문헌에서 보고된 내용입니다."
        ),
        "문헌_사용_변수": ["ECW/TBW", "체수분 지표"],
        "매칭_키워드": ["ecw", "tbw", "체중"],
        "추가_필요_데이터": ["동일 환자 반복 측정", "측정 날짜", "투석 여부", "임상 outcome"],
        "주의사항": "이 문헌의 ECW/TBW 0.40 기준은 해당 연구 조건에서 사용된 값이며, 일반적인 질병 cutoff로 사용하지 않습니다.",
    },
    {
        "번호": 9,
        "분류": "임산부",
        "제목": "Longitudinal changes and correlations of bioimpedance and anthropometric measurements in pregnancy",
        "doi": "10.1080/14767058.2016.1265929",
        "분석_유형": "종단 연구 / 그룹 비교",
        "문헌_결과_요약": (
            "정상 임신에서는 임신 진행에 따라 TBW, ECW, FFM, FM이 변화했고, 임신성 고혈압/전자간증 및 SGA "
            "그룹에서는 다른 변화 패턴이 관찰되었다는 것이 이 문헌에서 보고된 내용입니다."
        ),
        "문헌_사용_변수": ["TBW", "ECW", "FFM", "FM"],
        "매칭_키워드": ["tbw", "ecw", "ffm", "fm", "체지방", "체중"],
        "추가_필요_데이터": ["임신 주수", "반복 측정 날짜", "임신성 고혈압/HDP 여부", "SGA 여부"],
        "주의사항": None,
    },
    {
        "번호": 10,
        "분류": "임산부",
        "제목": "Measuring maternal body composition by biomedical impedance can predict risk for gestational diabetes mellitus",
        "doi": "10.1080/14767058.2020.1797666",
        "분석_유형": "Logistic Regression (Odds Ratio)",
        "문헌_결과_요약": (
            "임신 초기 체지방/내장지방 관련 지표가 이후 임신성 당뇨(GDM) 발생과 독립적으로 연관되어 있었다는 것이 "
            "이 문헌에서 보고된 내용입니다."
        ),
        "문헌_사용_변수": ["Body fat %", "Visceral fat", "BMI", "Bone mineral mass"],
        "매칭_키워드": ["체지방", "fat", "visceral", "내장지방", "bmi", "골격근"],
        "추가_필요_데이터": ["임신 주수", "GDM 여부", "OGTT 결과 또는 혈당 관련 데이터"],
        "주의사항": "이 문헌에서 사용한 cutoff/OR을 회사 데이터에 그대로 적용하지 않습니다.",
    },
]
