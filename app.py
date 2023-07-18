from flask import Flask, render_template, request
from datetime import datetime

import openai
import json
import os



openai.api_key = ""

f=open("onepager_developer.txt", "r")
onepager_developer=f.read()
f.close()



def chatbot_response(question):
    input_data=[
    {"role": "system", "content" : str("You are a chatbot on codespheres website.You need to compare codesphere with alternatives in 3 short bullet points. With the following context:\n"+onepager_developer)},
    {"role": "user", "content" : "How are you?"},
    {"role": "assistant", "content" : "I am doing well"},
    {"role":"user", "content": str(question)}]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages = input_data
    )

    response_gpt=json.loads(str(completion))
    data=response_gpt["choices"][0]
    reason_to_stop=data["finish_reason"]

    if reason_to_stop == "stop":
        response=data["message"]["content"]
        response=response.replace("\n", "<br>")
    else:
        response="An Error occured."


    return response



app = Flask(__name__)
app.static_folder = 'static'
@app.route("/")
def home():
    now=datetime.now()
    time=now.strftime("%H:%M")
    return render_template("index.html", time=time)


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


if __name__ == "__main__":
    port=int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)