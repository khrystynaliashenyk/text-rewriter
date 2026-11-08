
import streamlit as st
import requests

st.set_page_config(
    page_title="Text Rewriter",
    page_icon="✍️",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #F5F2FA;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 850px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    background: linear-gradient(135deg, #FFFFFF, #F0EAF8);
    border: 1px solid #E9E0F1;
    border-radius: 24px;
    padding: 35px;
    margin-bottom: 25px;
}

.eyebrow {
    color: #8B70AB;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero h1 {
    color: #302641;
    font-size: 43px;
    font-weight: 800;
    margin: 12px 0 5px 0;
}

.hero p {
    color: #756C80;
    font-size: 16px;
    line-height: 1.6;
}

.section-title {
    color: #302641;
    font-size: 21px;
    font-weight: 700;
    margin: 12px 0;
}

div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input {
    background: #FBFAFD !important;
    border: 1px solid #E5DDED !important;
    border-radius: 12px !important;
    color: #302641 !important;
}

div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: #9A7BBE !important;
    box-shadow: 0 0 0 1px #9A7BBE !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #FBFAFD;
    border-color: #E5DDED;
    border-radius: 12px;
}

.stButton > button,
.stFormSubmitButton > button {
    background: #8063A5 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    min-height: 48px;
    font-weight: 700 !important;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #6C508F !important;
    border: none !important;
}

.result-card {
    background: white;
    border: 1px solid #E9E0F1;
    border-radius: 18px;
    padding: 24px;
    margin-top: 20px;
}

.result-label {
    color: #8B70AB;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# Header
st.markdown("""
<div class="hero">
    <div class="eyebrow">AI WRITING ASSISTANT</div>
    <h1>Text Rewriter</h1>
</div>
""", unsafe_allow_html=True)


# Input section
st.markdown(
    '<div class="section-title">01. Твій текст</div>',
    unsafe_allow_html=True
)

st.write("Введи текст, який хочеш переписати.")

with st.form("rewrite_form"):

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Встав свій API-ключ"
    )

    text = st.text_area(
        "Вихідний текст",
        height=180,
        placeholder="Напиши або встав свій текст сюди..."
    )

    st.markdown(
        '<div class="section-title">02. Обери стиль</div>',
        unsafe_allow_html=True
    )

    style = st.selectbox(
        "Стиль переписування",
        [
            "Офіційний",
            "Розмовний",
        ]
    )

    submitted = st.form_submit_button(
        "Переписати текст",
        use_container_width=True
    )


if submitted:

    if not api_key.strip():
        st.error("Будь ласка, введи API-ключ Groq.")

    elif not text.strip():
        st.error("Будь ласка, введи текст для переписування.")

    else:

        system_prompt = f"""
        You are a professional text editor.

        Rewrite the user's text in the following style: {style}.

        Rules:
        - Preserve the original meaning and important information.
        - Do not invent facts, names, dates or details.
        - Keep the original language of the input.
        - Follow the selected style consistently.
        - Return only the rewritten text.
        - Do not include introductions or explanations.
        """

        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-oss-20b",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            "temperature": 0.5,
            "max_completion_tokens": 2048
        }

        try:
            with st.spinner("Працюємо над текстом..."):

                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60
                )

            if response.status_code == 200:

                result = response.json()["choices"][0]["message"]["content"].strip()

                st.session_state["result"] = result

            elif response.status_code == 401:
                st.error("Неправильний API-ключ. Перевір його.")

            elif response.status_code == 429:
                st.error("Перевищено ліміт запитів. Спробуй пізніше.")

            else:
                st.error(
                    f"Помилка API: {response.status_code}. "
                    "Перевір запит або спробуй пізніше."
                )

        except requests.exceptions.Timeout:
            st.error("Час очікування вичерпано. Спробуй ще раз.")

        except requests.exceptions.RequestException:
            st.error("Не вдалося з'єднатися з Groq API.")


# Display result
if st.session_state.get("result"):

    st.markdown("""
    <div class="result-card">
        <div class="result-label">✦ 03. РЕЗУЛЬТАТ</div>
        <h3 style="color:#302641; margin-top:8px;">
            Твій оновлений текст
        </h3>
    </div>
    """, unsafe_allow_html=True)

    st.text_area(
        "Переписаний текст",
        value=st.session_state["result"],
        height=200,
        disabled=False,
        label_visibility="collapsed"
    )

    st.download_button(
        "Завантажити результат",
        data=st.session_state["result"],
        file_name="rewritten_text.txt",
        mime="text/plain",
        use_container_width=True
    )


