import os
import streamlit as st
from dotenv import load_dotenv
import requests
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# .envファイルから環境変数をロード（ローカル環境用）
load_dotenv()

# ログ出力関数
def log_message(message):
    """ログをStreamlitの画面に出力する"""
    st.write(message)

# ローカル環境でプロキシを設定
if "OPENAI_API_KEY" not in st.secrets:  # Streamlit環境ではst.secretsが存在するため、これを利用して判断
    os.environ["HTTP_PROXY"] = " http://10.46.59.30:4221 ".strip()  # スペースを削除
    os.environ["HTTPS_PROXY"] = " http://10.46.59.30:4221 ".strip()  # スペースを削除
    os.environ["PYTHONHTTPSVERIFY"] = "0"  # SSL証明書検証を無効化（必要な場合のみ）
    log_message(f"HTTP_PROXY: {os.environ.get('HTTP_PROXY')}")
    log_message(f"HTTPS_PROXY: {os.environ.get('HTTPS_PROXY')}")
    log_message("プロキシ設定を適用しました")

# APIキーを取得する関数
def get_api_key():
    """APIキーを取得し、ログに出力"""
    if "OPENAI_API_KEY" in st.secrets:  # Streamlit環境
        api_key = st.secrets["OPENAI_API_KEY"]
        log_message("Streamlit環境でAPIキーを取得しました")
    elif "OPENAI_API_KEY" in os.environ:  # ローカル環境
        api_key = os.getenv("OPENAI_API_KEY")
        log_message("ローカル環境でAPIキーを取得しました")
    else:
        log_message("APIキーが設定されていません")
        return None
    log_message(f"取得したAPIキー: {api_key[:6]}******（一部非表示）")
    return api_key

# 接続確認（Pingテスト）
def check_connection():
    """OpenAIのAPIエンドポイントにPingを送信して接続確認"""
    api_url = " https://api.openai.com/v1/models ".strip()  # エンドポイントのスペースを削除
    api_key = get_api_key()  # APIキーを取得

    if not api_key:
        log_message("APIキーが設定されていません。.envファイルやStreamlitシークレットにAPIキーを設定してください。")
        return

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        log_message(f"現在のHTTP_PROXY: {os.environ.get('HTTP_PROXY')}")
        log_message(f"現在のHTTPS_PROXY: {os.environ.get('HTTPS_PROXY')}")
        log_message(f"現在のエンドポイント: {api_url}")
        log_message("OpenAI APIエンドポイントへの接続を確認中...")

        # HTTP GETリクエストを送信
        response = requests.get(api_url, headers=headers, timeout=10)

        # ステータスコードの確認
        if response.status_code == 200:
            log_message("OpenAI APIエンドポイントへの接続に成功しました")
            log_message(f"レスポンス内容: {response.json()}")
        elif response.status_code == 401:
            log_message("認証に失敗しました。APIキーが正しいか確認してください。")
        elif response.status_code == 404:
            log_message("エンドポイントが見つかりません。エンドポイントURLを確認してください。")
        else:
            log_message(f"OpenAI APIエンドポイントへの接続に失敗しました。ステータスコード: {response.status_code}")
    except requests.exceptions.RequestException as e:
        log_message(f"OpenAI APIエンドポイントへの接続エラー: {str(e)}")

# LLM呼び出し関数
def get_llm_response(user_text, expert_type):
    """OpenAIのLLMにリクエストを送信し、ログを出力"""
    api_key = get_api_key()  # APIキーを取得
    if not api_key:
        return "OpenAI APIキーが設定されていません。"

    # 接続確認
    check_connection()

    system_message = experts[expert_type]
    
    # LLM呼び出し（LangChain最新版準拠）
    chat = ChatOpenAI(
        openai_api_key=api_key,
        model_name="gpt-4",  # 必要に応じてgpt-4などに変更可能
        temperature=0.7,
        request_timeout=30  # タイムアウトを30秒に設定
    )
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_text)
    ]
    try:
        response = chat.invoke(messages)
        log_message("LLMへのリクエストが成功しました")
        return response.content
    except Exception as e:
        log_message(f"LLMへのリクエストでエラーが発生しました: {str(e)}")
        return f"エラーが発生しました: {str(e)}"

# StreamlitアプリのUI部分
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

# アプリ起動時に接続確認を実行
st.subheader("接続確認")
check_connection()

# ラジオボタンで専門家を選択
selected_expert = st.radio(
    "専門家の種類を選んでください", 
    list(experts.keys())
)

# 入力フォーム
user_input = st.text_input("質問を入力してください")

# ボタンの動作
if st.button("送信"):
    if user_input:
        with st.spinner("AIが考え中..."):
            answer = get_llm_response(user_input, selected_expert)
        st.subheader("AIからの回答")
        st.write(answer)
    else:
        st.warning("質問を入力してください。")