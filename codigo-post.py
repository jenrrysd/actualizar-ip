import urllib.request
import json

# Obtén la IP pública del router


def get_public_ip():
    try:
        with urllib.request.urlopen('https://api.ipify.org?format=json') as response:
            data = json.loads(response.read().decode('utf-8'))
            return data['ip']
    except Exception as e:
        print(f'Error al obtener la IP pública: {e}')
        return None

# Envía la IP pública al API Gateway


def send_ip_to_lambda(ip):
    # Reemplaza con tu URL de API Gateway
    api_url = 'https://j8kgv7gd8k.execute-api.us-east-1.amazonaws.com/prod/update-ip'
    payload = json.dumps({'ip': ip}).encode('utf-8')
    headers = {'Content-Type': 'application/json'}

    try:
        req = urllib.request.Request(
            api_url, data=payload, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            print(f'Respuesta del API Gateway: {response.read().decode()}')
    except Exception as e:
        print(f'Error al enviar la IP al API Gateway: {e}')


# Ejecuta el script
if __name__ == '__main__':
    public_ip = get_public_ip()
    if public_ip:
        print(f'IP pública obtenida: {public_ip}')
        send_ip_to_lambda(public_ip)
