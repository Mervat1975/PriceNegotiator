import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
import tensorflow as tf
import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences


def predict_sentiment(text):
    reviews_df = pd.read_csv("./sentiment/ai/new-reviews.csv")
    reviews = reviews_df.text.values
    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(reviews)
    tw = tokenizer.texts_to_sequences([text])
    tw = pad_sequences(tw, maxlen=200)
    sentiment_label = reviews_df.sentiment.factorize()
    model_c = keras.models.load_model("./sentiment/ai/final_model.h5")
    prediction = int(model_c.predict(tw).round().item())
    print(prediction)
    return (sentiment_label[1][prediction])
