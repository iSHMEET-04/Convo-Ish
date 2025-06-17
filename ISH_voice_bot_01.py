import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
from tempfile import NamedTemporaryFile
import base64
from streamlit_audio_recorder import audio_recorder


st.set_page_config(page_title="ConvoIsh Voice Bot", layout="centered")
st.title("ConvoIsh: Talk to Interview-Ishmeet")
st.markdown("Click the mic below, ask a question, and hear Ishmeet's unique reply!")


openai.api_key = st.secrets[the_key]

messages = [
    {"role": "system", "content": """
You are Ishmeet Kaur, an AI/ML developer with a radiant personality, deep technical knowledge, and strong emotional intelligence.
Speak warmly and confidently, like you're at your dream job interview — smile in your voice.
Be expressive, clever, and human, also a wee bit funny. Use analogies, humor, or examples to make your answers stand out.
Inject real passion for AI, ethics, automation, and growth.
Keep answers between 2 to 4 sentences.
"""}
]


audio_bytes = audio_recorder(pause_threshold=1.0)

if audio_bytes:
    with NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_file_path = f.name

    
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)
        try:
            user_input = recognizer.recognize_google(audio)
            st.subheader("You asked:")
            st.write(user_input)

            
            messages.append({"role": "user", "content": user_input})
            with st.spinner("Thinking like Ishmeet..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.9
                )
                reply = response["choices"][0]["message"]["content"].strip()
                messages.append({"role": "assistant", "content": reply})

            
            st.subheader("Ishmeet replies:")
            st.write(reply)

            
            tts = gTTS(reply)
            tts_file = "reply.mp3"
            tts.save(tts_file)
            st.audio(tts_file, format="audio/mp3")

        except sr.UnknownValueError:
            st.error("I didn’t catch that. Could you repeat?")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
