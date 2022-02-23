import pandas as pd
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, SpatialDropout1D
from tensorflow.keras.layers import Embedding

# 3 < negative, else positive


def f(row):
    if row['rating'] < 3:
        val = "negative"
    else:
        val = "positive"
    return val


reviews_df = pd.read_csv("new-reviews.csv")
sentiment_label = reviews_df.sentiment.factorize()
reviews = reviews_df.text.values
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(reviews)
vocab_size = len(tokenizer.word_index) + 1
encoded_docs = tokenizer.texts_to_sequences(reviews)
padded_sequence = pad_sequences(encoded_docs, maxlen=200)

# difine model
embedding_vector_length = 32
model = Sequential()
model.add(Embedding(vocab_size, embedding_vector_length, input_length=200))
model.add(SpatialDropout1D(0.25))
model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy'])
print(model.summary())

# fit model
history = model.fit(
    padded_sequence, sentiment_label[0], validation_split=0.2, epochs=5, batch_size=32)

# save model
model.save("final_model.h5")
