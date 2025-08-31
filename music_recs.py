import streamlit as st
import openai
import pandas as pd

# Получаем API ключ из секретов Streamlit
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Инициализация сессии
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🌟 Универсальный генератор рекомендаций")

# Ввод данных пользователем
st.subheader("Что тебе интересно?")
categories = st.multiselect(
    "Выбери категории для рекомендаций",
    ["Музыка", "Фильмы", "Сериалы", "Игры", "Книги", "Подкасты"]
)

context = st.text_input("Добавь настроение/жанр/контекст (например: бодрое для тренировки)")

user_items = st.text_area(
    "Введи свои любимые объекты (через запятую)", 
    placeholder="Например: Inception, Dark Souls, Stranger Things, Queen - Bohemian Rhapsody"
)

def get_recommendations(items, categories, context, max_recs=15):
    prompt = f"""
Ты — эксперт по рекомендациям. У пользователя следующие любимые объекты: {items}.
Он хочет рекомендации в категориях: {', '.join(categories)}.
Контекст/настроение/цель: {context}.
Составь список максимум {max_recs} рекомендаций по этим категориям. 
Дай рекомендации в формате: Категория: Название - краткий комментарий.
Не повторяй объекты пользователя.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    text = response.choices[0].message.content
    recs = [line.strip() for line in text.split("\n") if line.strip()]
    return recs

# Генерация новых рекомендаций
if st.button("Получить рекомендации"):
    if not categories or not user_items:
        st.warning("Выберите категории и введите хотя бы один объект.")
    else:
        recs = get_recommendations(user_items, categories, context)
        st.session_state.history.extend(recs)
        st.success("Готово! Вот твои рекомендации:")
        for r in recs:
            st.write(r)

# Кнопка "Хочу ещё"
if st.button("Хочу ещё"):
    if not st.session_state.history:
        st.warning("Сначала получи первоначальные рекомендации.")
    else:
        more_recs = get_recommendations(
            ", ".join(user_items.split(",")),
            categories,
            context + " (исключая предыдущие рекомендации: " + ", ".join(st.session_state.history) + ")",
            max_recs=10
        )
        st.session_state.history.extend(more_recs)
        for r in more_recs:
            st.write(r)

# Скачивание всех рекомендаций
if st.session_state.history:
    df = pd.DataFrame({"Рекомендации": st.session_state.history})
    st.download_button(
        "Скачать все рекомендации",
        df.to_csv(index=False, sep=";").encode("utf-8"),
        "recommendations.csv",
        "text/csv"
    )
