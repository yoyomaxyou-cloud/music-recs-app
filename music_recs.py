# music_recs_app.py

import streamlit as st
import openai
import time
from openai.error import RateLimitError

# --- Настройка API ключа ---
openai.api_key = st.secrets["OPENAI_API_KEY"]  # или просто "YOUR_API_KEY" для локальной разработки

# --- Функция получения рекомендаций с обработкой лимитов ---
def get_recommendations(user_items, categories, context, max_recs, max_retries=5, initial_wait=5):
    prompt = (
        f"Сделай рекомендации музыки на основе: {user_items}, "
        f"категории: {categories}, контекст: {context}. "
        f"Максимум {max_recs} рекомендаций."
    )
    
    wait_seconds = initial_wait
    for attempt in range(1, max_retries + 1):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8
            )
            return response.choices[0].message["content"]
        except RateLimitError:
            if attempt == max_retries:
                return "Превышен лимит запросов OpenAI. Попробуйте позже."
            st.warning(f"Превышен лимит запросов. Попытка {attempt}/{max_retries}, ждём {wait_seconds} секунд...")
            time.sleep(wait_seconds)
            wait_seconds *= 2  # экспоненциальная задержка

# --- Интерфейс Streamlit ---
st.title("Музыкальные рекомендации 🎵")

user_items = st.text_input("Ваши любимые песни/исполнители (через запятую):")
categories = st.text_input("Жанры или категории:")
context = st.text_input("Контекст/настроение:")
max_recs = st.slider("Сколько рекомендаций хотите?", 1, 10, 5)

if st.button("Получить рекомендации"):
    if not user_items.strip():
        st.error("Пожалуйста, укажите хотя бы одну песню или исполнителя.")
    else:
        with st.spinner("Генерируем рекомендации..."):
            recs = get_recommendations(user_items, categories, context, max_recs)
        st.success("Готово!")
        st.text_area("Рекомендации:", recs, height=200)
