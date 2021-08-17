from flask import Flask
#from flask_gtts import gtts
import flask
import os

app = Flask(__name__, template_folder='templates')
#gtts(app)

from preprocess_2 import make_pred, text_to_speech


@app.route('/', methods=['GET', 'POST'])
def main():
    headings = ['', 'Relevant Answers', 'Relevance']
    if flask.request.method == 'GET':
        try:
            os.remove('static/audio.wav')
        except OSError:
            pass
        return (flask.render_template('index.html'))

    if flask.request.method == 'POST':
        try:
            os.remove('static/audio.wav')
        except OSError:
            pass
        Input = flask.request.form['Question']
        #print(Input)
        prediction = make_pred(Input)
        #         print(prediction)
        #         print(type(prediction))
        prediction.index = prediction.index + 1

        prediction.reset_index(inplace=True)
        result = list(prediction.values)
        text = 'Hello' + result[0][1] + 'and the Relevance of this answer is ' + str(result[0][2] + 'Hello')
        text_to_speech(text)


    return flask.render_template('index.html', headings=headings, original_input=Input, data=result)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return flask.render_template('b.html')


if __name__ == '__main__':
    app.run()