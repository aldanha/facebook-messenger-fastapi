from fastapi import FastAPI, Request, Response, HTTPException
import requests
import uvicorn


app = FastAPI()



FB_VERIFY_TOKEN= ""


YOUR_ACCESS_TOKEN = ""


@app.get('/webhook')
def init_messenger(request: Request):
    fb_token = request.query_params.get("hub.verify_token")
    if fb_token == FB_VERIFY_TOKEN:
        return Response(content=request.query_params["hub.challenge"])
    return 'Failed to verify token'


FB_MESSENGER_API = "https://graph.facebook.com/v18.0/me/messages?access_token="+YOUR_ACCESS_TOKEN



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




