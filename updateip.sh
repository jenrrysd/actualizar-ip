#!/bin/bash

# este script actuliza l aip publica de una instancia de EC2
# previamente debe tener la politica añadida a la instancia.
sleep 15
DOMAIN="dva.dextre.xyz."  # ¡Asegúrate del punto final!
HOSTED_ZONE_ID="Z07584812PI7WPI0EX98O"
AWS_REGION="us-east-1"
PUBLIC_IP=$(curl ifconfig.me)

echo "la ip publica es; $PUBLIC_IP"

aws route53 change-resource-record-sets \
    --hosted-zone-id "$HOSTED_ZONE_ID" \
    --region "$AWS_REGION" \
    --change-batch '{
        "Changes": [{
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "'"$DOMAIN"'",
                "Type": "A",
                "TTL": 300,
                "ResourceRecords": [{"Value": "'"$PUBLIC_IP"'"}]
            }
        }]
    }
