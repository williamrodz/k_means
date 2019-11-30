from flask import Flask, render_template
import k_means
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
  print ('I got clicked!')

  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)
