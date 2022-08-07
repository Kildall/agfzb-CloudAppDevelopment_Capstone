from ibmcloudant.cloudant_v1 import CloudantV1, IndexDefinition, IndexField
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import requests


def main(dict):
    databaseName = "reviews"

    try:
        authenticator = IAMAuthenticator(dict.get("IAM_API_KEY"))
        cloudant = CloudantV1(authenticator=authenticator)
        cloudant.set_service_url(dict.get("COUCH_URL"))
        review = dict.get("review")
        response = cloudant.post_document(
            db=databaseName,
            document=review
        ).get_result()

    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"response": response}