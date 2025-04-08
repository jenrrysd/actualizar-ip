import json
import boto3


def lambda_handler(event, context):
    print(json.dumps(event))
    # Obtén la IP pública del cuerpo de la solicitud HTTP
    try:
        body = json.loads(event['body'])
        public_ip = body.get('ip')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': 'No se proporcionó una IP pública en el cuerpo de la solicitud'
        }

    # Configuración de Route 53
    hosted_zone_id = 'Z07584812PI7WPI0EX98O'  # Reemplaza con tu Hosted Zone ID
    domain_name = 'router.dextre.xyz'     # Reemplaza con tu nombre de dominio

    # Actualiza el registro DNS en Route 53
    try:
        client = boto3.client('route53')
        response = client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': 'A',
                            'TTL': 300,
                            'ResourceRecords': [{'Value': public_ip}]
                        }
                    }
                ]
            }
        )
        return {
            'statusCode': 200,
            'body': f'Registro DNS actualizado correctamente: {domain_name} -> {public_ip}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al actualizar el DNS: {str(e)}'
        }
