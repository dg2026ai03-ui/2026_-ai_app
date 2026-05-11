import streamlit as st
import anthropic
import time
import json
from datetime import datetime

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
        color: rgba(255,255,255,0.5);
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }
    .stChatInput textarea {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 14px !important;
        color: white !important;
        font-family: 'Noto Sans KR', sans-serif !important;
        font-size: 0.95rem !important;
    }
    .stChatInput textarea:focus {
        border: 1px solid rgba(102,126,234,0.6) !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.15) !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    .stTextArea textarea {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Noto Sans KR', sans-serif !important;
        font-size: 0.88rem !important;
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
        box-shadow: 0 6px 20px rgba(102,126,234,0.35) !important;
    }
    [data-testid="stSidebar"] {
        background: rgba(15,12,41,0.85) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
        backdrop-filter: blur(20px) !important;
    }
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        padding: 0.8rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.75rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #a78bfa !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }
    hr {
        border: none !important;
        border-top: 1px solid rgba(255,255,255,0.08) !important;
        margin: 1.5rem 0 !important;
    }
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(102,126,234,0.4);
        border-radius: 10px;
    }
    .stMarkdown, p, li {
        color: rgba(255,255,255,0.85);
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
    .info-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 0.25rem 0.75rem;
        font-size: 0.75rem;
        color: rgba(255,255,255,0.5);
        margin: 0.2rem;
    }
    .favorite-card {
        background: rgba(255,215,0,0.07);
        border: 1px solid rgba(255,215,0,0.2);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }
    .favorite-card-text {
        color: rgba(255,255,255,0.8);
        font-size: 0.88rem;
        line-height: 1.7;
    }
    .favorite-meta {
        color: rgba(255,215,0,0.5);
        font-size: 0.72rem;
        margin-top: 0.5rem;
    }
    .char-counter {
        text-align: right;
        color: rgba(255,255,255,0.3);
        font-size: 0.75rem;
        margin-top: -0.8rem;
        margin-bottom: 0.5rem;
    }
    .response-time {
        color: rgba(255,255,255,0.3);
        font-size: 0.72rem;
    }
    .tab-content {
        padding: 1rem 0;
    }
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 12px !important;
        padding: 0.3rem !important;
        gap: 0.2rem !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 1rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# API 키 정제 함수
# ─────────────────────────────────────────
def clean_api_key(key: str) -> str:
    key = key.strip()
    key = key.replace('\n', '').replace('\r', '').replace(' ', '')
    key = key.encode('ascii', 'ignore').decode('ascii')
    return key


# ─────────────────────────────────────────
# API 키 불러오기
# ─────────────────────────────────────────
try:
    raw_key = st.secrets["ANTHROPIC_API_KEY"]
    api_key = clean_api_key(str(raw_key))
    if not api_key.startswith("sk-ant-"):
        st.error("❌ API 키 형식이 올바르지 않습니다. 'sk-ant-'로 시작해야 합니다.")
        st.stop()
    if len(api_key) < 40:
        st.error("❌ API 키가 너무 짧습니다.")
        st.stop()
except KeyError:
    st.error("❌ Streamlit Cloud Secrets에 ANTHROPIC_API_KEY를 등록해주세요.")
    st.code('ANTHROPIC_API_KEY = "sk-ant-api03-여기에_키_입력"', language="toml")
    st.stop()


