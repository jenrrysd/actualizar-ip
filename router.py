import boto3
import urllib.request
import json
import logging

# Configuración
DOMAIN = 'dva.dextre.xyz.'  # Subdominio que deseas actualizar
# Reemplaza con tu Hosted Zone ID en Route 53
HOSTED_ZONE_ID = 'Z07584812PI7WPI0EX98O'

# Configura el logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Obtén la IP pública actual


def get_public_ip():
    try:
        response = urllib.request.urlopen(
            'https://api.ipify.org?format=json', timeout=5)
        data = json.loads(response.read().decode('utf-8'))
        ip = data.get('ip')
        if not ip:
            raise ValueError("La api no devolio una ip valida")
        print("IP publica obtenida:", ip)
        return ip
        # return ip
    except Exception as e:
        logger.error(f"Error al obtener la IP pública: {str(e)}")
        raise

# Actualiza el registro DNS en Route 53


def update_dns(ip):
    try:
        client = boto3.client('route53')
        response = client.change_resource_record_sets(
            HostedZoneId=HOSTED_ZONE_ID,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': DOMAIN,
                            'Type': 'A',
                            'TTL': 300,
                            'ResourceRecords': [{'Value': ip}]
                        }
                    }
                ]
            }
        )
        logger.info(f'Registro DNS actualizado: {DOMAIN} -> {ip}')
        return response
    except Exception as e:
        logger.error(f'Error al actualizar el DNS: {e}')
        raise

# Función principal de Lambda


def lambda_handler(event, context):
    try:
        new_ip = get_public_ip()
        if not new_ip:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'No se puedo obtener la Ip publica'})
            }

        logger.info(f'IP pública actual: {new_ip}')
        update_dns(new_ip)
        return {
            'statusCode': 200,
            'body': 'DNS actualizado correctamente'
        }
    except Exception as e:
        logger.error(f'Error en la función Lambda: {e}')
        return {
            'statusCode': 500,
            'body': 'Error al actualizar el DNS'
        }


# Bloque para ejecución local (¡IMPORTANTE!)
if __name__ == "__main__":
    print("\n=== Prueba local iniciada ===")
    try:
        ip = get_public_ip()
        print(f"\n✅ IP pública obtenida: {ip}")

        print("\nProbando update_dns()...")
        result = update_dns(ip)
        print(f"✅ DNS actualizado. Response: {result}")

    except Exception as e:
        print(f"\n❌ Error durante la prueba: {str(e)}")
