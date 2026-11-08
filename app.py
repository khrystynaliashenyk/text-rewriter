import streamlit as st
import requests


st.set_page_config(
    page_title="Text Rewriter",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

/* Main page */

.stApp {
    background: #F5F2FA;
    color: #302641;
    font-family: sans-serif;
}

.block-container {
    max-width: 850px;
    padding: 45px 25px 60px 25px;
}

/* Hide default Streamlit elements */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Main heading card */

.hero {
    background: linear-gradient(
        135deg,
        #FFFFFF 0%,
        #F0EAF8 100%
    );
    border: 1px solid #E8DDF1;
    border-radius: 24px;
    padding: 38px;
    margin-bottom: 35px;
}

.hero-label {
    color: #8B70AB;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 15px;
}

.hero h1 {
    color: #302641 !important;
    font-size: 43px;
    font-weight: 800;
    margin: 0 0 12px 0;
    line-height: 1.2;
}

.hero p {
    color: #756C80 !important;
    font-size: 16px;
    line-height: 1.7;
    margin: 0;
}

/* Section headings */

.section-title {
    color: #302641 !important;
    font-size: 22px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 8px;
}

.section-description {
    color: #756C80 !important;
    font-size: 14px;
    margin-bottom: 18px;
}

/* All labels */

.stApp label,
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stWidgetLabel"] p {
    color: #49385D !important;
    font-weight: 600 !important;
}

/* Text input and textarea */

.stApp input,
.stApp textarea {
    background-color: #FFFFFF !important;
    color: #302641 !important;
    border: 1px solid #E5DDED !important;
    border-radius: 12px !important;
    font-size: 15px !important;
}

.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #A39AAF !important;
    opacity: 1 !important;
}

.stApp input:focus,
.stApp textarea:focus {
    border-color: #9A7BBE !important;
    box-shadow: 0 0 0 1px #9A7BBE !important;
}

/* Select box */

.stApp [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #302641 !important;
    border: 1px solid #E5DDED !important;
    border-radius: 12px !important;
}

.stApp [data-baseweb="select"] span {
    color: #302641 !important;
}

.stApp [role="option"] {
    color: #302641 !important;
    background-color: #FFFFFF !important;
}

.stApp [role="option"]:hover {
    background-color: #F0EAF8 !important;
}

/* Form */

.stApp [data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* Primary button */

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background: #8063A5 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 13px !important;
    min-height: 50px;
    font-size: 15px !important;
    font-weight: 700 !important;
    transition: background 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background: #6C508F !important;
    color: #FFFFFF !important;
    border: none !important;
}

/* Result card */

.result-card {
    background: #FFFFFF;
    border: 1px solid #E8DDF1;
    border-radius: 18px;
    padding: 25px;
    margin-top: 35px;
    margin-bottom: 15px;
}

.result-label {
    color: #8B70AB;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.result-title {
    color: #302641;
    font-size: 23px;
    font-weight: 750;
    margin-top: 10px;
}

/* Messages */

.stAlert {
    border-radius: 12px;
}

/* Footer */

.custom-footer {
    text-align: center;
    color: #9A8EAA;
    font-size: 12px;
    margin-top: 45px;
    letter-spacing: 1px;
}

/* Mobile */

@media (max-width: 600px) {
    .block-container {
        padding: 25px 15px 40px 15px;
    }

    .hero {
        padding: 25px;
    }

    .hero h1 {
        font-size: 32px;
    }

    .hero p {
        font-size: 14px;
    }
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <div class="hero-label">
        <h1>AI Text Rewriter</h1>
    </div>

   
</div>
""", unsafe_allow_html=True)



st.markdown(
    '<div class="section-title">Твій текст</div>',
    unsafe_allow_html=True
)

with st.form("rewrite_form", border=False):

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
        '<div class="section-title">Обери стиль</div>',
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

        Your task is to rewrite the user's text
        in the following style: {style}.

        Follow these rules:
        - Preserve the original meaning.
        - Preserve all important facts and information.
        - Do not invent names, dates or details.
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

            with st.spinner("Працюємо над твоїм текстом..."):

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

                st.session_state.pop("result", None)
                st.error("Неправильний API-ключ. Перевір його.")

            elif response.status_code == 429:

                st.session_state.pop("result", None)
                st.error(
                    "Перевищено ліміт запитів Groq. "
                    "Спробуй пізніше."
                )

            else:

                st.session_state.pop("result", None)
                st.error(
                    f"Помилка API: {response.status_code}. "
                    "Перевір запит або спробуй пізніше."
                )

        except requests.exceptions.Timeout:

            st.session_state.pop("result", None)
            st.error("Час очікування відповіді вичерпано.")

        except requests.exceptions.RequestException:

            st.session_state.pop("result", None)
            st.error("Не вдалося з'єднатися з Groq API.")


if st.session_state.get("result"):

    st.markdown("""
    <div class="section-title">
             РЕЗУЛЬТАТ
        </div>
    </div>
    """, unsafe_allow_html=True)

    result = st.session_state["result"]

    st.text_area(
        "Переписаний текст",
        value=result,
        height=200,
        label_visibility="collapsed",
        key="result_output"
    )

    st.download_button(
        "Завантажити результат",
        data=result,
        file_name="rewritten_text.txt",
        mime="text/plain",
        use_container_width=True
    )

