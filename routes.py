from flask import Flask, render_template
import helpers

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("home.html", questions_and_answers = helpers.get_csv_as_dict("transformed_data/test.csv").items())

if __name__ == '__main__':
    app.run(debug=True)
