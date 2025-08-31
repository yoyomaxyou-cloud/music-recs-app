import streamlit as st
from openai import OpenAI

# Создаём клиента OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Функция для получения рекомендаций
def get_recommendations(tracks, max_recs=10):
    prompt = f"""
    У меня есть список любимых треков:
    {tracks}

    На основе этого списка порекомендуй {max_recs} похожих треков. 
    Форматируй список нумерованно.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )
    return response.choices[0].message.content

# Заголовок приложения
st.title("🎶 AI Музыкальные рекомендации")

# Поле для ввода треков
tracks = st.text_area("Вставь свой список любимых треков:")

# Инициализация session_state
if "recs" not in st.session_state:
    st.session_state.recs = []

# Кнопка "Сгенерировать"
if st.button("Сгенерировать рекомендации"):
    if tracks.strip():
        recs = get_recommendations(tracks, max_recs=15)
        st.session_state.recs = [recs]  # заменяем старые рекомендации на новые
    else:
        st.warning("Пожалуйста, вставь хотя бы один трек!")

# Кнопка "Хочу ещё"
if st.button("Хочу ещё"):
    if tracks.strip():
        more_recs = get_recommendations(tracks, max_recs=15)
        st.session_state.recs.append(more_recs)  # добавляем новые рекомендации
    else:
        st.warning("Сначала вставь список треков и нажми 'Сгенерировать'")

# Отображение всех списков рекомендаций
for i, block in enumerate(st.session_state.recs, 1):
    st.subheader(f"Рекомендации #{i}")
    st.write(block)

