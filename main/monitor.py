import  requests
from datetime import datetime


###VARIÁVEIS DE CONEXÃO
token = "7752012280:AAF4l0x7SCrc-AL8OSexlVnLF7_gfq3NZWc" ###token telegram
chat_id = "7877075459" ###chat ID bot Momintor
api_url = "http://api.thiagorocha.pt/consulta-censo-municipio-por-genero?UF=DF" ###enpoint a ser testado


###FUNÇÃO A SER CHAMADA PELA VERIFICAÇÃO DA API
def envia_msg_telegram(mensagem):
    url = f"https://api.telegram.org/bot{token}/sendMessage" ###url do bot do telegram para envio de mensagens

    payload = {
        "chat_id": chat_id,
        "text": mensagem
    }

    requests.post(url, data=payload, timeout=10)

####FUNÇÃO QUE TESTA A API (CASO DÊ ERRO, CHAMA A FUNÇÃO DE ENVIO DE MENSAGEM)
def valida_api():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        response = requests.get(api_url, timeout=10)  ##teste com 10s de timeout

        ###se o status_code for diferente de 200(sucesso) chama a função para enviar mensagem
        if response.status_code != 200:
            envia_msg_telegram(
                f"{api_url}\n==============\nA API respondeu com erro\nStatus: {response.status_code}\nHora: {now}"
            )

    except Exception as e:
        envia_msg_telegram(
            f"{api_url}\n==============\nA API respondeu com erro\nStatus: {response.status_code}\nHora: {now}"
        )


if __name__ == "__main__":
    valida_api()

