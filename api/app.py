from flask import Flask, jsonify


app = Flask(__name__)

products = {
    1000: {'name': 'Keyboard', 'price': 23.8}, 
    1012: {'name': 'Mouse', 'price':14.5},
    2002: {'name': 'Laptop', 'price': 1098.12},
}

@app.route('/api/products')
def api_products():
    return jsonify({'products': products})


if __name__ == '__main__':
    app.run()