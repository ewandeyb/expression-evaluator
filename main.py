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
    expressions = data.get('expressions', [])
    
    if not expressions:
        return jsonify({'error': 'Please provide expressions'})
    
    # Create a local symbol table for this request to ensure isolation
    symbol_table = {}
    
    results = []
    errors = []
    
    for i, expression in enumerate(expressions):
        line_num = i + 1
        expression = expression.strip()
        
        if not expression:
            continue
            
        try:
            # Lexical analysis
            lexer = Lexer(expression)
            tokens = lexer.tokenize()
            
            # Parsing
            parser = Parser(tokens)
            ast = parser.parse()
            
            if ast is None:
                errors.append(f'Line {line_num}: Empty expression')
                continue
            
            # Evaluation
            evaluator = Evaluator(ast, symbol_table)
            evaluator.evaluate()
            
            # Get postfix notation
            postfix_str = str(evaluator)
            
            # Execute the assignment
            assigned_var = evaluator.execute()
            result_value = symbol_table[assigned_var]
            
            results.append({
                'line': line_num,
                'input': expression,
                'postfix': postfix_str,
                'result': f"{assigned_var} = {result_value}"
            })
            
        except ParseError as e:
            errors.append(f'Line {line_num}: Parse Error: {str(e)}')
        except NameError as e:
            errors.append(f'Line {line_num}: Name Error: {str(e)}')
        except Exception as e:
            errors.append(f'Line {line_num}: Error: {str(e)}')
    
    return jsonify({
        'success': True,
        'results': results,
        'errors': errors,
        'symbol_table': dict(symbol_table)
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)