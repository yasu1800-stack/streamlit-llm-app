import os
# プロキシ設定
#os.environ["HTTP_PROXY"] = "http://10.46.59.30:4221"
#os.environ["HTTPS_PROXY"] = "http://10.46.59.30:4221"
#os.environ["PYTHONHTTPSVERIFY"] = "0"
import streamlit as st
from dotenv import load_dotenv
import os

# LangChain最新版のインポートパス
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# .envファイルから環境変数をロード
load_dotenv()

st.title("専門家AIに質問しよう！")

st.write("""
このWebアプリは、あなたの質問に対してAIが専門家として回答します。  
画面下部のラジオボタンで「専門家の種類」を選び、質問を入力して送信してください。  
AIは選択した専門家の立場から回答します。
""")

# 専門家の種類（例。自由に追加や変更OK）
experts = {
    "医療専門家": "あなたは医療分野の専門家です。専門的かつ分かりやすい解説をしてください。",
    "法律専門家": "あなたは法律分野の専門家です。分かりやすく法的観点から説明してください。",
    "ITエンジニア": "あなたはIT分野の専門家です。技術的に正確で分かりやすく説明してください。",
    "教育者": "あなたは教育分野の専門家です。初心者にも分かるように優しく説明してください。"
}

# ラジオボタンで専門家を選択
selected_expert = st.radio(
    "専門家の種類を選んでください", 
    list(experts.keys())
)

# 入力フォーム
user_input = st.text_input("質問を入力してください")

def get_llm_response(user_text, expert_type):
#    api_key = os.getenv("OPENAI_API_KEY")
    api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key:
        return "OpenAI APIキーが設定されていません。"
    
    system_message = experts[expert_type]
    
    # LLM呼び出し（LangChain最新版準拠）
    chat = ChatOpenAI(
        openai_api_key=api_key,
        model_name="gpt-4o-mini",  # 必要に応じてgpt-4などに変更可能
        temperature=0.7
    )
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_text)
    ]
    response = chat.invoke(messages)
    return response.content

if st.button("送信"):
    if user_input:
        with st.spinner("AIが考え中..."):
            answer = get_llm_response(user_input, selected_expert)
        st.subheader("AIからの回答")
        st.write(answer)
    else:
        st.warning("質問を入力してください。")