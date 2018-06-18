import pickle
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import sklearn

from . import preprocessing

THISDIR = os.path.abspath(os.path.dirname(__file__))
MODELS_DIR = os.path.join(THISDIR, 'models')

COUNT_VECTORIZER_FILENAME = os.path.join(MODELS_DIR, 'count_vectorizer.pkl')
TFIDF_TRANSFORMER_FILENAME = os.path.join(MODELS_DIR, 'tfidf_transformer.pkl')
MODEL_FILENAME = os.path.join(MODELS_DIR, 'model.pkl')


def learn(records_list, labels_list):

    assert len(records_list) == len(labels_list), 'Length of records and labels must be equal'

    records = np.array(records_list)
    labels = np.array(labels_list)

    records = preprocessing.preprocess_text_vector(records)

    count_vect = CountVectorizer()
    tfidf_trans = TfidfTransformer()

    x_count = count_vect.fit_transform(records)
    x_tfidf = tfidf_trans.fit_transform(x_count)

    model = sklearn.linear_model.SGDClassifier(
        loss="log", alpha=1e-3, max_iter=10)
    model.fit(x_tfidf, labels)

    with open(COUNT_VECTORIZER_FILENAME, 'wb') as file_opened:
        pickle.dump(count_vect, file_opened)

    with open(TFIDF_TRANSFORMER_FILENAME, 'wb') as file_opened:
        pickle.dump(tfidf_trans, file_opened)

    with open(MODEL_FILENAME, 'wb') as file_opened:
        pickle.dump(model, file_opened)


def predict_labels(text):

    with open(COUNT_VECTORIZER_FILENAME, 'rb') as file_opened:
        count_vect = pickle.load(file_opened)

    with open(TFIDF_TRANSFORMER_FILENAME, 'rb') as file_opened:
        tfidf_trans = pickle.load(file_opened)

    with open(MODEL_FILENAME, 'rb') as file_opened:
        model = pickle.load(file_opened)

    records = np.array([text])
    records = preprocessing.preprocess_text_vector(records)

    labels = model.classes_.tolist()
    probas = model.predict_proba(
        tfidf_trans.transform(count_vect.transform(records)))

    results = list(zip(labels, probas[0]))
    results.sort(key=lambda it: it[1], reverse=True)

    return results
