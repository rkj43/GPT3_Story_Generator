from flask import Flask, send_file, jsonify, request
import openai, requests
from PIL import Image
import io
import base64
import json

app = Flask(__name__)

@app.route("/")
def index():
    return send_file("index.html")

@app.route('/generate-story', methods=['GET'])
def generate_story():
    openai.api_key = "sk-NOT_MY_KEY" 
    # this is not my key, get your API key from https://openai.com/api/

    

    # Use the OpenAI API to generate a story
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Short Anime Story",
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )

    # Extract the generated story from the response
    story = response.choices[0].text

    # Use the OpenAI API to generate a story
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="One line summary of :" + story,
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )

    # Use the OpenAI API to generate a summary for image prompt
    summary = response.choices[0].text


    # Use DALL-E 2 to generate the image
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer "+ openai.api_key
    }
    data = {
        "model": "image-alpha-001",
        "prompt": summary,
        "num_images":1,
        "size":"1024x1024"
    }
    resp = requests.post(url, headers=headers, json=data)
    image_url = json.loads(resp.text)['data'][0]['url']
    # Encode the image as a base64 string
    image_base64 = base64.b64encode(requests.get(image_url).content).decode()
    # Return the story and the image as a JSON object
    return jsonify(story=story, image=f"data:image/png;base64,{image_base64}")
   

