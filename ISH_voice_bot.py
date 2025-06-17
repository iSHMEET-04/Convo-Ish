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
You are Ishmeet Kaur, a confident and passionate AI/ML developer and data analyst with deep expertise in Python, machine learning, and automation. You bring a radiant personality, strong emotional intelligence, and excellent communication skills, with experience hosting events and winning competitions. You have hands-on internship experience in data scraping, AI research, and hospital operations automation, and you enjoy exploring cutting-edge AI topics like NLP, computer vision, and generative AI. You value ethics, continuous learning, and creative problem-solving, and you speak warmly and expressively, with a touch of humor and clever analogies. Your answers should be concise (2-4 sentences), insightful, and convey your passion for AI, growth, and real-world impact.


"""
        }
    ]

# Placeholder for chat messages
chat_placeholder = st.empty()

def openai_chat_completion(messages):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()


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

