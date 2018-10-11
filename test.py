from flask import Flask, render_template, request 

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello fucking world!'

@app.route('/input')
def index():
	return render_template('input.html')

@app.route('/Evaluation', methods = ['GET','POST'])
def success():
	if request.method == 'POST':
		age = request.form['age']
		gender = request.form['gender']
		if gender == "男":
			gend = 0
		elif gender == "女":
			gend = 1
		else:
			pass
		weight = request.form['weight']
		filepath = request.form['filepath']
		return
		#return render_template('result.html', age = age, gender = gend, weight = weight, filepath = filepath)
	else:
		pass



if __name__ == "__main__":
	app.run()
