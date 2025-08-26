import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("📷 QR/바코드 출석 체크 시스템 (Cloud용)")

# 출석 리스트 초기화
if "attendance" not in st.session_state:
    st.session_state.attendance = []

# 카메라 스트리밍 (WebRTC)
webrtc_streamer(
    key="scanner",
    video_transformer_factory=None,  # Python 영상 처리 제거
    media_stream_constraints={"video": True, "audio": False}
)

st.subheader("📋 출석 명단")
st.table(st.session_state.attendance)

st.info(
    "⚠️ QR/바코드 인식은 현재 Streamlit Cloud 환경에서는 Python 대신 "
    "Web 브라우저에서 JS 기반으로 처리해야 합니다.\n"
    "학생들은 각자 핸드폰으로 QR 스캔 → 코드 입력 방식으로 출석 등록 가능합니다."
)

# 예시: 수동 등록 (학생이 QR 내용 입력)
code_input = st.text_input("QR/바코드 코드 입력")
if st.button("출석 등록"):
    if code_input and code_input not in st.session_state.attendance:
        st.session_state.attendance.append(code_input)

