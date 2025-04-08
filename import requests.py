import urllib.request
import json
import boto3

region = 'us-east-1'

# Obtén la IP pública del router


def get_public_ip():
    try:
        with urllib.request.urlopen('https://api.ipify.org?format=json') as response:
            data = json.loads(response.read().decode('utf-8'))
            print(data)
            return data['ip']
    except Exception as e:
        print(f'Error al obtener la IP pública: {e}')
        return None

# Envía la IP pública a la función Lambda


def send_ip_to_lambda(ip):
    lambda_client = boto3.client('lambda', region_name=region)
    response = lambda_client.invoke(
        FunctionName='Update-DNS',
        InvocationType='RequestResponse',
        Payload=json.dumps({'ip': ip})
    )
    return response


# Ejecuta el script
if __name__ == '__main__':
    public_ip = get_public_ip()
    if public_ip:
        send_ip_to_lambda(public_ip)
