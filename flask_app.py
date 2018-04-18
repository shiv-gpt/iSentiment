# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request
from flask import make_response
import miner
import os
from datetime import datetime


app = Flask(__name__, static_url_path = "/static", static_folder = "static")
app.config['STATIC_FOLDER'] ='static'

@app.route('/')
# def hello_world():
#    return 'Hello World'
@app.route('/index', methods = ['POST', 'GET'])
def index():
   response = None
   if request.method == 'POST':
        topic = request.form['tweetTopic']
        strNumber = request.form['tweetNumber']
        print(strNumber)
        if strNumber is not "":
            number = int(strNumber)
            # os.remove(os.path.join('static', 'plot.png'))
            miner.performSentimentAnalysis(topic, number)
            response = make_response(redirect(url_for('image')))
            # response.headers['Cache-Control'] = 'no-cache, no-store'
            # response.headers['Pragma'] = 'no-cache'
            # response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
            # response.headers['Cache-Control'] = 'public, max-age=0'

            # response.headers['Last-Modified'] = datetime.now()
            # response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            # response.headers['Pragma'] = 'no-cache'
            # response.headers['Expires'] = '-1'
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            response.headers['Cache-Control'] = 'public, max-age=0'
            # result = "TRUE"
            # resp = make_response('{"response": '+result+'}')
            # resp.headers['Content-Type'] = "application/json"
            # return response
            return redirect(url_for('image'))
   return render_template('index.html', message='')
   # return message
   # else:
   #      topic = request.GET.get['tweetTopic']
   #      number = request.GET.get['tweetNumber']
   #      miner.performSentimentAnalysis('Trump', 100)
   #      return redirect(url_for('index'))

@app.route('/image')
def image():
    full_filename = '/static/plot.png'
    # print(full_filename)
    response = make_response(render_template('image.html', user_image = full_filename))
    # # response.headers['Cache-Control'] = 'no-cache, no-store'
    # # response.headers['Pragma'] = 'no-cache'
    # # response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    # # response.headers['Cache-Control'] = 'public, max-age=0'
    # # response.headers['Last-Modified'] = datetime.now()
    # # response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    # # response.headers['Pragma'] = 'no-cache'
    # # response.headers['Expires'] = '-1'
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
    # return render_template('image.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
   app.run(debug = True)

