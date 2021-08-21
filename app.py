from flask import Flask
#from flask_gtts import gtts
import flask
import os
import time
app = Flask(__name__, template_folder='templates',static_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

#gtts(app)

from preprocess_2 import make_pred, text_to_speech, speech_to_text

@app.route('/', methods=['GET', 'POST'])
def main():
    global result
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
        try:
            if flask.request.method == 'POST':
                f = flask.request.files['audio_data']
                with open('ques.wav', 'wb') as audio:
                    f.save(audio)
                print('file uploaded successfully')
                Input = speech_to_text('ques.wav')
        except:
            Input = flask.request.form['Question']
        #print(Input)
        prediction = make_pred(Input)
        #         print(prediction)
        #         print(type(prediction))
        prediction.index = prediction.index + 1

        prediction.reset_index(inplace=True)
        result = list(prediction.values)
        text = 'Hello' + result[0][1] + 'and the Relevance of this answer is ' + str(result[0][2] + 'Hello')
        
        file_name=text_to_speech(text)
        zz=str(time.time())
        print(file_name)
        

    return flask.render_template('index.html', headings=headings, original_input=Input, data=result,testing=file_name)



@app.route('/dashboard', methods=['GET'])
def dashboard():
    return flask.render_template('b.html')
    
    
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
    



if __name__ == '__main__':
   
    app.run(debug=True)
    