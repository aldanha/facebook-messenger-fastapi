from fastapi import FastAPI, Request, Response, HTTPException
import requests
import uvicorn


app = FastAPI()


#token for webhook callback
FB_VERIFY_TOKEN= "fbtoken"

#token for facebook page
YOUR_ACCESS_TOKEN = "EAAOVavafXL8BOZCJ3skyemhEluPlCFNoa2MKxQUaAQnmIbhWjKbHhmwkfhPu0xOBfZAN6aZA0wVjY4fH5BTVHrjtzQymQN0cTslS7NLt0ArkePXPsltw5E3YnJs0pb7zTTYFvCD1Ba26oAZAH0UJmDfrx3m7jma1P47G2HVarRvrcFfpVNDj467w8L0gfl6c"

#webhook for handling get method
@app.get('/webhook')
def init_messenger(request: Request):
    # FB sends the verify token as hub.verify_token
    fb_token = request.query_params.get("hub.verify_token")

    # we verify if the token sent matches our verify token
    if fb_token == FB_VERIFY_TOKEN:
        # respond with hub.challenge parameter from the request.
        return Response(content=request.query_params["hub.challenge"])
    return 'Failed to verify token'

#send message endpoint
FB_MESSENGER_API = "https://graph.facebook.com/v18.0/me/messages?access_token="+YOUR_ACCESS_TOKEN


#webhook for handling post method
@app.post("/webhook")
async def fbwebhook(data: dict):
    try:
        message = data['entry'][0]['messaging'][0]['message']
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']

        if message['text'] == "hi":
            request_body = {
                "recipient": {
                    "id": sender_id
                },
                "message": {
                    "text": "hello, world!"
                }
            }
            response = requests.post(FB_MESSENGER_API, json=request_body).json()
            return response
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid request data") from e

if __name__ == "__main__":
    uvicorn.run("app:app", log_config=None, debug=True, reload=True)



#Steps

#Create a facebook page
#Create a facebook messenger app
#Create FASTApi Webhook
#Add Subscription/permission to the app
#Generate page access token
#Create ngrok agent to handle callback
#Set callback and token setting in the app
