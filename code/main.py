from flask import Flask, jsonify, request
import csv

from storage import all_articles, liked_articles, not_liked_articles, not_watched_articles
from demographic_filtering import output
from content_filtering import get_recommendations

all_articles=[]
with open("articles.csv") as f:
    reader=csv.reader(f)
    data=list(reader)
    all_articles=data[1:]

liked_articles=[]
not_liked_articles=[]

app=Flask(__name__)
@app.route("/get-article")

def get_article():
    article_data = {
        "title": all_articles[0][13],
        "contentId": all_articles[0][5],
        "contentType": all_articles[0][11],
        "lang": all_articles[0][15],
        "total_events": all_articles[0][16],
        "url": all_articles[0][12],
        "eventType": all_articles[0][4],
    }
    return jsonify({
        "data":all_articles[0],
        "status":"success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article=all_articles[0]
    all_articles=all_articles[1:]
    liked_articles.append(article)
    return jsonify({
        "status":"success"
    }), 201

@app.route("/not-liked-article", methods=["POST"])
def not_liked_article():
    article=all_articles[0]
    all_articles=all_articles[1:]
    not_liked_articles.append(article)
    return jsonify({
        "status":"success"
    }), 201

@app.route("/not-watched-article", methods=["POST"])
def not_watched_article():
    article=all_articles[0]
    all_articles=all_articles[1:]
    not_watched_articles.append(article)
    return jsonify({
        "status":"success"
    }), 201    

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
    app.run()