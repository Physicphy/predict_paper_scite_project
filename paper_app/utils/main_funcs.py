from paper_app.services.embedding_api import en
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier as rfc

def msg_processor(msg_code):
    '''
    msg_processor returns a msg object with 'msg', 'type'
    where 'msg' corresponds to the message user sees
    and 'type' is the color of the alert element

    codes:
        - 0 : Successfully added to database
        - 1 : User does not exist
        - 2 : Unable to retrieve tweets
        - 3 : Successfully deleted user
    '''

    msg_code = int(msg_code)

    msg_list = [
        (
            'Successfully added to database',
            'success'
        ),
        (
            'User does not exist',
            'warning'
        ),
        (
            'Unable to retrieve tweets',
            'warning'
        ),
        (
            'Successfully deleted user',
            'info'
        )
    ]

    return {
        'msg':msg_list[msg_code][0],
        'type':msg_list[msg_code][1]
    }

def predict_text(user_list, predict_text):
    user_1, user_2 = user_list

    embeddings = []
    labels = []

    for tw in user_1.many_tweets:
        embeddings.append(tw.embedding)
        labels.append(user_1.username)

    for tw in user_2.many_tweets:
        embeddings.append(tw.embedding)
        labels.append(user_2.username)

    classifier = rfc(class_weight='balanced')
    # classifier = LogisticRegression()
    classifier.fit(embeddings, labels)

    predict_embedding = en.encode(texts=[predict_text])
    prediction = classifier.predict(predict_embedding)

    print(f"Prediction Results {prediction[0]}")

    return prediction[0]
