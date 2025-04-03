from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

def train_model(intents):
    # Prepare training data
    texts = []
    labels = []
    for intent in intents:
        for pattern in intent['patterns']:
            texts.append(pattern)
            labels.append(intent['tag'])
    
    # Vectorize text
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    
    # Train classifier
    clf = MultinomialNB()
    clf.fit(X, labels)
    
    # Save model
    with open('model.pkl', 'wb') as f:
        pickle.dump((vectorizer, clf), f)