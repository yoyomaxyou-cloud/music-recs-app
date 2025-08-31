import streamlit as st
import openai

# --- Настройка API ключа ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Функция получения рекомендаций ---
def get_recommendations(items_list, category="Музыка", max_recs=20):
    """
    Получает рекомендации через ChatGPT на основе введенного списка и категории.
    """
    prompt = f"""
Ты эксперт в {category}. 
Вот список интересов пользователя:
{items_list}

Дай {max_recs} рекомендаций, похожих на вышеуказанные, в виде маркированного списка с короткой подписью (название + описание).
Не повторяй элементы из исходного списка.
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content
        # Разделение на пункты, если GPT дал маркированный список
        recs = [line.strip("-• ").strip() for line in text.splitlines() if line.strip()]
        return recs
    except Exception as e:
        st.error(f"Ошибка при генерации рекомендаций: {e}")
        return []

# --- Интерфейс Streamlit ---
st.set_page_config(page_title="Умные Рекомендации", layout="wide")
st.title("🎯 Умные Рекомендации от ИИ")
st.write("Получай персонализированные рекомендации по музыке, фильмам, играм, сериалам и любым интересам!")

# --- Ввод от пользователя ---
category = st.selectbox("Выберите категорию", ["Музыка", "Фильмы", "Сериалы", "Игры", "Книги", "Прочее"])
items_input = st.text_area("Введите список любимых треков, фильмов или игр (через запятую или с новой строки)")

max_recs = st.slider("Сколько рекомендаций показать сразу?", min_value=5, max_value=50, value=15)

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Получить рекомендации") and items_input.strip():
    with st.spinner("Генерируем рекомендации..."):
        recs = get_recommendations(items_input, category, max_recs)
        st.session_state.history = recs
        for r in recs:
            st.markdown(f"- {r}")

if st.button("Хочу ещё") and st.session_state.history:
    with st.spinner("Ищем дополнительные рекомендации..."):
        more_recs = get_recommendations(", ".join(st.session_st_
