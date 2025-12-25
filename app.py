import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. 보안 설정 ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    # 모델 이름을 'models/gemini-1.5-flash'로 더 명확히 지정합니다.
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception:
    st.error("⚠️ 설정에서 API 키를 입력해주세요! (Settings > Secrets)")

st.set_page_config(page_title="Pick & Shot - 픽앤샷", page_icon="📸")
st.title("📸 픽앤샷 (Pick & Shot)")

# --- 2. 메인 로직 ---
uploaded_file = st.file_uploader("상품 사진을 올려주세요", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="분석 준비 완료!", use_container_width=True)
    
    if st.button("🚀 숏폼 촬영 지시서 생성"):
        with st.spinner("AI 감독님이 전략을 짜는 중..."):
            try:
                # 지시문(Prompt)을 더 구체적으로 보강했습니다.
                prompt = "너는 숏폼 전문 감독이야. 이 사진의 상품을 분석해서 대박 나게 할 15초 촬영 구도와 자막을 짜줘."
                response = model.generate_content([prompt, image])
                st.write(response.text)
                st.balloons() # 성공 시 풍선 효과!
            except Exception as e:
                # 에러 메시지를 더 자세히 보여주도록 수정했습니다.
                st.error(f"분석 중 오류 발생: {e}")
