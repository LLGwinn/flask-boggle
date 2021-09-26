from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# end app setup

boggle_game = Boggle()

@app.route('/')
def display_game():
    """Display game board and statistics"""
    board = boggle_game.make_board()  #creates array of arrays
    session['board'] = board
    highscore = session.get('highscore', 0)
    turns = session.get('turns', 0)

    return render_template('index.html', board=board, highscore=highscore, turns=turns)

@app.route('/evaluate')
def evaluate_word():
    """Check to see if user's word is in dictionary and possible on board"""
    word = request.args['word']
    board = session['board']
    result = boggle_game.check_valid_word(board, word)

    return jsonify({'result': result})

@app.route("/post_score", methods=['POST'])
def post_score():
    """Receive score, update turns, update high score if appropriate"""
    score = request.json['score']
    highscore = session.get('highscore', 0)
    turns = session.get('turns', 0)

    session['turns'] = turns + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)

