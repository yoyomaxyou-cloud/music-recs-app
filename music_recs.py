import streamlit as st
import openai

# Подключаем ключ OpenAI из секретов Streamlit
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Рекомендации от ИИ", page_icon="🎯")

st.title("Рекомендации от ИИ для всего!")
st.markdown("Введите ваши любимые объекты и выберите категории, чтобы получить персональные рекомендации.")

# --- Ввод пользователем ---
user_items = st.text_area(
    "Введите список ваших любимых объектов (треки, фильмы, игры, сериалы и т.д.), через запятую:",
    placeholder="Например: Inception, Dark Souls, Stranger Things, The Beatles"
)

categories = st.text_input(
    "Категории рекомендаций (через запятую):",
    placeholder="Музыка, Фильмы, Игры, Сериалы"
)

context = st.text_input(
    "Контекст / настроение / цель (необязательно):",
    placeholder="Например: хочу расслабиться, для вечеринки, изучаю жанр"
)

max_recs = st.slider("Сколько рекомендаций показывать за раз:", 5, 50, 15)

# --- Сессия для хранения рекомендаций ---
if "all_recs" not in st.session_state:
    st.session_state.all_recs = []

def get_recommendations(items, categories, context, max_recs=15):
    prompt = f"""
Ты — эксперт по рекомендациям. У пользователя следующие любимые объекты: {items}.
Он хочет рекомендации в категориях: {categories}.
Контекст/настроение/цель: {context}.
Составь список максимум {max_recs} рекомендаций по этим категориям. 
Дай рекомендации в формате: Категория: Название - краткий комментарий.
Не повторяй объекты пользователя.
"""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    text = response.choices[0].message.content
    recs = [line.strip() for line in text.split("\n") if line.strip()]
    return recs

# --- Кнопки ---
if st.button("Получить рекомендации"):
    if user_items.strip() and categories.strip():
        recs = get_recommendations(user_items, categories, context, max_recs)
        st.session_state.all_recs = recs
        st.success(f"Сгенерировано {len(recs)} рекомендаций!")
    else:
        st.warning("Введите хотя бы список объектов и категории!")

if st.session_state.all_recs:
    st.subheader("Ваши рекомендации:")
    for i, rec in enumerate(st.session_state.all_recs, 1):
        st.write(f"{i}. {rec}")

    if st.button("Хочу ещё"):
        more_recs = get_recommendations(user_items, categories, context, max_recs)
        # Добавляем новые рекомендации, уникальные
        st.session_state.all_recs += [r for r in more_recs if r not in st.session_state.all_recs]
        st.experimental_rerun()
