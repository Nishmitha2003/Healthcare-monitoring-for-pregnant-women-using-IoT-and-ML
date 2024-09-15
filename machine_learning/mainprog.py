
from flask import Flask, render_template,request,session,flash
import sqlite3 as sql
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/gohome')
def homepage():
    return render_template('index.html')


@app.route('/enternew')
def new_user():
   return render_template('signup.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['Name']
            phonno = request.form['MobileNumber']
            email = request.form['email']
            unm = request.form['Username']
            passwd = request.form['password']
            with sql.connect("pregnant.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user(name,phono,email,username,password)VALUES(?, ?, ?, ?,?)",(nm,phonno,email,unm,passwd))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/userlogin')
def user_login():
   return render_template("login.html")

@app.route('/logindetails',methods = ['POST', 'GET'])
def logindetails():
    if request.method=='POST':
            usrname=request.form['username']
            passwd = request.form['password']

            with sql.connect("pregnant.db") as con:
                cur = con.cursor()
                cur.execute("SELECT username,password FROM user where username=? ",(usrname,))
                account = cur.fetchall()

                for row in account:
                    database_user = row[0]
                    database_password = row[1]
                    if database_user == usrname and database_password==passwd:
                        session['logged_in'] = True
                        return render_template('home1.html')
                    else:
                        flash("Invalid user credentials")
                        return render_template('login.html')



@app.route('/info')
def predictin():
   return render_template('info.html')

# Load data and train the model
data = pd.read_csv('data.csv')
X = data.drop('Target', axis=1)
y = data['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2)
rf_classifier = RandomForestClassifier(n_estimators=20, random_state=2)
rf_classifier.fit(X_train, y_train)



# Define route for prediction
@app.route('/info', methods=['POST', 'GET'])
def predcrop():
    if request.method == 'POST':
        # Retrieve form data
        heart_beat = float(request.form['heart_beat'])
        sop2 = float(request.form['sop2'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        breath = float(request.form['breath'])
        sugar = float(request.form['sugar'])


        # Predict target based on user input
        prediction = predict_target(heart_beat, sop2, temperature, humidity, breath, sugar)

        # Calculate accuracy and generate classification report
        y_pred = rf_classifier.predict(X_test)
        print(y_pred)
        accuracy = "{:.2f}".format(accuracy_score(y_test, y_pred) * 100)
        class_report_dict = classification_report(y_test, y_pred, output_dict=True)

        precision_0 = "{:.2f}".format(class_report_dict['0']['precision'] * 100)
        recall_0 = "{:.2f}".format(class_report_dict['0']['recall'] * 100)
        f1_score_0 = "{:.2f}".format(class_report_dict['0']['f1-score'] * 100)

        precision_1 = "{:.2f}".format(class_report_dict['1']['precision'] * 100)
        recall_1 = "{:.2f}".format(class_report_dict['1']['recall'] * 100)
        f1_score_1 = "{:.2f}".format(class_report_dict['1']['f1-score'] * 100)
        # Pass prediction, accuracy, and classification report to the template for rendering
        return render_template('resultpred.html', prediction=prediction, accuracy=accuracy,
                               precision_0=precision_0, recall_0=recall_0, f1_score_0=f1_score_0,
                               precision_1=precision_1, recall_1=recall_1, f1_score_1=f1_score_1)

    # Render the form if request method is GET
    return render_template('info.html')

# Function to predict the target based on user input
def predict_target(heart_beat, sop2, temperature, humidity, breath, sugar):
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
        return "Patient is Healthy"
    else:
        return "Patient is Unhealthy"



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)


