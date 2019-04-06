from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('form(ajax_ex).html')

@app.route('/process', methods=['POST'])
def process():

	email = request.form['email']
	name = request.form['name']

	if name and email:
		newName = name[::-1]

		return jsonify({'name' : "test"})

	return jsonify({'error' : 'Missing Data!'})

if __name__ == '__main__':
	app.run(debug=True)