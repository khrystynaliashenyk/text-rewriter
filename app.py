import streamlit as st
import requests

st.set_page_config(
    page_title="Text Rewriter",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ Text Rewriter")
st.write("Переписуй текст у різних стилях за допомогою штучного інтелекту.")

st.divider()

api_key = st.text_input(
    "Groq API Key",
    type="password",
    placeholder="Введіть свій API-ключ"
)

text = st.text_area(
    "Введіть текст для переписування",
    height=200,
    placeholder="Введіть або вставте свій текст сюди..."
)

style = st.selectbox(
    "Оберіть стиль тексту",
    ["Офіційний", "Розмовний"]
)

if st.button("Переписати текст", type="primary", use_container_width=True):

    if not api_key.strip():
        st.error("Введіть API-ключ Groq.")

    elif not text.strip():
        st.error("Введіть текст для переписування.")

    else:
        system_prompt = f"""
        You are a professional text editor.
        Rewrite the user's text in this style: {style}.

        Rules:
        - Preserve the original meaning and information.
        - Do not invent facts or details.
        - Keep the original language.
        - Return only the rewritten text.
        - Do not include introductions or explanations.
        """

        data = {
            "model": "openai/gpt-oss-20b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            "temperature": 0.5,
            "max_completion_tokens": 2048
        }

        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json"
        }

        try:
            with st.spinner("Переписуємо текст..."):
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60
                )

            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                st.subheader("Результат")
                st.text_area("Переписаний текст", value=result.strip(), height=250)

            elif response.status_code == 401:
                st.error("Неправильний API-ключ.")

            elif response.status_code == 429:
                st.error("Перевищено ліміт запитів. Спробуйте пізніше.")

            else:
                st.error(f"Помилка API: {response.status_code} — {response.text}")

        except requests.exceptions.RequestException as error:
            st.error(f"Помилка з'єднання: {error}")
