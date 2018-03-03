# Importing flask library
from app import app
from flask import Flask, redirect, make_response, render_template, url_for, session, request, escape, flash
import os
app.secret_key = os.environ.get('SECRET_KEY') or 'hard to guess string'

@app.route('/')
@app.route('/index')
def index():
    username = ''
    if 'username' in session: #check if the user is already in session, if so, direct the user to survey.html Hint: render_template with a variable
        username = session['username']
        return render_template('survey.html', username=username)
    else:
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST']) # You need to specify something here for the function to get requests
def login():
    # Here, you need to have logic like if there's a post request method, store the username and email from the form into
    # session dictionary
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        return redirect(url_for('index'))
    return None

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('email', None)
	return redirect(url_for('index'))

@app.route('/submit-survey', methods=['GET', 'POST'])
def submitSurvey():
    username = session['username']
    email = session['email']
    if request.method == 'POST': #check if user in session or request.method == 'POST'?
        username = session.get('username')
        #get the rest o responses from users using request library Hint: ~3 lines of code
        surveyResponse = dict()
        surveyResponse['color'] = request.form.get('color')
        surveyResponse['food'] = request.form.get('food')
        surveyResponse['vacation'] = request.form.get('vacation')

        surveyResponse['fe-before'] = request.form.get('feBefore')
        surveyResponse['fe-after'] = request.form.get('feAfter')

        if surveyResponse['fe-before'] < surveyResponse['fe-after']:
            surveyResponse['result-message'] = 'Wow! Your front-end skillz got better in only a few weeks!'
        elif surveyResponse['fe-before'] == surveyResponse['fe-after']:
            surveyResponse['result-message'] = 'Looks like your front-end skillz are still the same. Need to work harder!'
        else:
            surveyResponse['result-message'] = 'Your front-end skillz are now worse than before! What happened???'

        return render_template('results.html', surveyResponse=surveyResponse, username=username) # pass in variables to the template
    else:
        return render_template('login.html')

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404
