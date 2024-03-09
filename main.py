from flask import Flask, jsonify, request
import pandas as pd
from output import output
articles_data = pd.read_csv('articles.csv')
all_articles = articles_data[['url' , 'title' , 'text' , 'lang' , 'total_events']]
liked_articles = []
not_liked_articles = []

app = Flask(__name__)

def assign_val():
    m_data = {
        "url": all_articles.iloc[0,0],
        "title": all_articles.iloc[0,1],
        "text": all_articles.iloc[0,2] or "N/A",
        "lang": all_articles.iloc[0,3],
        "total_events": all_articles.iloc[0,4]/2
    }
    return m_data

@app.route("/get-article")
def get_article():

    article_info = assign_val()
    return jsonify({
        "data": article_info,
        "status": "success"
    })

@app.route("/liked-article")
def liked_article():
    global all_articles
    article_info = assign_val()
    liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

@app.route("/unliked-article")
def unliked_article():
    global all_articles
    article_info = assign_val()
    not_liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })
@app.route("/favourites")
def fav_article():
    global liked_articles
    return jsonify({
        "data":liked_articles,"success":"success"
    })
@app.route("/popular")
def popular_articles():
    articles_data=[]
    for i,data in output.iterrows():
        d={
        "url": data["url"],
        "title": data["title"],
        "text": data["text"],
        "lang": data["lang"],
        "total_events": data["total_events"]
        }
        articles_data.append(d)
    return(jsonify({
        "data":articles_data,"status":"success"
    }))
if __name__ == "__main__":
    app.run()