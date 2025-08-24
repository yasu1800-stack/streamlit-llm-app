import os
import requests
from dotenv import load_dotenv

# .envファイルから環境変数をロード（ローカル環境用）
load_dotenv()

# プロキシ設定（スペースを削除）
os.environ["HTTP_PROXY"] = " http://10.46.59.30:4221 ".strip()
os.environ["HTTPS_PROXY"] = " http://10.46.59.30:4221 ".strip()
os.environ["PYTHONHTTPSVERIFY"] = "0"  # SSL証明書検証を無効化（必要な場合のみ）

def log_message(message):
    """ログを出力"""
    print(message)

def check_connection():
    """OpenAIのAPIエンドポイントにPingを送信して接続確認"""
    api_url = " https://api.openai.com/v1/models ".strip()  # エンドポイントのスペースを削除
    api_key = os.getenv("OPENAI_API_KEY")  # .envファイルからAPIキーを取得

    if not api_key:
        log_message("APIキーが設定されていません。.envファイルにOPENAI_API_KEYを設定してください。")
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

if __name__ == "__main__":
    log_message("プロキシ設定を適用しました")
    check_connection()