from unittest import TestCase

from flask.json import jsonify
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True

    def test_display_game(self):
        """Successful status, html loaded, starting statistics, session for board created"""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<p>High Score:', html)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('turns'))
            self.assertIn('board', session)

    def test_evaluate_word(self):
        """Create sample session board, check for correct word evaluation results"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ['A','B','C','D','E'],
                    ['A','B','C','D','E'],
                    ['A','B','C','D','E'],
                    ['A','B','C','D','E'],
                    ['A','B','C','D','E'],
                ]

            response = client.get('/evaluate?word=baa')
            self.assertEqual(response.json['result'], 'ok')

            response = client.get('/evaluate?word=abcd')
            self.assertEqual(response.json['result'], 'not-word')

            response = client.get('/evaluate?word=hello')
            self.assertEqual(response.json['result'], 'not-on-board')

            self.assertEqual(response.status_code, 200)

    def test_post_score(self):
        """Sessions storing correct values, return value brokeRecord accurate"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['turns'] = 4
                change_session['highscore'] = 20
            
            response = client.post('/post_score', json={'score': 15})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(session['turns'], 5)
            self.assertEqual(session['highscore'], 20)
            self.assertFalse(response.json['brokeRecord'])

            


            



