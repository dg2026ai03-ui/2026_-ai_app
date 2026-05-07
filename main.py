import streamlit as st
import anthropic

# ─────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Claude AI 질문 앱",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Claude AI 질문 앱")
st.markdown("Claude에게 무엇이든 질문해보세요!")
st.divider()

# ─────────────────────────────────────────
# API 키 불러오기 (Streamlit Secrets)
# ─────────────────────────────────────────
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except KeyError:
    st.error("❌ API 키가 설정되지 않았습니다. Streamlit Cloud의 Secrets에 ANTHROPIC_API_KEY를 등록해주세요.")
    st.stop()

# ─────────────────────────────────────────
# 사이드바 - 모델 선택 및 설정
# ─────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ 설정")

    model_option = st.selectbox(
        "🧠 AI 모델 선택",
        options=[
            "claude-sonnet-4-5",
            "claude-opus-4-5",
        ],
        format_func=lambda x: {
            "claude-sonnet-4-5": "✨ Claude Sonnet 4.5 (빠르고 효율적)",
            "claude-opus-4-5": "🏆 Claude Opus 4.5 (가장 강력함)",
        }[x],
        help="Sonnet은 빠른 응답, Opus는 더 깊은 분석에 적합합니다."
    )

    max_tokens = st.slider(
        "📏 최대 응답 토큰 수",
        min_value=256,
        max_value=4096,
        value=1024,
        step=256,
        help="응답의 최대 길이를 설정합니다. 값이 클수록 더 긴 답변을 받을 수 있습니다."
    )

    st.divider()
    st.markdown("### 📊 이번 세션 누적 사용량")

    # 세션 상태 초기화
    if "total_input_tokens" not in st.session_state:
        st.session_state.total_input_tokens = 0
    if "total_output_tokens" not in st.session_state:
        st.session_state.total_output_tokens = 0
    if "total_requests" not in st.session_state:
        st.session_state.total_requests = 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📥 입력 토큰", f"{st.session_state.total_input_tokens:,}")
        st.metric("🔢 총 요청 수", f"{st.session_state.total_requests:,}")
    with col2:
        st.metric("📤 출력 토큰", f"{st.session_state.total_output_tokens:,}")
        st.metric("🔤 총 토큰", f"{st.session_state.total_input_tokens + st.session_state.total_output_tokens:,}")

    if st.button("🔄 사용량 초기화", use_container_width=True):
        st.session_state.total_input_tokens = 0
        st.session_state.total_output_tokens = 0
        st.session_state.total_requests = 0
        st.rerun()

# ─────────────────────────────────────────
# 대화 기록 초기화
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "usage_history" not in st.session_state:
    st.session_state.usage_history = []

# ─────────────────────────────────────────
# 대화 기록 출력
# ─────────────────────────────────────────
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # AI 답변 아래에 해당 응답의 사용량 표시
        if message["role"] == "assistant" and i // 2 < len(st.session_state.usage_history):
            usage = st.session_state.usage_history[i // 2]
            with st.expander("📊 이 응답의 토큰 사용량"):
                u_col1, u_col2, u_col3 = st.columns(3)
                with u_col1:
                    st.metric("📥 입력 토큰", f"{usage['input_tokens']:,}")
                with u_col2:
                    st.metric("📤 출력 토큰", f"{usage['output_tokens']:,}")
                with u_col3:
                    st.metric("🔤 합계", f"{usage['input_tokens'] + usage['output_tokens']:,}")
                st.caption(f"🧠 사용 모델: `{usage['model']}`")

# ─────────────────────────────────────────
# 대화 기록 초기화 버튼
# ─────────────────────────────────────────
if st.session_state.messages:
    if st.button("🗑️ 대화 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.usage_history = []
        st.rerun()

# ─────────────────────────────────────────
# 사용자 입력 처리
# ─────────────────────────────────────────
if user_input := st.chat_input("질문을 입력하세요..."):

    # 사용자 메시지 저장 및 출력
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Claude API 호출
    with st.chat_message("assistant"):
        with st.spinner("🤔 Claude가 생각하는 중..."):
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

                answer = response.content[0].text
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens

                # 답변 출력
                st.markdown(answer)

                # 토큰 사용량 표시
                with st.expander("📊 이 응답의 토큰 사용량"):
                    u_col1, u_col2, u_col3 = st.columns(3)
                    with u_col1:
                        st.metric("📥 입력 토큰", f"{input_tokens:,}")
                    with u_col2:
                        st.metric("📤 출력 토큰", f"{output_tokens:,}")
                    with u_col3:
                        st.metric("🔤 합계", f"{input_tokens + output_tokens:,}")
                    st.caption(f"🧠 사용 모델: `{model_option}`")

                # 세션 상태 업데이트
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.session_state.usage_history.append({
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "model": model_option,
                })
                st.session_state.total_input_tokens += input_tokens
                st.session_state.total_output_tokens += output_tokens
                st.session_state.total_requests += 1

            except anthropic.AuthenticationError:
                st.error("❌ API 키가 올바르지 않습니다. Secrets 설정을 확인해주세요.")
            except anthropic.RateLimitError:
                st.error("⚠️ API 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
            except anthropic.APIError as e:
                st.error(f"🚨 API 오류가 발생했습니다: {e}")
