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
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        font-family: 'Noto Sans KR', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 780px;
    }

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

    .stChatInput textarea {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        color: white !important;
        font-family: 'Noto Sans KR', sans-serif !important;
        font-size: 0.95rem !important;
    }

    .stChatInput textarea:focus {
        border: 1px solid rgba(102, 126, 234, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
    }

    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
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

    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.85) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(20px) !important;
    }

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

    hr {
        border: none !important;
        border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin: 1.5rem 0 !important;
    }

    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.4);
        border-radius: 10px;
    }

    .stMarkdown, .stText, p, li, span {
        color: rgba(255, 255, 255, 0.85);
    }

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

    .welcome-box {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }

    .welcome-text {
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
        line-height: 1.8;
    }

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
# ✅ API 키 불러오기 + 정제 (핵심 수정!)
# ─────────────────────────────────────────
def clean_api_key(key: str) -> str:
    """API 키에서 공백, 줄바꿈, 비ASCII 문자를 모두 제거"""
    key = key.strip()                          # 앞뒤 공백/줄바꿈 제거
    key = key.replace('\n', '')                # 줄바꿈 제거
    key = key.replace('\r', '')                # 캐리지 리턴 제거
    key = key.replace(' ', '')                 # 중간 공백 제거
    key = key.encode('ascii', 'ignore').decode('ascii')  # 비ASCII 문자 제거
    return key

try:
    raw_key = st.secrets["ANTHROPIC_API_KEY"]
    api_key = clean_api_key(str(raw_key))

    # API 키 기본 형식 검증
    if not api_key.startswith("sk-ant-"):
        st.error("❌ API 키 형식이 올바르지 않습니다. 'sk-ant-'로 시작해야 합니다.")
        st.code(f"현재 키 앞 10자리: {api_key[:10]}...", language="text")
        st.stop()

    if len(api_key) < 40:
        st.error("❌ API 키가 너무 짧습니다. 키를 다시 확인해주세요.")
        st.stop()

