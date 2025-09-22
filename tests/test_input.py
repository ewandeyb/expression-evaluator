import pytest
from main import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestBatchProcessing:
    """Test cases for batch processing functionality."""

    def test_single_expression(self, client):
        """Test processing a single expression."""
        response = client.post('/evaluate', 
                              json={'expressions': ['a = 5']})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert len(data['results']) == 1
        assert data['results'][0]['result'] == 'a = 5'
        assert data['symbol_table'] == {'a': 5}
        assert len(data['errors']) == 0

    def test_multiple_expressions_with_dependencies(self, client):
        """Test processing multiple expressions where later ones depend on earlier ones."""
        expressions = [
            'a = 5',
            'b = a + 3',
            'c = a * b'
        ]
        response = client.post('/evaluate', 
                              json={'expressions': expressions})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert len(data['results']) == 3
        assert data['results'][0]['result'] == 'a = 5'
        assert data['results'][1]['result'] == 'b = 8'
        assert data['results'][2]['result'] == 'c = 40'
        assert data['symbol_table'] == {'a': 5, 'b': 8, 'c': 40}
        assert len(data['errors']) == 0

    def test_complex_mathematical_expressions(self, client):
        """Test complex mathematical expressions."""
        expressions = [
            'x = 10',
            'y = x + 5 * 2',
            'z = (x + y) * 2 - 10',
            'result = z / 5 + x'
        ]
        response = client.post('/evaluate', 
                              json={'expressions': expressions})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert len(data['results']) == 4
        assert data['symbol_table']['x'] == 10
        assert data['symbol_table']['y'] == 20  # 10 + 5*2
        assert data['symbol_table']['z'] == 50  # (10+20)*2-10
        assert data['symbol_table']['result'] == 20  # 50/5+10

    def test_empty_expressions_list(self, client):
        """Test handling of empty expressions list."""
        response = client.post('/evaluate', 
                              json={'expressions': []})
        data = response.get_json()
        
        assert response.status_code == 200
        assert 'error' in data
        assert 'provide expressions' in data['error']

    def test_missing_expressions_key(self, client):
        """Test handling when expressions key is missing."""
        response = client.post('/evaluate', 
                              json={})
        data = response.get_json()
        
        assert response.status_code == 200
        assert 'error' in data

    def test_expressions_with_syntax_errors(self, client):
        """Test handling expressions with syntax errors."""
        expressions = [
            'a = 5',
            'b = a +',  # Syntax error
            'c = a * 2'
        ]
        response = client.post('/evaluate', 
                              json={'expressions': expressions})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert len(data['results']) == 2  # Only a and c should succeed
        assert len(data['errors']) == 1
        assert 'Line 2' in data['errors'][0]
        assert data['symbol_table'] == {'a': 5, 'c': 10}

    def test_expressions_with_undefined_variables(self, client):
        """Test handling expressions with undefined variables."""
        expressions = [
            'a = 5',
            'b = undefinedvar + 1',  # NameError - no underscores allowed
            'c = a * 2'
        ]
        response = client.post('/evaluate', 
                              json={'expressions': expressions})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert len(data['results']) == 2  # Only a and c should succeed
        assert len(data['errors']) == 1
        assert 'Line 2' in data['errors'][0]
        assert 'Error' in data['errors'][0]  # Could be Name Error or other error

    def test_empty_and_whitespace_lines(self, client):
        """Test handling of empty lines and whitespace-only lines."""
        expressions = [
            'a = 5',
            '',  # Empty line
            '   ',  # Whitespace only
            'b = a + 1'
        ]
        response = client.post('/evaluate', 
                              json={'expressions': expressions})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert len(data['results']) == 2  # Only a and b should be processed
        assert data['symbol_table'] == {'a': 5, 'b': 6}

    def test_operator_precedence(self, client):
        """Test operator precedence in expressions."""
        expressions = [
            'a = 2 + 3 * 4',  # Should be 14
            'b = (2 + 3) * 4',  # Should be 20
            'c = 10 - 6 / 2',  # Should be 7, not 2
            'd = (10 - 6) / 2'  # Should be 2
        ]
        response = client.post('/evaluate', 
                              json={'expressions': expressions})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['symbol_table']['a'] == 14
        assert data['symbol_table']['b'] == 20
        assert data['symbol_table']['c'] == 7
        assert data['symbol_table']['d'] == 2

    def test_variable_reassignment(self, client):
        """Test reassigning variables."""
        expressions = [
            'x = 10',
            'y = x + 5',
            'x = 20',  # Reassign x
            'z = x + y'  # y should still be 15, x is now 20
        ]
        response = client.post('/evaluate', 
                              json={'expressions': expressions})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['symbol_table']['x'] == 20
        assert data['symbol_table']['y'] == 15
        assert data['symbol_table']['z'] == 35

    def test_large_numbers(self, client):
        """Test handling of large numbers."""
        expressions = [
            'big = 999999999',
            'bigger = big * 1000'
        ]
        response = client.post('/evaluate', 
                              json={'expressions': expressions})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['symbol_table']['big'] == 999999999
        assert data['symbol_table']['bigger'] == 999999999000

    def test_division_by_zero(self, client):
        """Test handling division by zero."""
        expressions = [
            'a = 10',
            'b = 0',
            'c = a / b'  # Should cause an error
        ]
        response = client.post('/evaluate', 
                              json={'expressions': expressions})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert len(data['results']) == 2  # Only a and b should succeed
        assert len(data['errors']) == 1
        assert 'Line 3' in data['errors'][0]

    def test_isolation_between_requests(self, client):
        """Test that different requests don't affect each other."""
        # First request
        response1 = client.post('/evaluate', 
                               json={'expressions': ['x = 100']})
        data1 = response1.get_json()
        
        # Second request - should not see x from first request
        response2 = client.post('/evaluate', 
                               json={'expressions': ['y = x + 1']})
        data2 = response2.get_json()
        
        assert data1['success'] is True
        assert data1['symbol_table'] == {'x': 100}
        
        assert data2['success'] is True
        assert len(data2['errors']) == 1  # x should be undefined
        assert 'Name Error' in data2['errors'][0]


class TestPostfixNotation:
    """Test cases for postfix notation generation."""

    def test_postfix_simple_expression(self, client):
        """Test postfix notation for simple expressions."""
        response = client.post('/evaluate', 
                              json={'expressions': ['a = 5 + 3']})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['results'][0]['postfix'] == 'a 5 3 + ='

    def test_postfix_complex_expression(self, client):
        """Test postfix notation for complex expressions."""
        response = client.post('/evaluate', 
                              json={'expressions': ['result = (2 + 3) * 4']})
        data = response.get_json()
        
        assert response.status_code == 200
        assert 'result 2 3 + 4 * =' in data['results'][0]['postfix']