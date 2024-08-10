from flask import Flask, request, jsonify, send_from_directory, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/getProfilePicture', methods=['GET'])
def get_profile_picture():
    username = request.args.get('username')
    if not username:
        return jsonify({'imageUrl': None, 'message': 'Username parameter is missing.'})

    url = f"https://instagram.com/{username}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.text, 'html.parser')
        image_tag = soup.find('meta', property='og:image')

        if image_tag:
            return jsonify({'imageUrl': image_tag['content']})
        else:
            return jsonify({'imageUrl': None, 'message': 'Profile picture not found or user is private.'})
    except requests.RequestException as e:
        return jsonify({'imageUrl': None, 'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