except KeyError:
    st.error("❌ API 키가 없습니다. Streamlit Cloud Secrets에 아래와 같이 등록해주세요.")
    st.code('ANTHROPIC_API_KEY = "sk-ant-api03-여기에_키_입력"', language="toml")
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

    st.markdown('<div class="sidebar-section">🧠 모델 선택</div>', unsafe_allow_html=True)
    model_option = st.selectbox(
        label="model",
        options=["claude-sonnet-4-5", "claude-opus-4-5"],
        format_func=lambda x: {
            "claude-sonnet-4-5": "⚡ Sonnet 4.5 — 빠르고 효율적",
            "claude-opus-4-5":   "🏆 Opus 4.5  — 가장 강력함",
        }[x],
        label_visibility="collapsed",
    )

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

    st.markdown('<div class="sidebar-section">📏 응답 길이</div>', unsafe_allow_html=True)
    max_tokens = st.slider(
        label="tokens",
        min_value=256,
        max_value=4096,
        value=1024,
        step=256,
        label_visibility="collapsed",
    )
    st.markdown(
        f"<div style='text-align:right; color:rgba(255,255,255,0.35);"
        f"font-size:0.78rem; margin-top:-0.5rem;'>"
        f"최대 <b style='color:#a78bfa;'>{max_tokens:,}</b> 토큰</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

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

model_display = {
    "claude-sonnet-4-5": ("⚡", "Claude Sonnet 4.5", "#667eea"),
    "claude-opus-4-5":   ("🏆", "Claude Opus 4.5",   "#f093fb"),
}
icon, name, color = model_display[model_option]
st.markdown(f"""
    <div style='display:flex; align-items:center; justify-content:center; margin-bottom:1.5rem;'>
        <div style='
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 30px;
            padding: 0.4rem 1.2rem;
            display: flex; align-items: center; gap: 0.5rem;
        '>
            <span>{icon}</span>
            <span style='color:{color}; font-size:0.85rem; font-weight:600;'>{name}</span>
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
# 웰컴 메시지
# ─────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-box">
            <div style='font-size:3rem; margin-bottom:1rem;'>💬</div>
            <div style='color:rgba(255,255,255,0.8); font-size:1.05rem;
                        font-weight:600; margin-bottom:0.7rem;'>
                무엇이든 물어보세요!
            </div>
            <div class="welcome-text">
                코딩 · 글쓰기 · 번역 · 분석 · 요약<br>
                어떤 주제든 도움을 드릴 수 있어요 ✨
            </div>
            <div style='margin-top:1.2rem; display:flex; gap:0.5rem;
                        justify-content:center; flex-wrap:wrap;'>
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

        if message["role"] == "assistant":
            assistant_index = sum(
                1 for m in st.session_state.messages[:i]
                if m["role"] == "assistant"
            )
            if assistant_index < len(st.session_state.usage_history):
                usage = st.session_state.usage_history[assistant_index]
                with st.expander("📊 토큰 사용량 보기"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("📥 입력", f"{usage['input_tokens']:,}")
                    c2.metric("📤 출력", f"{usage['output_tokens']:,}")
                    c3.metric("🔤 합계",
                              f"{usage['input_tokens'] + usage['output_tokens']:,}")
                    st.markdown(
                        f"<div style='color:rgba(255,255,255,0.3); font-size:0.78rem;'>"
                        f"🧠 모델: <code style='color:#a78bfa;'>"
                        f"{usage['model']}</code></div>",
                        unsafe_allow_html=True
                    )


# ─────────────────────────────────────────
# 사용자 입력 & API 호출
# ─────────────────────────────────────────
if user_input := st.chat_input("메시지를 입력하세요..."):

    # 사용자 메시지 저장 + 출력
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # API 호출
    answer        = None
    input_tokens  = 0
    output_tokens = 0
    error_msg     = None

    with st.spinner("✨ Claude가 생각하는 중..."):
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
            answer        = response.content[0].text
            input_tokens  = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

        except anthropic.AuthenticationError:
            error_msg = "❌ API 키 인증 실패! Secrets에서 키를 다시 확인해주세요."
        except anthropic.RateLimitError:
            error_msg = "⚠️ API 사용량 한도 초과! 잠시 후 다시 시도해주세요."
        except anthropic.BadRequestError as e:
            error_msg = f"🚫 잘못된 요청: {e}"
        except UnicodeEncodeError as e:
            error_msg = (
                f"❌ API 키 인코딩 오류!\n\n"
                f"Secrets에서 API 키에 **공백이나 특수문자**가 없는지 확인해주세요.\n\n"
                f"```\n{e}\n```"
            )
        except Exception as e:
            error_msg = (
                f"🚨 예상치 못한 오류!\n\n"
                f"```\n{type(e).__name__}: {e}\n```"
            )

    # 결과 출력
    if error_msg:
        st.error(error_msg)
        # 에러 시 마지막 사용자 메시지도 제거 (재시도 가능하도록)
        st.session_state.messages.pop()

    else:
        with st.chat_message("assistant"):
            st.markdown(answer)
            with st.expander("📊 토큰 사용량 보기"):
                c1, c2, c3 = st.columns(3)
                c1.metric("📥 입력", f"{input_tokens:,}")
                c2.metric("📤 출력", f"{output_tokens:,}")
                c3.metric("🔤 합계", f"{input_tokens + output_tokens:,}")
                st.markdown(
                    f"<div style='color:rgba(255,255,255,0.3); font-size:0.78rem;'>"
                    f"🧠 모델: <code style='color:#a78bfa;'>{model_option}</code></div>",
                    unsafe_allow_html=True
                )

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.usage_history.append({
            "input_tokens":  input_tokens,
            "output_tokens": output_tokens,
            "model":         model_option,
        })
        st.session_state.total_input_tokens  += input_tokens
        st.session_state.total_output_tokens += output_tokens
        st.session_state.total_requests      += 1
