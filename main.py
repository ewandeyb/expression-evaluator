from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser import Parser, ParseError
from evaluator import Evaluator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)