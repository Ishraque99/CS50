from flask import Flask, redirect, render_template, request, url_for

import sys
import os
import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name, 100)
    if tweets == None:
        return redirect(url_for("index"))

    # TODO
    positive, negative, neutral = 0.0, 0.0, 0.0
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    analyzer = Analyzer(positives, negatives)
    for tweet in tweets:
        score = analyzer.analyze(tweet)
        if score > 0.0:
            
            positive += 1.0
            
        elif score < 0.0:
            
            negative += 1.0
            
        else:
            neutral += 1.0

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
