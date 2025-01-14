from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Get the Hugging Face API key from the environment variables
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"}

# Get the upload folder path from the environment variables
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')  # Default to 'static/uploads' if not set
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Function to query the API and get the caption
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    result = response.json()

    # Handle the response: the result will be a list with a dictionary inside
    if isinstance(result, list) and len(result) > 0:
        return result[0].get('generated_text', 'No caption found.')
    return 'No caption found.'


# Route to display the upload form and handle image upload
@app.route('/', methods=['GET', 'POST'])
def index():
    caption = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            # Save the uploaded file to the 'static/uploads' folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Query the API and get the caption
            caption = query(filepath)

    return render_template('index.html', caption=caption)


if __name__ == '__main__':
    app.run(debug=True)
