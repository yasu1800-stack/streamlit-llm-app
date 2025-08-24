
import openai
import os
# プロキシ設定
os.environ["HTTP_PROXY"] = "http://10.46.59.30:4221"
os.environ["HTTPS_PROXY"] = "http://10.46.59.30:4221"
os.environ["PYTHONHTTPSVERIFY"] = "0"
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEYが環境変数に設定されていません")

client = openai.OpenAI(api_key=openai_api_key)
response = client.models.list()
print(response)