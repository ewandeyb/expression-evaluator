from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser import Parser, ParseError
from evaluator import Evaluator

app = Flask(__name__)
symbol_table = {}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    expression = data.get('expression', '').strip()
    
    if not expression:
        return jsonify({'error': 'Please enter an expression'})
    
    try:
        # Lexical analysis
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        if ast is None:
            return jsonify({'error': 'Empty expression'})
        
        # Evaluation
        evaluator = Evaluator(ast, symbol_table)
        evaluator.evaluate()
        
        # Get postfix notation
        postfix_str = str(evaluator)
        
        # Execute the assignment
        assigned_var = evaluator.execute()
        result_value = symbol_table[assigned_var]
        
        return jsonify({
            'success': True,
            'input': expression,
            'postfix': postfix_str,
            'result': f"{assigned_var} = {result_value}",
            'symbol_table': dict(symbol_table)
        })
        
    except ParseError as e:
        return jsonify({'error': f'Parse Error: {str(e)}'})
    except NameError as e:
        return jsonify({'error': f'Name Error: {str(e)}'})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})

@app.route('/clear_variables', methods=['POST'])
def clear_variables():
    global symbol_table
    symbol_table.clear()
    return jsonify({'success': True, 'symbol_table': {}})

@app.route('/get_variables', methods=['GET'])
def get_variables():
    return jsonify({'symbol_table': dict(symbol_table)})

if __name__ == '__main__':
    app.run(debug=True, port=8000)