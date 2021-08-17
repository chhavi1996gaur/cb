import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from gtts import gTTS


def make_final_df(input_value):
    df = pd.read_csv('final_df.csv')
    df['Input'] = input_value
    final_df = df[['answer', 'wrong_answer', 'Input', 'question']]
    return final_df

def make_pred(Input):
    Input = str(Input)
    final_df = make_final_df(Input)
    ques = []
    ques.append(final_df.loc[0, 'Input'])
    for i in range(len(final_df)):
        ques.append(final_df.loc[i, 'question'])
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(ques)
    ques_df = pd.DataFrame(vectors.toarray(), columns=vectorizer.get_feature_names(), index=ques)
    similarity = cosine_similarity(vectors[0:1], vectors)
    similarity_df = pd.DataFrame(similarity[0], columns=['Similarity Value'])
    similarity_df.drop([0], axis=0, inplace=True)
    similarity_df.reset_index(inplace=True)
    similarity_df.drop(['index'], axis=1, inplace=True)
    first_index = similarity_df['Similarity Value'].idxmax()
    first_output = final_df.loc[first_index, 'answer']
    first_sim = similarity_df.loc[first_index, 'Similarity Value']
    second_df = similarity_df.drop([first_index], axis = 0)
    second_index = second_df['Similarity Value'].idxmax()
    second_output = final_df.loc[second_index, 'answer']
    second_sim = second_df.loc[second_index, 'Similarity Value']
    third_df = second_df.drop([second_index], axis = 0)
    third_index = third_df['Similarity Value'].idxmax()
    third_output = final_df.loc[third_index, 'answer']
    third_sim = third_df.loc[third_index, 'Similarity Value']
    if first_sim>0:
        output_df = pd.DataFrame([[first_output, str(int(round(first_sim, 2) * 100)) + '%'], [second_output, (str(int(round(second_sim, 2) * 100)) + '%')],
                                      [third_output, (str(int(round(third_sim, 2) * 100)) + '%')]],
                                     columns=['Answer', 'Relevance'])
    else:
        output_df = pd.DataFrame([['No Relevant Answers found. Try other question.', ]])
    print(output_df)

    return output_df


def text_to_speech(text):
    '''voice_dict = {'Male': 0, 'Female': 1}
    gender = voice_dict[gender]

    engine = pyttsx3.init()

    # Setting up voice rate
    engine.setProperty('rate', 125)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    # Change voices: 0 for male and 1 for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[gender].id)
    with open('audio.wav', 'wb') as audio:
        engine.save_to_file(text, 'static/audio.wav')'''
    tts = gTTS(text)
    with open('static/audio.wav', 'wb') as audio:
        tts.save('audio.wav')
    main_file = open("audio.wav", "rb").read()
    dest_file = open('static/audio.wav', 'wb+')
    dest_file.write(main_file)
    dest_file.close()
    #engine.runAndWait()

