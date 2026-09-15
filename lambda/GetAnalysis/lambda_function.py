import boto3
import json
import os


s3 = boto3.client("s3")

BUCKET = os.environ["BUCKET_NAME"]


def lambda_handler(event, context):

    try:

        query = event.get(
            "queryStringParameters"
        ) or {}


        filename = query.get("file")


        if not filename:

            return make_response(
                400,
                {
                    "error":
                        "Missing file parameter"
                }
            )


        filename = filename.split("/")[-1]


        result_key = (
            f"results/{filename}.json"
        )


        s3_response = s3.get_object(
            Bucket=BUCKET,
            Key=result_key
        )


        data = json.loads(
            s3_response["Body"]
            .read()
            .decode("utf-8")
        )


        return make_response(
            200,
            data
        )


    except s3.exceptions.NoSuchKey:

        return make_response(
            404,
            {
                "error":
                    "Analysis not found"
            }
        )


    except Exception as e:

        print(
            f"ERROR TYPE: {type(e).__name__}"
        )

        print(
            f"ERROR DETAILS: {repr(e)}"
        )


        return make_response(
            500,
            {
                "error": str(e)
            }
        )


def make_response(
    status_code,
    body
):

    return {

        "statusCode":
            status_code,

        "headers": {

            "Content-Type":
                "application/json",

            "Access-Control-Allow-Origin":
                "*",

            "Access-Control-Allow-Headers":
                "Content-Type",

            "Access-Control-Allow-Methods":
                "GET,OPTIONS"

        },

        "body":
            json.dumps(body)

    }
