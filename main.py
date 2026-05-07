import streamlit as st
import anthropic

# ─────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Claude AI 챗봇",
    page_icon="✨",
    layout="centered",
)

# ─────────────────────────────────────────
# CSS 커스텀 스타일
# ─────────────────────────────────────────
st.markdown("""
<style>
    /* 구글 폰트 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 메인 컨테이너 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 780px;
    }

    /* 헤더 타이틀 */
    .main-title {
        text-align: center;
        padding: 2.5rem 1rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -1px;
        margin-bottom: 0;
    }

    .main-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.95rem;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
    }

    /* 모델 선택 카드 */
    .model-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }

    .model-card-title {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    /* 사용량 카드 */
    .usage-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }

    .usage-label {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.72rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }

    .usage-value {
        color: #a78bfa;
        font-size: 1.4rem;
        font-weight: 700;
    }

    .usage-total {
        color: rgba(255, 255, 255, 0.35);
        font-size: 0.78rem;
        margin-top: 0.8rem;
        text-align: right;
    }

    /* 채팅 메시지 - 사용자 */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2)) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 18px 18px 4px 18px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(10px) !important;
    }

    /* 채팅 메시지 - AI */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px 18px 18px 4px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(10px) !important;
    }

    /* 채팅 입력창 */
    .stChatInput textarea {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        color: white !important;
        font-family: 'Noto Sans KR', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.9rem 1.2rem !important;
        backdrop-filter: blur(10px) !important;
        transition: border 0.2s ease !important;
    }

    .stChatInput textarea:focus {
        border: 1px solid rgba(102, 126, 234, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
    }

    /* 셀렉트박스 */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* 슬라이더 */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }

    /* 버튼 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-family: 'Noto Sans KR', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        opacity: 0.85 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35) !important;
    }

    /* expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        color: rgba(255, 255, 255, 0.5) !important;
        font-size: 0.82rem !important;
    }

    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.85) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(20px) !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
    }

    /* 사이드바 텍스트 */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p {
        color: rgba(255, 255, 255, 0.7) !important;
    }

    /* metric */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 0.8rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.5) !important;
        font-size: 0.75rem !important;
    }

    [data-testid="stMetricValue"] {
        color: #a78bfa !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }

    /* 구분선 */
    hr {
        border: none !important;
        border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin: 1.5rem 0 !important;
    }

    /* 스크롤바 */
    ::-webkit-scrollbar {
        width: 5px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.4);
        border-radius: 10px;
    }

    /* 에러/경고 메시지 */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }

    /* 텍스트 색상 전체 */
    .stMarkdown, .stText, p, li, span {
        color: rgba(255, 255, 255, 0.85);
    }

    /* 배지 스타일 */
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(102,126,234,0.25), rgba(118,75,162,0.25));
        border: 1px solid rgba(102,126,234,0.4);
        color: #a78bfa;
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.2rem;
    }

    /* 웰컴 박스 */
    .welcome-box {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }

    .welcome-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .welcome-text {
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
        line-height: 1.8;
    }

    /* 사이드바 섹션 헤더 */
    .sidebar-section {
        color: rgba(255,255,255,0.35);
        font-size: 0.7rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 1.2rem 0 0.6rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# API 키 불러오기
# ─────────────────────────────────────────
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except KeyError:
    st.error("❌ API 키가 설정되지 않았습니다. Streamlit Cloud의 Secrets에 ANTHROPIC_API_KEY를 등록해주세요.")
    st.stop()


# ─────────────────────────────────────────
# 세션 상태 초기화
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "usage_history" not in st.session_state:
    st.session_state.usage_history = []
if "total_input_tokens" not in st.session_state:
    st.session_state.total_input_tokens = 0
if "total_output_tokens" not in st.session_state:
    st.session_state.total_output_tokens = 0
if "total_requests" not in st.session_state:
    st.session_state.total_requests = 0


# ─────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────
with st.sidebar:
    # 로고 영역
    st.markdown("""
        <div style='text-align:center; padding: 1rem 0 1.5rem;'>
            <div style='font-size:2.5rem; margin-bottom:0.4rem;'>✨</div>
            <div style='font-size:1.1rem; font-weight:700;
                        background: linear-gradient(135deg, #667eea, #f093fb);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                        background-clip: text;'>
                Claude AI
            </div>
            <div style='color:rgba(255,255,255,0.3); font-size:0.75rem; margin-top:0.2rem;'>
                Powered by Anthropic
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 모델 선택
    st.markdown('<div class="sidebar-section">🧠 모델 선택</div>', unsafe_allow_html=True)
    model_option = st.selectbox(
        label="model",
        options=["claude-sonnet-4-5", "claude-opus-4-5"],
        format_func=lambda x: {
            "claude-sonnet-4-5": "⚡ Sonnet 4.5  — 빠르고 효율적",
            "claude-opus-4-5":   "🏆 Opus 4.5   — 가장 강력함",
        }[x],
        label_visibility="collapsed",
    )

    # 모델 설명 배지
    if model_option == "claude-sonnet-4-5":
        st.markdown("""
            <div style='margin-top:0.5rem;'>
                <span class='badge'>⚡ 빠른 응답</span>
                <span class='badge'>💰 경제적</span>
                <span class='badge'>📝 일상 작업</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='margin-top:0.5rem;'>
                <span class='badge'>🧠 최고 성능</span>
                <span class='badge'>🔬 복잡한 분석</span>
                <span class='badge'>✍️ 창의적 작업</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 토큰 슬라이더
    st.markdown('<div class="sidebar-section">📏 응답 길이</div>', unsafe_allow_html=True)
    max_tokens = st.slider(
        label="tokens",
        min_value=256,
        max_value=4096,
        value=1024,
        step=256,
        label_visibility="collapsed",
        help="값이 클수록 더 긴 답변을 받을 수 있습니다."
    )
    st.markdown(
        f"<div style='text-align:right; color:rgba(255,255,255,0.35); font-size:0.78rem; margin-top:-0.5rem;'>"
        f"최대 <b style='color:#a78bfa;'>{max_tokens:,}</b> 토큰</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 누적 사용량
    st.markdown('<div class="sidebar-section">📊 세션 사용량</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📥 입력", f"{st.session_state.total_input_tokens:,}")
        st.metric("🔢 요청", f"{st.session_state.total_requests:,}")
    with col2:
        st.metric("📤 출력", f"{st.session_state.total_output_tokens:,}")
        total = st.session_state.total_input_tokens + st.session_state.total_output_tokens
        st.metric("🔤 합계", f"{total:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 초기화 버튼들
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️ 대화 초기화", use_container_width=True):
            st.session_state.messages = []
            st.session_state.usage_history = []
            st.rerun()
    with col_b:
        if st.button("📊 사용량 초기화", use_container_width=True):
            st.session_state.total_input_tokens = 0
            st.session_state.total_output_tokens = 0
            st.session_state.total_requests = 0
            st.rerun()


# ─────────────────────────────────────────
# 메인 영역 - 헤더
# ─────────────────────────────────────────
st.markdown('<h1 class="main-title">✨ Claude AI 챗봇</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="main-subtitle">Anthropic의 최신 AI 모델과 대화해보세요</p>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────────
# 현재 선택 모델 표시
# ─────────────────────────────────────────
model_display = {
    "claude-sonnet-4-5": ("⚡", "Claude Sonnet 4.5", "#667eea"),
    "claude-opus-4-5":   ("🏆", "Claude Opus 4.5",   "#f093fb"),
}
icon, name, color = model_display[model_option]
st.markdown(f"""
    <div style='
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    '>
        <div style='
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 30px;
            padding: 0.4rem 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        '>
            <span>{icon}</span>
            <span style='color: {color}; font-size: 0.85rem; font-weight: 600;'>{name}</span>
            <span style='
                background: rgba(255,255,255,0.1);
                color: rgba(255,255,255,0.4);
                font-size: 0.7rem;
                padding: 0.1rem 0.5rem;
                border-radius: 10px;
                margin-left: 0.3rem;
            '>활성화됨</span>
        </div>
    </div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 웰컴 메시지 (대화 없을 때)
# ─────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-box">
            <div class="welcome-icon">💬</div>
            <div style='color:rgba(255,255,255,0.8); font-size:1.05rem; font-weight:600; margin-bottom:0.7rem;'>
                무엇이든 물어보세요!
            </div>
            <div class="welcome-text">
                코딩 · 글쓰기 · 번역 · 분석 · 요약<br>
                어떤 주제든 도움을 드릴 수 있어요 ✨
            </div>
            <div style='margin-top:1.2rem; display:flex; gap:0.5rem; justify-content:center; flex-wrap:wrap;'>
                <span class='badge'>💡 아이디어 제안</span>
                <span class='badge'>🔍 정보 검색</span>
                <span class='badge'>📝 문서 작성</span>
                <span class='badge'>🐍 코드 작성</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# 대화 기록 출력
# ─────────────────────────────────────────
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # AI 메시지 아래 토큰 사용량
        if message["role"] == "assistant":
            usage_index = sum(1 for m in st.session_state.messages[:i+1] if m["role"] == "assistant") - 1
            if usage_index < len(st.session_state.usage_history):
                usage = st.session_state.usage_history[usage_index]
                with st.expander("📊 토큰 사용량 보기"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("📥 입력", f"{usage['input_tokens']:,}")
                    c2.metric("📤 출력", f"{usage['output_tokens']:,}")
                    c3.metric("🔤 합계", f"{usage['input_tokens'] + usage['output_tokens']:,}")
                    st.markdown(
                        f"<div style='color:rgba(255,255,255,0.3); font-size:0.78rem; margin-top:0.3rem;'>"
                        f"🧠 모델: <code style='color:#a78bfa;'>{usage['model']}</code></div>",
                        unsafe_allow_html=True
                    )


# ─────────────────────────────────────────
# 채팅 입력
# ─────────────────────────────────────────
if user_input := st.chat_input("메시지를 입력하세요..."):

    # 사용자 메시지
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답
    with st.chat_message("assistant"):
        with st.spinner(""):
            st.markdown("""
                <div style='color:rgba(255,255,255,0.4); font-size:0.85rem; padding:0.3rem 0;'>
                    ✨ Claude가 생각하는 중...
                </div>
            """, unsafe_allow_html=True)
            try:
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model=model_option,
                    max_tokens=max_tokens,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                )

                answer       = response.content[0].text
                input_tokens = response.usage.input_tokens
                output_tokens= response.usage.output_tokens

                st.markdown(answer)

                with st.expander("📊 토큰 사용량 보기"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("📥 입력", f"{input_tokens:,}")
                    c2.metric("📤 출력", f"{output_tokens:,}")
                    c3.metric("🔤 합계", f"{input_tokens + output_tokens:,}")
                    st.markdown(
                        f"<div style='color:rgba(255,255,255,0.3); font-size:0.78rem; margin-top:0.3rem;'>"
                        f"🧠 모델: <code style='color:#a78bfa;'>{model_option}</code></div>",
                        unsafe_allow_html=True
                    )

                # 세션 업데이트
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.session_state.usage_history.append({
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "model": model_option,
                })
                st.session_state.total_input_tokens  += input_tokens
                st.session_state.total_output_tokens += output_tokens
                st.session_state.total_requests      += 1

            except anthropic.AuthenticationError:
                st.error("❌ API 키가 올바르지 않습니다. Secrets 설정을 확인해주세요.")
            except anthropic.RateLimitError:
                st.error("⚠️ API 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
            except anthropic.APIError as e:
                st.error(f"🚨 API 오류가 발생했습니다: {e}")
