from flask import Flask, render_template, request
from page import Page
import helpers

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("home.html", questions_and_answers = helpers.get_csv_as_list_dict('raw_data/2017/12.csv'))

@app.route('/ask_question', methods=['POST'])
def ask_question():
    return request.form['text']

if __name__ == '__main__':
    app.run(debug=True)
