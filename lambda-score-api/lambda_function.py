import boto3
import json
from custom_encorder import CustomEncoder

dynamodbTableName = "ponto_buyer"
dynamo = boto3.resource("dynamodb")
table = dynamo.Table(dynamodbTableName)

getMehod = "GET"
pathMethod = "PATCH"
deleteMethod = "DELETE"
scorePath = "/score"


def lambda_handler(event, context):
    httpMethod = event["httpMethod"]
    path = event["path"]

    if httpMethod == getMehod and path == scorePath:

        response = getScore(event["queryStringParameters"]["id"])

    elif httpMethod == pathMethod and path == scorePath:

        requestBody = json.loads(event["body"])
        response = modifyScore(requestBody["id"], requestBody["updateValue"])

    elif httpMethod == deleteMethod and path == scorePath:

        requestBody = json.loads(event["body"])
        response = deleteUser(requestBody["id"])

    else:
        response = buildResponse(404, "Not found Endpoint")

    return response


def somar_elementos(lista):
    soma = 0
    for numero in lista:
        soma += numero
    return soma


def getScore(id):
    try:
        response = table.get_item(Key={"id": id})
        if "Item" in response:
            dic = response["Item"]
            soma = somar_elementos(response["Item"]["value_points"])
            dic['soma'] = soma

            return buildResponse(200, dic)
        else:
            return buildResponse(404, {f"Message": "Id: not found {id}!!"})
    except:
        print("Erro GET")


def modifyScore(id_user, updateValue):
    try:
        idVal = [updateValue]
        response = table.update_item(
            Key={"id": id_user},
            ExpressionAttributeNames={"#value_points": "value_points"},
            ExpressionAttributeValues={":idVal": idVal},
            UpdateExpression="SET #value_points = list_append(value_points , :idVal)",
            ReturnValues="UPDATED_NEW",
        )
        body = {
            "Operation": "UPDATE",
            "Message": "SUCCESS",
            "UpdatedAttrebutes": response,
        }
        # body={response["Attributes"]}
        return buildResponse(200, body)

    except:
        print("Erro modify!")


def deleteUser(id_user):
    try:
        response = table.delete_item(
            Key={"id": id_user}, ReturnValues="ALL_OLD")
        body = {"Operation": "DELETE",
                "Message": "SUCCESS", "deletedItem": response}
        return buildResponse(200, body)
    except:
        print("Erro delete!!!")


def buildResponse(statusCode, body=None):
    response = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    if body is not None:
        response["body"] = json.dumps(body, cls=CustomEncoder)
    return response
