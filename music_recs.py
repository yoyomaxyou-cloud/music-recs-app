import streamlit as st
from openai import OpenAI

# Создаём клиента OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Функция для получения универсальных рекомендаций
def get_recommendations(category, items, max_recs=10):
    prompt = f"""
    У меня есть список любимых {category}:
    {items}

    На основе этого списка предложи {max_recs} похожих {category}. 
    Форматируй вывод нумерованным списком, по возможности с краткой подсказкой о каждом.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )
    return response.choices[0].message.content

# Заголовок приложения
st.title("🎯 Универсальный AI-рекомендатор")

# Выбор категории
category = st.selectbox(
    "Что ты хочешь получить рекомендации по?",
    ["Музыка", "Фильмы", "Сериалы", "Игры", "Книги", "Подкасты", "Аниме", "Прочее"]
)

# Поле для ввода списка любимых объектов
items = st.text_area(f"Вставь список твоих любимых {category.lower()}:")

# Инициализация session_state
if "recs" not in st.session_state:
    st.session_state.recs = []

# Кнопка "Сгенерировать рекомендации"
if st.button("Сгенерировать рекомендации"):
    if items.strip():
        recs = get_recommendations(category, items, max_recs=15)
        st.session_state.recs = [recs]  # заменяем старые рекомендации
    else:
        st.warning(f"Пожалуйста, вставь хотя бы один {category.lower()}!")

# Кнопка "Хочу ещё"
if st.button("Хочу ещё"):
    if items.strip():
        more_recs = get_recommendations(category, items, max_recs=15)
        st.session_state.recs.append(more_recs)  # добавляем новые рекомендации
    else:
        st.warning(f"Сначала вставь список {category.lower()} и нажми 'Сгенерировать'")

# Отображение всех списков рекомендаций
for i, block in enumerate(st.session_state.recs, 1):
    st.subheader(f"Рекомендации #{i}")
    st.write(block)
