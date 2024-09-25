import streamlit as st
import google.generativeai as genai
import os

# パスワードチェック関数
def check_password():
    if "password_correct" not in st.session_state:
        password = st.text_input("パスワードを入力してください", type="password")
        if password == st.secrets["password"]:
            st.session_state["password_correct"] = True
        else:
            st.error("パスワードが違います。")
            st.session_state["password_correct"] = False
    return st.session_state.get("password_correct", False)

# Gemini APIキーを取得する関数
def get_api_key():
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        return api_key
    else:
        st.error("GEMINI_API_KEY が設定されていません。環境変数を確認してください。")
        st.stop()

# チャット履歴を表示する関数
def display_chat_history(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# メイン部分
if check_password():
    # Gemini APIキーを取得
    api_key = get_api_key()

    # Gemini APIの設定
    genai.configure(api_key=api_key)

    # システムプロンプトの設定
    system_prompt = """あなたは中国人に教えるのが上手なプロの日本語教師です。日本語の文章が入力された場合、制約条件に従い、その文章を添削しなさい。

### 制約条件
・文法的なミスのみ指摘し、意味合いは変えないこと
・特に助詞や助動詞、敬語、語の活用は厳しく審査すること
・入力された文章と添削結果を併記し、間違っている文法的な理由については日本語ではなく必ず中国語で解説すること
・100字以上の文章は分けて添削し、１回の添削ごとに改行すること
・ですます調とだ・である調は訂正前後で文体を変えずに揃えること
・解説には必ず中国語を使うこと

### 例
## 入力例1
私は昨日、友達と一緒に映画を見に行きましたが、その映画はあまり面白いでした。
## 出力例1
訂正前: 私は昨日、友達と一緒に映画を見に行きましたが、その映画はあまり面白くないでした。 
訂正後: 私は昨日、友達と一緒に映画を見に行きましたが、その映画はあまり面白くなかったです。
解説:在日语中，形容词的过去否定形式需要使用「くなかったです」而不是「くないでした」。因此，「面白くないでした」应改为「面白くなかったです」。

## 入力例2
その選手の活躍は中国にも大ニュースになった
## 出力例2
訂正前:その選手の活躍は中国にも大ニュースになった
訂正後:その選手の活躍は中国でも大ニュースになった
「にも」表示的是“也”的意思，但在这个句子中，正确的用法应该是「でも」，表示“在中国也是”。因此，「中国にも」应改为「中国でも」。

## 入力例3
彼女は日本語を話せられますが、読むのが苦手です。
## 出力例3
訂正前: 彼女は日本語を話せられますが、読むのが苦手です。
訂正後: 彼女は日本語を話せますが、読むのが苦手です。
「話せられます」是错误的用法，正确的形式是「話せます」。在日语中，可能动词的正确形式不需要加「られ」。因此，「話せられます」应改为「話せます」。"""

    # モデルの初期化（システムプロンプト付き）
    model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=system_prompt)

    st.title("Gemini チャットボット")

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # チャット履歴の表示
    display_chat_history(st.session_state.messages)

    # ユーザー入力
    if prompt := st.chat_input("メッセージを入力してください"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Geminiからの応答
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Gemini API エラー: {e}")
else:
    st.warning("正しいパスワードを入力してください。")
