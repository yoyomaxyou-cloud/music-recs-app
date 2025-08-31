import streamlit as st
from openai import OpenAI

# Клиент OpenAI, ключ берём из Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_recommendations(track_list, max_recs=50):
    """
    Получает рекомендации на основе списка треков.
    track_list: строка с треками, по одному на строку
    max_recs: количество рекомендаций
    """
    prompt = f"""У меня есть список моих любимых треков:
{track_list}

Предложи {max_recs} новых треков, которые мне могут понравиться. 
Выводи каждый трек с новой строки, формат: Исполнитель - Название трека"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )
    
    recommendations = response.choices[0].message.content.strip()
    return recommendations

# --- Streamlit UI ---
st.title("🎵 Музыкальные рекомендации на основе твоих треков")
st.write("Вставь список любимых треков (по одному на строку).")

user_tracks = st.text_area("Твои треки", height=200, placeholder="Например:\nEminem - Lose Yourself\nThe Weeknd - Blinding Lights\n...")
max_recs = st.slider("Сколько рекомендаций показывать?", 10, 100, 50)

if st.button("Получить рекомендации"):
    if user_tracks.strip() == "":
        st.warning("Сначала введи список треков!")
    else:
        recs = get_recommendations(user_tracks, max_recs=max_recs)
        st.subheader("✨ Вот, что тебе может понравиться:")
        st.text(recs)

        if st.button("Хочу ещё"):
            user_tracks += "\n" + recs
            recs_more = get_recommendations(user_tracks, max_recs=max_recs)
            st.subheader("🎶 Дополнительные рекомендации:")
            st.text(recs_more)
