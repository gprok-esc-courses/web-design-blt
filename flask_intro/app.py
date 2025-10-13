from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    product_list = [
        {'name': 'Keyboard VM7', 'price': 34.2},
        {'name': 'Mouse A3', 'price': 12.1},
        {'name': 'Monitor AA786', 'price': 186.2},
        {'name': 'Laprop X', 'price': 1098.23}
    ]
    return render_template('products.html', products=product_list)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/confirm', methods=['POST'])
def confirm():
    data = request.form
    return render_template('confirm.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)