# ─────────────────────────────────────────
# 세션 상태 초기화
# ─────────────────────────────────────────
defaults = {
    "messages": [],
    "usage_history": [],
    "total_input_tokens": 0,
    "total_output_tokens": 0,
    "total_requests": 0,
    "favorites": [],
    "response_times": [],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ─────────────────────────────────────────
# 시스템 프롬프트 프리셋
# ─────────────────────────────────────────
SYSTEM_PRESETS = {
    "🤖 기본 어시스턴트": "당신은 친절하고 유능한 AI 어시스턴트입니다. 사용자의 질문에 정확하고 도움이 되는 답변을 제공하세요.",
    "👩‍💻 코딩 전문가": "당신은 숙련된 소프트웨어 개발자입니다. 코드를 작성할 때는 항상 주석을 달고, 효율적이고 읽기 쉬운 코드를 제공하세요. 버그가 있으면 정확히 짚어주세요.",
    "✍️ 글쓰기 도우미": "당신은 창의적인 글쓰기 전문가입니다. 사용자의 글을 더 풍부하고 매력적으로 만들어주세요. 문법, 문체, 표현력을 향상시키는 제안을 해주세요.",
    "🧑‍🏫 친절한 선생님": "당신은 인내심 있고 친절한 선생님입니다. 어려운 개념을 쉬운 언어로 설명하고, 예시를 들어 이해를 돕습니다. 학생이 스스로 생각할 수 있도록 유도하세요.",
    "🌐 영어 번역가": "당신은 전문 번역가입니다. 한국어를 영어로, 영어를 한국어로 자연스럽게 번역합니다. 번역 후 어색한 표현이 있으면 대안도 함께 제시하세요.",
    "📊 데이터 분석가": "당신은 데이터 분석 전문가입니다. 데이터를 분석하고, 인사이트를 도출하며, 시각화 방법을 제안합니다. 통계적 근거를 바탕으로 명확하게 설명하세요.",
    "✏️ 직접 입력": "",
}


# ─────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────
with st.sidebar:
    # 로고
    st.markdown("""
        <div style='text-align:center; padding:1rem 0 1.5rem;'>
            <div style='font-size:2.5rem; margin-bottom:0.4rem;'>✨</div>
            <div style='font-size:1.1rem; font-weight:700;
                background:linear-gradient(135deg,#667eea,#f093fb);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                background-clip:text;'>Claude AI</div>
            <div style='color:rgba(255,255,255,0.3); font-size:0.75rem; margin-top:0.2rem;'>
                Powered by Anthropic
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── 모델 선택 ──
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
            <div style='margin-top:0.4rem;'>
                <span class='badge'>⚡ 빠른 응답</span>
                <span class='badge'>💰 경제적</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='margin-top:0.4rem;'>
                <span class='badge'>🧠 최고 성능</span>
                <span class='badge'>🔬 심층 분석</span>
            </div>""", unsafe_allow_html=True)

    # ── 응답 길이 ──
    st.markdown('<div class="sidebar-section">📏 응답 길이</div>', unsafe_allow_html=True)
    max_tokens = st.slider(
        "tokens", 256, 4096, 1024, 256,
        label_visibility="collapsed"
    )
    st.markdown(
        f"<div style='text-align:right;color:rgba(255,255,255,0.35);font-size:0.78rem;margin-top:-0.5rem;'>"
        f"최대 <b style='color:#a78bfa;'>{max_tokens:,}</b> 토큰</div>",
        unsafe_allow_html=True
    )

    # ── Temperature ──
    st.markdown('<div class="sidebar-section">🌡️ 창의성 (Temperature)</div>',
                unsafe_allow_html=True)
    temperature = st.slider(
        "temperature", 0.0, 1.0, 0.7, 0.05,
        label_visibility="collapsed",
        help="낮을수록 일관된 답변, 높을수록 창의적인 답변"
    )
    temp_label = (
        "🧊 정확·일관" if temperature < 0.3 else
        "⚖️ 균형" if temperature < 0.7 else
        "🔥 창의적"
    )
    st.markdown(
        f"<div style='text-align:right;color:rgba(255,255,255,0.35);font-size:0.78rem;margin-top:-0.5rem;'>"
        f"{temp_label} <b style='color:#a78bfa;'>{temperature}</b></div>",
        unsafe_allow_html=True
    )

    # ── 시스템 프롬프트 ──
    st.markdown('<div class="sidebar-section">🎭 AI 역할 설정</div>',
                unsafe_allow_html=True)
    preset_choice = st.selectbox(
        "preset", list(SYSTEM_PRESETS.keys()),
        label_visibility="collapsed"
    )
    if preset_choice == "✏️ 직접 입력":
        system_prompt = st.text_area(
            "system_custom", "",
            placeholder="AI에게 부여할 역할이나 지시사항을 입력하세요...",
            height=100,
            label_visibility="collapsed"
        )
    else:
        system_prompt = SYSTEM_PRESETS[preset_choice]
        st.markdown(
            f"<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);"
            f"border-radius:10px;padding:0.7rem 0.9rem;font-size:0.78rem;"
            f"color:rgba(255,255,255,0.5);line-height:1.6;margin-top:0.4rem;'>"
            f"{system_prompt[:120]}{'...' if len(system_prompt) > 120 else ''}</div>",
            unsafe_allow_html=True
        )

    # ── 세션 사용량 ──
    st.markdown('<div class="sidebar-section">📊 세션 사용량</div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.metric("📥 입력", f"{st.session_state.total_input_tokens:,}")
        st.metric("🔢 요청", f"{st.session_state.total_requests:,}")
    with c2:
        st.metric("📤 출력", f"{st.session_state.total_output_tokens:,}")
        total_tok = (st.session_state.total_input_tokens
                     + st.session_state.total_output_tokens)
        st.metric("🔤 합계", f"{total_tok:,}")

    # 평균 응답 시간
    if st.session_state.response_times:
        avg_time = sum(st.session_state.response_times) / len(st.session_state.response_times)
        st.markdown(
            f"<div style='text-align:center;margin-top:0.5rem;'>"
            f"<span class='info-chip'>⏱️ 평균 응답 {avg_time:.1f}초</span></div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 초기화 버튼 ──
    ca, cb = st.columns(2)
    with ca:
        if st.button("🗑️ 대화 초기화", use_container_width=True):
            st.session_state.messages = []
            st.session_state.usage_history = []
            st.session_state.response_times = []
            st.rerun()
    with cb:
        if st.button("📊 통계 초기화", use_container_width=True):
            st.session_state.total_input_tokens = 0
            st.session_state.total_output_tokens = 0
            st.session_state.total_requests = 0
            st.session_state.response_times = []
            st.rerun()

    # ── 대화 내보내기 ──
    if st.session_state.messages:
        st.markdown('<div class="sidebar-section">💾 대화 내보내기</div>',
                    unsafe_allow_html=True)

        # TXT 내보내기
        export_txt = "\n\n".join([
            f"[{'나' if m['role'] == 'user' else 'Claude'}]\n{m['content']}"
            for m in st.session_state.messages
        ])
        export_txt = f"=== Claude AI 대화 기록 ===\n날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n모델: {model_option}\n\n" + export_txt
        st.download_button(
            label="📄 TXT로 저장",
            data=export_txt.encode("utf-8"),
            file_name=f"claude_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

        # JSON 내보내기
        export_json = json.dumps({
            "exported_at": datetime.now().isoformat(),
            "model": model_option,
            "messages": st.session_state.messages,
            "usage": {
                "total_input_tokens": st.session_state.total_input_tokens,
                "total_output_tokens": st.session_state.total_output_tokens,
                "total_requests": st.session_state.total_requests,
            }
        }, ensure_ascii=False, indent=2)
        st.download_button(
            label="🗂️ JSON으로 저장",
            data=export_json.encode("utf-8"),
            file_name=f"claude_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True,
        )


# ─────────────────────────────────────────
# 메인 영역 - 헤더
# ─────────────────────────────────────────
st.markdown('<h1 class="main-title">✨ Claude AI 챗봇</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="main-subtitle">Anthropic의 최신 AI 모델과 대화해보세요</p>',
    unsafe_allow_html=True
)

# 현재 설정 칩 표시
model_display = {
    "claude-sonnet-4-5": ("⚡", "Sonnet 4.5", "#667eea"),
    "claude-opus-4-5":   ("🏆", "Opus 4.5",   "#f093fb"),
}
m_icon, m_name, m_color = model_display[model_option]
temp_color = "#60a5fa" if temperature < 0.3 else "#34d399" if temperature < 0.7 else "#f87171"

st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:center;
                flex-wrap:wrap;gap:0.4rem;margin-bottom:1.5rem;'>
        <span class='info-chip'>{m_icon} {m_name}</span>
        <span class='info-chip'>🌡️ <span style='color:{temp_color};font-weight:600;'>{temperature}</span></span>
        <span class='info-chip'>📏 {max_tokens:,} 토큰</span>
        <span class='info-chip'>🎭 {preset_choice}</span>
    </div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 탭 구성 (💬 대화 / ⭐ 즐겨찾기)
# ─────────────────────────────────────────
tab_chat, tab_fav = st.tabs(["💬 대화", "⭐ 즐겨찾기"])


# ══════════════════════════════════════════
# 탭 1 : 대화
# ══════════════════════════════════════════
with tab_chat:

    # 웰컴 메시지
    if not st.session_state.messages:
        st.markdown("""
            <div class="welcome-box">
                <div style='font-size:3rem;margin-bottom:1rem;'>💬</div>
                <div style='color:rgba(255,255,255,0.8);font-size:1.05rem;
                            font-weight:600;margin-bottom:0.7rem;'>
                    무엇이든 물어보세요!
                </div>
                <div class="welcome-text">
                    코딩 · 글쓰기 · 번역 · 분석 · 요약<br>
                    어떤 주제든 도움을 드릴 수 있어요 ✨
                </div>
                <div style='margin-top:1.2rem;display:flex;gap:0.5rem;
                            justify-content:center;flex-wrap:wrap;'>
                    <span class='badge'>💡 아이디어</span>
                    <span class='badge'>🔍 정보 검색</span>
                    <span class='badge'>📝 문서 작성</span>
                    <span class='badge'>🐍 코딩</span>
                    <span class='badge'>🌐 번역</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 대화 기록 출력
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":
                assistant_index = sum(
                    1 for m in st.session_state.messages[:i]
                    if m["role"] == "assistant"
                )

                # 메타 정보 (응답 시간 + 토큰)
                meta_parts = []
                if assistant_index < len(st.session_state.response_times):
                    rt = st.session_state.response_times[assistant_index]
                    meta_parts.append(f"⏱️ {rt:.1f}초")
                if assistant_index < len(st.session_state.usage_history):
                    usage = st.session_state.usage_history[assistant_index]
                    meta_parts.append(
                        f"🔤 {usage['input_tokens'] + usage['output_tokens']:,} 토큰"
                    )
                if meta_parts:
                    st.markdown(
                        f"<div style='margin-top:0.3rem;'>"
                        + "".join(f"<span class='info-chip'>{p}</span>" for p in meta_parts)
                        + "</div>",
                        unsafe_allow_html=True
                    )

                # 토큰 상세 + 즐겨찾기 버튼
                col_exp, col_fav = st.columns([4, 1])
                with col_exp:
                    if assistant_index < len(st.session_state.usage_history):
                        usage = st.session_state.usage_history[assistant_index]
                        with st.expander("📊 토큰 상세"):
                            cc1, cc2, cc3 = st.columns(3)
                            cc1.metric("📥 입력", f"{usage['input_tokens']:,}")
                            cc2.metric("📤 출력", f"{usage['output_tokens']:,}")
                            cc3.metric("🔤 합계",
                                       f"{usage['input_tokens']+usage['output_tokens']:,}")
                            st.markdown(
                                f"<div style='color:rgba(255,255,255,0.3);font-size:0.78rem;'>"
                                f"🧠 <code style='color:#a78bfa;'>{usage['model']}</code></div>",
                                unsafe_allow_html=True
                            )
                with col_fav:
                    if st.button("⭐", key=f"fav_{i}",
                                 help="즐겨찾기에 저장"):
                        # 해당 AI 답변 앞의 사용자 질문 찾기
                        user_q = ""
                        for j in range(i - 1, -1, -1):
                            if st.session_state.messages[j]["role"] == "user":
                                user_q = st.session_state.messages[j]["content"]
                                break
                        fav_item = {
                            "question": user_q,
                            "answer": message["content"],
                            "model": model_option,
                            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        }
                        # 중복 저장 방지
                        already = any(
                            f["answer"] == fav_item["answer"]
                            for f in st.session_state.favorites
                        )
                        if not already:
                            st.session_state.favorites.append(fav_item)
                            st.toast("⭐ 즐겨찾기에 저장했어요!", icon="⭐")
                        else:
                            st.toast("이미 저장된 답변이에요!", icon="ℹ️")

    # ── 입력창 ──
    if user_input := st.chat_input("메시지를 입력하세요..."):

        # 글자수 표시 (입력 후)
        st.markdown(
            f"<div class='char-counter'>{len(user_input):,}자</div>",
            unsafe_allow_html=True
        )

        # 사용자 메시지 저장 + 출력
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # API 호출
        answer        = None
        input_tokens  = 0
        output_tokens = 0
        error_msg     = None
        elapsed       = 0.0

        with st.spinner("✨ Claude가 생각하는 중..."):
            try:
                client = anthropic.Anthropic(api_key=api_key)

                # 시스템 프롬프트 포함 여부
                kwargs = dict(
                    model=model_option,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                )
                if system_prompt.strip():
                    kwargs["system"] = system_prompt.strip()

                start_time = time.time()
                response   = client.messages.create(**kwargs)
                elapsed    = time.time() - start_time

                answer        = response.content[0].text
                input_tokens  = response.usage.input_tokens
                output_tokens = response.usage.output_tokens

            except anthropic.AuthenticationError:
                error_msg = "❌ API 키 인증 실패! Secrets에서 ANTHROPIC_API_KEY를 확인해주세요."
            except anthropic.RateLimitError:
                error_msg = "⚠️ API 사용량 한도 초과! 잠시 후 다시 시도해주세요."
            except anthropic.BadRequestError as e:
                error_msg = f"🚫 잘못된 요청: {e}"
            except UnicodeEncodeError as e:
                error_msg = (
                    f"❌ API 키 인코딩 오류! 키에 공백·특수문자가 없는지 확인해주세요.\n\n"
                    f"```\n{e}\n```"
                )
            except Exception as e:
                error_msg = f"🚨 오류 발생\n\n```\n{type(e).__name__}: {e}\n```"

        if error_msg:
            st.error(error_msg)
            st.session_state.messages.pop()
        else:
            with st.chat_message("assistant"):
                st.markdown(answer)

                # 메타 칩
                st.markdown(
                    f"<div style='margin-top:0.3rem;'>"
                    f"<span class='info-chip'>⏱️ {elapsed:.1f}초</span>"
                    f"<span class='info-chip'>🔤 {input_tokens+output_tokens:,} 토큰</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                # 토큰 상세
                with st.expander("📊 토큰 상세"):
                    cc1, cc2, cc3 = st.columns(3)
                    cc1.metric("📥 입력", f"{input_tokens:,}")
                    cc2.metric("📤 출력", f"{output_tokens:,}")
                    cc3.metric("🔤 합계", f"{input_tokens+output_tokens:,}")
                    st.markdown(
                        f"<div style='color:rgba(255,255,255,0.3);font-size:0.78rem;'>"
                        f"🧠 <code style='color:#a78bfa;'>{model_option}</code> · "
                        f"🌡️ temperature {temperature}</div>",
                        unsafe_allow_html=True
                    )

            # 세션 업데이트
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.session_state.usage_history.append({
                "input_tokens":  input_tokens,
                "output_tokens": output_tokens,
                "model":         model_option,
            })
            st.session_state.response_times.append(elapsed)
            st.session_state.total_input_tokens  += input_tokens
            st.session_state.total_output_tokens += output_tokens
            st.session_state.total_requests      += 1


# ══════════════════════════════════════════
# 탭 2 : 즐겨찾기
# ══════════════════════════════════════════
with tab_fav:
    if not st.session_state.favorites:
        st.markdown("""
            <div class="welcome-box" style='margin-top:1rem;'>
                <div style='font-size:2.5rem;margin-bottom:0.8rem;'>⭐</div>
                <div style='color:rgba(255,255,255,0.6);font-size:0.95rem;'>
                    아직 저장된 즐겨찾기가 없어요.<br>
                    <span style='color:rgba(255,255,255,0.35);font-size:0.85rem;'>
                    마음에 드는 AI 답변 옆 ⭐ 버튼을 눌러 저장해보세요!
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='color:rgba(255,255,255,0.4);font-size:0.85rem;margin-bottom:1rem;'>"
            f"⭐ 총 <b style='color:#a78bfa;'>{len(st.session_state.favorites)}</b>개 저장됨</div>",
            unsafe_allow_html=True
        )

        # 즐겨찾기 내보내기
        fav_export = "\n\n".join([
            f"[질문]\n{f['question']}\n\n[답변]\n{f['answer']}\n저장: {f['saved_at']}"
            for f in st.session_state.favorites
        ])
        st.download_button(
            "📄 즐겨찾기 TXT 저장",
            data=fav_export.encode("utf-8"),
            file_name=f"favorites_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # 즐겨찾기 목록 (최신순)
        for idx, fav in enumerate(reversed(st.session_state.favorites)):
            real_idx = len(st.session_state.favorites) - 1 - idx
            with st.container():
                st.markdown(f"""
                    <div class="favorite-card">
                        <div style='color:rgba(255,215,0,0.7);font-size:0.78rem;
                                    margin-bottom:0.4rem;font-weight:600;'>
                            🙋 질문
                        </div>
                        <div style='color:rgba(255,255,255,0.6);font-size:0.85rem;
                                    margin-bottom:0.8rem;'>
                            {fav['question'][:200]}{'...' if len(fav['question'])>200 else ''}
                        </div>
                        <div style='color:rgba(255,215,0,0.7);font-size:0.78rem;
                                    margin-bottom:0.4rem;font-weight:600;'>
                            🤖 답변
                        </div>
                        <div class="favorite-card-text">
                            {fav['answer'][:400]}{'...' if len(fav['answer'])>400 else ''}
                        </div>
                        <div class="favorite-meta">
                            🧠 {fav['model']} · 🕐 {fav['saved_at']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                if st.button(f"🗑️ 삭제", key=f"del_fav_{real_idx}"):
                    st.session_state.favorites.pop(real_idx)
                    st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)
