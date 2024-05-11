

# FOR AMALYZE THE DATA


# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import nltk
nltk.download('vader_lexicon')

def analyze_sentiment(comment_file, training_file):
    # Load cleaned comments and sentiment analysis results
    comments_df = pd.read_csv(comment_file)
    training_df = pd.read_csv(training_file)

    # Ensure both dataframes have the same number of rows
    min_len = min(len(comments_df), len(training_df))
    comments_df = comments_df[:min_len]
    training_df = training_df[:min_len]

    # Concatenate the dataframes side by side
    df = pd.concat([comments_df, training_df], axis=1)

    # Initialize the sentiment analyzer
    sentiments = SentimentIntensityAnalyzer()

    # Calculate the sentiment scores for each comment
    df['sentiment_scores'] = df['comment'].apply(lambda x: sentiments.polarity_scores(x))

    # Extract the compound scores from the sentiment scores
    df['Compound'] = df['sentiment_scores'].apply(lambda x: x['compound'])

    # Determine the sentiment for each comment based on the compound score
    df['Sentiment'] = df['Compound'].apply(lambda x: 'Positive' if x >= 0.05 else ('Negative' if x <= -0.05 else 'Neutral'))

    # Count the number of positive, negative, and neutral sentiments
    sentiment_counts = df['Sentiment'].value_counts()

    # Create a dataframe for the plot
    sentiment_counts = pd.DataFrame({'Sentiment': ['Positive', 'Negative', 'Neutral'],
                                     'Count': [sentiment_counts.get('Positive', 0), sentiment_counts.get('Negative', 0), sentiment_counts.get('Neutral', 0)]})


    return df

def analyze_main():
    comment_file = "cleaned_comments.csv"
    training_file = "sentiment_analysis_results.csv"
    analyzed_data = analyze_sentiment(comment_file, training_file)



# Split the data into training and testing sets
    X = analyzed_data['comment']
    y = analyzed_data['Sentiment']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Vectorize the comments
    vectorizer = TfidfVectorizer(max_features=1000)
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    # Initialize and train the Random Forest classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_vectorized, y_train)

    # Predict sentiment on the test set
    y_pred = clf.predict(X_test_vectorized)




    # Evaluate the classifier
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Plot the sentiments based on the test set
    sentiment_counts_test = pd.DataFrame({'Sentiment': ['Positive', 'Negative', 'Neutral'],
                                        'Count': [sum(y_test == 'Positive'), sum(y_test == 'Negative'), sum(y_test == 'Neutral')]})

    return sentiment_counts_test

