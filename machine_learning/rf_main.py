'''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load data from CSV
data = pd.read_csv('data.csv')

# Separate features and target variable
X = data.drop('Target', axis=1)  # Adjust 'target_column_name' to the column name of your target variable
y = data['Target']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
rf_classifier.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_classifier.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Generate and print classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))
'''

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load data from CSV
data = pd.read_csv('data.csv')

# Separate features and target variable
X = data.drop('Target', axis=1)
y = data['Target']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2)

# Initialize Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=20, random_state=2)

# Train the classifier
rf_classifier.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_classifier.predict(X_test)
print((y_pred))

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Generate and print classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))


# Function to predict the target based on user input
def predict_target(heart_beat, sop2, temperature, humidity):
    # Create a DataFrame with user input
    user_data = pd.DataFrame({
        'heart_beat': [heart_beat],
        'sop2': [sop2],
        'temperature': [temperature],
        'humidity': [humidity],
        'breath': [breath],
        'sugar': [sugar]

    })

    # Predict target for user input
    prediction = rf_classifier.predict(user_data)

    # Determine if the prediction is close to 0 or 1
    if prediction == 0:
        print("Predicted target: 0 (close to 0)")
    else:
        print("Predicted target: 1 (close to 1)")


# Get user input for features
heart_beat = float(request.form['heart_beat'])
sop2 = float(request.form['sop2'])
temperature = float(request.form['temperature'])
humidity = float(request.form['humidity'])
breath = float(request.form['breath'])
sugar = float(request.form['sugar'])


# Predict target based on user input
prediction = predict_target(heart_beat, sop2, temperature, humidity, breath, sugar )


