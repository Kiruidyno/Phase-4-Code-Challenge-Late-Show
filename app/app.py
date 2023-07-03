from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "DELETE"], allow_headers=["Content-Type"])

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def home():
    return ''

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify({
        'episodes': [episode.to_dict() for episode in episodes]
    })

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if episode is None:
        return jsonify({'error': 'Episode not found'})
    return jsonify({
        'episode': episode.to_dict()
    })

@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get(id)
    if episode is None:
        return jsonify({'error': 'Episode not found'})
    episode.delete()
    return '', 204

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify({
        'guests': [guest.to_dict() for guest in guests]
    })

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    rating = data['rating']
    episode_id = data['episode_id']
    guest_id = data['guest_id']
    appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)
    db.session.add(appearance)
    db.session.commit()
    return jsonify({
        'appearance': appearance.to_dict()
    })

if __name__ == '__main__':
    app.run(port=5555)

