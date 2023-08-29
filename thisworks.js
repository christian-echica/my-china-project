exports.handler = async function (event, context) {
    return {
      "isBase64Encoded": false, 
      "statusCode": 200,
      "statusDescription": "200 OK",
      "headers": {
        "Set-cookie": "cookies",
        "Content-type": "application/json"
      },
      "body": JSON.stringify('This is Lambda function is behind the ALB')
    }
  }
  