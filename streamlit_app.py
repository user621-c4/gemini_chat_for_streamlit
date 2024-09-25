import streamlit as st
import google.generativeai as genai
import os

# Gemini APIキーを環境変数から取得
api_key = os.environ.get('GEMINI_API_KEY')

# Gemini APIの設定
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("GEMINI_API_KEY が設定されていません。環境変数を確認してください。")
    st.stop()

# システムプロンプトの設定
system_prompt = "あなたは親切で丁寧な日本語アシスタントです。ユーザーの質問に対して、簡潔かつ正確に回答してください。"

# モデルの初期化（システムプロンプト付き）
model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=system_prompt)

st.title("Gemini チャットボット")

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# チャット履歴の表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("メッセージを入力してください"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Geminiからの応答
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})# モデルの初期化（システムプロンプト付き）
model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=system_prompt)

