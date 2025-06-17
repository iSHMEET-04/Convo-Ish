import streamlit as st
import av
import numpy as np
import openai
from streamlit_webrtc import webrtc_streamer, WebRtcMode


openai.api_key = st.secrets["the_key"]

st.title("ConvoIsh: AI Interview Twin with Voice")


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
You are Ishmeet Kaur, an AI/ML developer with a radiant personality, deep technical knowledge, and strong emotional intelligence.
Speak warmly and confidently, like you're at your dream job interview — smile in your voice.
Be expressive, clever, and human, also a wee bit funny. Use analogies, humor, or examples to make your answers stand out.
Inject real passion for AI, ethics, automation, and growth.
Keep answers between 2 to 4 sentences.
"""
        }
    ]

# Placeholder for chat messages
chat_placeholder = st.empty()

def openai_chat_completion(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.9,
    )
    return response['choices'][0]['message']['content'].strip()

# Audio processing callback (dummy, just passes audio through)


def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    return frame



webrtc_ctx = webrtc_streamer(
    key="voice-bot",
    mode=WebRtcMode.SENDRECV,
    audio_frame_callback=audio_frame_callback,
    media_stream_constraints={"audio": True, "video": False},
)

if webrtc_ctx.audio_receiver:
    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
    if audio_frames:
        pass


user_text = st.text_input("Or type your question here:")



if user_text:
    
    st.session_state.messages.append({"role": "user", "content": user_text})


    with st.spinner("ConvoIsh is thinking..."):
        reply = openai_chat_completion(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": reply})

    
    chat_placeholder.markdown("### Conversation:")
    for msg in st.session_state.messages[1:]:
        role = "You" if msg["role"] == "user" else "ConvoIsh"
        st.markdown(f"**{role}:** {msg['content']}")

