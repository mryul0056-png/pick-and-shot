import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. 필수 설정 (미스터율 개발자님 입력 구역) ---
GOOGLE_CLIENT_ID = "276368848990-p5ugb0b51n3dnbitr2fthf9e3h1g4309.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GEMINI_API_KEY = "이곳에_발급받은_GEMINI_API_키_입력"

# Gemini AI 설정
genai.configure(api_key=AIzaSyD_irYy-P1drkmy9gaPYd9aLa88yNtPN0U)
model = genai.GenerativeModel('gemini-1.5-flash')

# 페이지 설정
st.set_page_config(page_title="Pick & Shot - 픽앤샷", page_icon="📸", layout="centered")

# --- 2. 프로그램 로직 ---

# 세션 상태 초기화 (로그인 여부 및 데이터 저장)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 3. UI 화면 구성 ---

st.title("📸 픽앤샷 (Pick & Shot)")
st.caption("천재 AI 감독이 제안하는 숏폼 촬영 지시서")

# [A] 로그인 전 화면
if not st.session_state.logged_in:
    st.image("https://images.unsplash.com/photo-1492691523567-61723c295dbd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80")
    st.write("### 사장님, 사진 한 장만 주세요. 떡상 시나리오는 제가 짭니다.")
    st.info("💡 지금 구글 로그인하면 5회 무료 체험 가능!")
    
    if st.button("구글 계정으로 3초 만에 시작하기"):
        # 실제 운영 시에는 OAuth 연동이 되나, 현재 로컬 테스트를 위해 로그인 성공으로 처리합니다.
        st.session_state.logged_in = True
        st.rerun()

# [B] 로그인 후 메인 기능 화면
else:
    with st.sidebar:
        st.success("로그인 성공!")
        st.write("멤버십: **무통장 입금 대기 중**")
        st.write("---")
        st.write("💰 **구독 안내**")
        st.write("월 19,900원으로 무제한 이용")
        st.write("입금계좌: 신한은행 110-xxx-xxxxxx (미스터율)")
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.rerun()

    st.write("### 📤 상품/매장 사진을 업로드하세요")
    uploaded_file = st.file_uploader("사진을 올리면 즉시 촬영 가이드가 나옵니다.", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="분석할 사진", use_container_width=True)
        
        if st.button("🚀 10만 조회수 촬영 지시서 생성"):
            with st.spinner("AI 감독님이 사진을 분석하여 전략을 짜고 있습니다..."):
                try:
                    # [핵심] Gemini에게 내리는 전문가 페르소나 주입 프롬프트
                    prompt = """
                    너는 보스턴 컨설팅 그룹 출신의 마케팅 전략가이자, 100만 팔로워를 보유한 숏폼(릴스, 쇼츠, 틱톡) 전문 촬영 감독이야.
                    제공된 사진을 분석해서 소상공인이 '돈을 벌 수 있는' 구체적인 촬영 지시서를 작성해줘.

                    답변은 반드시 다음 구조로 한국어로 작성해:
                    1. 상품의 핵심 가치(USP) 분석: 사진 속 상품이 왜 매력적인지 1문장 요약.
                    2. 15초 숏폼 시나리오:
                       - 0~3초(후킹): 시선을 끌 수 있는 강렬한 첫 장면과 카메라 움직임.
                       - 3~10초(본문): 상품의 디테일을 보여주는 연출법.
                       - 10~15초(결론): 구매를 유도하는 마무리 샷.
                    3. 추천 문구: 영상 위에 적을 자막 (당근마켓용 / 인스타용 구분).
                    4. 촬영 꿀팁: 이 상품을 찍을 때 가장 중요한 조명이나 각도 조언.

                    전문적이지만 사장님들이 이해하기 쉽게 친절하게 설명해줘.
                    """
                    
                    # Gemini에게 이미지와 프롬프트 전달
                    response = model.generate_content([prompt, image])
                    
                    st.divider()
                    st.write("### 🎬 AI 감독님의 촬영 지시서")
                    st.write(response.text)
                    st.balloons() # 축하 효과
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

# --- 4. 자동 안전 레이어 및 공지 ---
st.write("---")
st.caption("주의: 본 가이드는 AI의 분석 결과이며, 실제 촬영 시 안전과 주변 환경을 고려해 주세요.")
