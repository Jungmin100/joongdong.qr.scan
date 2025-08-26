import streamlit as st
import av
import cv2
import pandas as pd
from pyzbar.pyzbar import decode
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title("📷 QR/바코드 출석 확인 시스템 (카메라)")

# 출석 데이터 초기화
if "attendance" not in st.session_state:
    st.session_state.attendance = []

class QRBarcodeScanner(VideoTransformerBase):
    def __init__(self):
        self.last_scanned = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        decoded_objects = decode(img)

        for obj in decoded_objects:
            code_text = obj.data.decode("utf-8")
            code_type = obj.type  # QRCODE, EAN13, CODE128 등
            display_text = f"{code_text} ({code_type})"

            # 코드 영역 표시
            (x, y, w, h) = obj.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(img, display_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (255, 0, 0), 2)

            # 출석 저장 (QR/바코드 중복 방지)
            if display_text not in st.session_state.attendance:
                st.session_state.attendance.append(display_text)
                self.last_scanned = display_text

        return img

# 카메라 실행
webrtc_streamer(
    key="scanner",
    video_transformer_factory=QRBarcodeScanner,
    media_stream_constraints={"video": True, "audio": False}
)

# 최근 스캔 결과 표시
if "attendance" in st.session_state and len(st.session_state.attendance) > 0:
    st.success(f"최근 스캔된 코드: {st.session_state.attendance[-1]}")

# 출석 명단 표시
st.subheader("📋 출석 명단")
df = pd.DataFrame(st.session_state.attendance, columns=["코드 내용 (타입)"])
st.table(df)

# CSV 다운로드
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="출석 명단 CSV 다운로드",
    data=csv,
    file_name="attendance.csv",
    mime="text/csv",
)
