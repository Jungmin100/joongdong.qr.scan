import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from pyzbar.pyzbar import decode
from PIL import Image

st.title("📷 QR/바코드 출석 확인 시스템 (Cloud용)")

if "attendance" not in st.session_state:
    st.session_state.attendance = []

class QRBarcodeScanner(VideoTransformerBase):
    def __init__(self):
        self.last_scanned = None

    def transform(self, frame):
        # 카메라 프레임을 PIL 이미지로 변환
        img = frame.to_ndarray(format="rgb24")
        pil_img = Image.fromarray(img)

        # QR/바코드 인식
        decoded_objects = decode(pil_img)
        for obj in decoded_objects:
            code_text = obj.data.decode("utf-8")
            code_type = obj.type
            display_text = f"{code_text} ({code_type})"

            # 중복 방지하고 출석 저장
            if display_text not in st.session_state.attendance:
                st.session_state.attendance.append(display_text)
                self.last_scanned = display_text

        return img  # OpenCV 대신 numpy array 그대로 반환

webrtc_streamer(
    key="scanner",
    video_transformer_factory=QRBarcodeScanner,
    media_stream_constraints={"video": True, "audio": False}
)

if st.session_state.attendance:
    st.subheader("최근 스캔된 코드")
    st.write(st.session_state.attendance[-1])

st.subheader("📋 출석 명단")
st.table(st.session_state.attendance)

