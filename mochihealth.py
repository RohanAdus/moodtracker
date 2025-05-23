# 1) Install ngrok + auth it
!pip install pyngrok
from pyngrok import ngrok

# replace with your real token from https://dashboard.ngrok.com/get-started/your-authtoken
ngrok.set_auth_token("2xVhcqimbGsjuSGTJ1gXPj1tJH3_4k7GjNFej7ZrQFJfB9db7")

# 2) Launch your app
get_ipython().system_raw("streamlit run app.py &")


# kills every tunnel in this session
ngrok.kill()

public_url = ngrok.connect(8501, bind_tls=True)
print("🔗 Streamlit public URL:", public_url)
