import requests
import json
import boto3


def lambda_handler(event, context):
    result = json.loads(json.dumps(event))
    body_dic = json.loads(result['body'])
    orderid = body_dic['OrderId']
    url = f"https://travellog.myvtex.com/api/oms/pvt/orders/{orderid}?_stats=1"
    headers = {
        'X-VTEX-API-AppKey': 'vtexappkey-travellog-MWLBRW',
        'X-VTEX-API-AppToken': 'JMBJMGEKUOPFVKKVWJNKEZDRBWJIRSOGIMYZCQDGTCHTLLCVQWPFOXKDNFMJSUJHOQZBOFJBVBHCHZVWSIMAADKEJZJYBZQGWZYVDMZXAEJKMUWOUYFVLSVKEFXWIZQV',
    }

    response = requests.request("GET", url, headers=headers)
    result = json.loads(response.text)
    id_user = result['clientProfileData']['userProfileId']
    value = int(result['value']/100)
    client = boto3.resource("dynamodb")
    table = client.Table("ponto_buyer")

    respo = table.get_item(Key={"id": id_user})
    
    if respo.get("Item") == None:

        table.put_item(
            Item={
                "id": id_user,
                "value_points": [value],
            }
        )

    else:
        idVal = [value]
        table.update_item(
            Key={'id': id_user},
            ExpressionAttributeNames={'#value_points': 'value_points'},
            ExpressionAttributeValues={':idVal': idVal},
            UpdateExpression="SET #value_points = list_append(value_points , :idVal)",
        )
