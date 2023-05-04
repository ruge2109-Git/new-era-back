from flask import Flask, request
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

openai.api_key = os.getenv("OPENAI_ID")

if not openai.api_key:
    raise ValueError("No se encontró ninguna clave de API de OpenAI. Configure la variable de entorno OPENAI_ID.")


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/translate', methods=['POST'])
def translate():
    text = request.json['text']
    language = request.json['language']
    if not text or not language:
        return {"error": "Se requieren ambas claves 'text' y 'language' en la carga útil de la solicitud."}, 400
    return {"text": translate_text(text, language)}


def translate_text(text, target_language):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Translate the following text to {target_language}: '{text}'\n",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


if __name__ == '__main__':
    app.run(debug=True)
