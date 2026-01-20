import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        .block-container {
            padding-top: 3rem !important; 
            padding-bottom: 1rem !important;
        }
        h1 {
            margin-top: 0rem !important;
            padding-top: 0rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* 메인 화면의 큰 버튼 (기존 60px 유지) */
        div.stButton > button {
            height: 60px !important; 
            font-size: 20px !important;
            font-weight: bold !important;
            width: 100%;
            border-radius: 8px;
        }

        /* [요청 1] 사이드바 내의 단원 선택 버튼만 크기를 절반(30px)으로 줄임 */
        [data-testid="stSidebar"] div.stButton > button {
            height: 30px !important;
            font-size: 14px !important;
            padding: 0px 5px !important;
            margin-bottom: 2px !important;
            font-weight: normal !important; /* 사이드바는 가독성을 위해 굵기 조절 */
        }

        /* [요청 2] 현재 선택된 단원(Primary) 강조 스타일 */
        [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
            background-color: #2E7D32 !important; /* 강조색: 진한 초록 */
            color: white !important;
            border: none !important;
            font-weight: bold !important;
        }

        .calc-display {
            background-color: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 0 15px;
            margin-bottom: 15px;
            text-align: right;
            font-family: 'Courier New', monospace;
            font-size: 28px;
            font-weight: bold;
            color: #333;
            letter-spacing: 2px;
            min-height: 75px; 
            display: flex;
            align-items: center;
            justify-content: flex-end;
        }
        .feedback-box {
            border: 2px solid #e9ecef;
            border-radius: 8px;
            background-color: #ffffff;
            padding: 10px;
            margin-top: 15px; 
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #6c757d;
        }
        .status-success { color: #2E7D32 !important; }
        .status-error { color: #d32f2f !important; }
        </style>
    """, unsafe_allow_html=True)