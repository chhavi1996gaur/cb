from flask import Flask
#from flask_gtts import gtts
import flask

app = Flask(__name__, template_folder='templates')
#gtts(app)

from preprocess_2 import make_pred, text_to_speech

#engine = pyttsx3.init()

@app.route('/', methods=['GET', 'POST'])
def main():
    headings = ['', 'Relevant Answers', 'Relevance']
    if flask.request.method == 'GET':
        return (flask.render_template('index.html'))

    if flask.request.method == 'POST':
        Input = flask.request.form['Question']
        #print(Input)
        prediction = make_pred(Input)
        #         print(prediction)
        #         print(type(prediction))
        prediction.index = prediction.index + 1

        prediction.reset_index(inplace=True)
        result = list(prediction.values)
        text = result[0][1] + 'and the Relevance of this answer is ' + str(result[0][2] + 'Hello')
        text_to_speech(text, 'Male')


    return flask.render_template('index.html', headings=headings, original_input=Input, data=result)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return flask.render_template('b.html')


if __name__ == '__main__':
    app.run()