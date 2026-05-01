from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os
from database.loader import get_decks_for_level, get_words_for_deck
from database.db_handler import get_words_by_deck, toggle_mark_status

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nihongo_key_123'
# socketio handles the bidirectional voice communication
socketio = SocketIO(app, cors_allowed_origins="*")

# --- NAVIGATION ROUTES ---

@app.route('/')
def index():
    """Main Menu: JLPT 1-5, Sandbox, Store, Database"""
    return render_template('menu.html')

@app.route('/level/<jlpt_level>')
def level_menu(jlpt_level):
    """Shows the sliced decks (20 words each) for a specific level"""
    decks = get_decks_for_level(jlpt_level)
    return render_template('level_select.html', level=jlpt_level, decks=decks)

@app.route('/session/<jlpt_level>/<int:deck_id>') # Removed 'int:' from jlpt_level
def game_session(jlpt_level, deck_id):
    mode = request.args.get('mode', 'normal')
    
    # Extract the number from strings like 'jlpt5' or 'n5'
    # This turns 'jlpt5' into 5
    try:
        level_num = int(''.join(filter(str.isdigit, jlpt_level)))
    except ValueError:
        return "Invalid Level Format", 400

    # Now pass the clean integer to your database handler
    words = get_words_by_deck(level_num, deck_id)
    
    return render_template('session.html', 
                           level=jlpt_level, 
                           level_num=level_num,
                           deck_id=deck_id, 
                           words=words, 
                           mode=mode)

# --- CORE MECHANIC: VOICE & MARKING ---

@socketio.on('voice_input')
def handle_voice(data):
    """
    Receives audio from the frontend, processes IPA, 
    and returns Sensei's feedback.
    """
    # Logic will go here: 
    # 1. stt_handler.process(data['audio'])
    # 2. evaluator.compare(input_ipa, target_ipa)
    # 3. emit('feedback', {'result': '...'})
    print(f"Received voice for word: {data['word_id']}")
    emit('feedback', {'message': 'Sensei is listening...', 'status': 'processing'})

@app.route('/api/mark', methods=['POST'])
def toggle_mark():
    data = request.json
    # We use the unique ID from the database now
    toggle_mark_status(data['word_id'], 1 if data['marked'] else 0)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    socketio.run(app, debug=True)