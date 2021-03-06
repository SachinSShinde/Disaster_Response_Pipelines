# import libraries
import sys
import pandas as pd
import numpy as np
import re
import nltk
nltk.download(['punkt', 'wordnet'])
nltk.download('stopwords')
from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV

import pickle


def load_data(database_filepath):
    '''
    Loads data from database file and return features(messages) and labels(categories)
    Args: database_filepath: the path of the database
    Returns: X: features(messages)
             Y: categories
    '''
    engine = create_engine('sqlite:///'+database_filepath)
    #conn = engine.connect();
    df = pd.read_sql("SELECT * FROM disaster_data_cleaned", engine)
    X = df['message']
    Y = df.iloc[:,4:]
    category_names = Y.columns
    return X, Y, category_names


def tokenize(text):
    '''
    Tokenize a text and cleaning it
    Args: text: the text to process
    Returns: clean_tokens: processed text, with removed stop words, and Lemmatization applied
    '''
    # remove punctuations
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in stopwords.words('english')]
    # lemmatize as shown in the classroom
    lemmatizer = WordNetLemmatizer()
    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
    return clean_tokens


def build_model():
    '''
    Builds a ML model pipeline for training
    Returns: cv: A Grid Search selector on the complete model pipeline
    '''
    pipeline = Pipeline([('count', CountVectorizer(tokenizer=tokenize)),
                         ('tfidf', TfidfTransformer()),
                         ('model', MultiOutputClassifier(RandomForestClassifier(n_estimators=10,random_state=13,n_jobs=1)))
                        ]);

    parameters = {'model__estimator__max_depth' : [5, 10], 'model__estimator__max_features' : [5, 10]};

    cv = GridSearchCV(pipeline, param_grid=parameters, verbose=2);

    return cv;


def evaluate_model(model, X_test, Y_test, category_names):
    '''
    Evalutates the model on testing data
    Args: X_test: Messages to test on
          Y_test: Categories to predict
          category_names: Category label names
    '''
    y_pred = model.predict(X_test)
    y_pred = pd.DataFrame(y_pred)
    y_pred.columns = Y_test.columns
    
    for column in Y_test.columns:
        print('Column : ' , column)
        print(classification_report(Y_test[column], y_pred[column]))
    


def save_model(model, model_filepath):
    '''
    Saves the model to a file
    Args: model: The Scikit-Learn model to save
          model_filepath: The file in which to save the model
    '''
    pickle.dump(model, open(model_filepath, 'wb'));


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()