from flask import Flask, render_template, request
from newsapi import NewsApiClient
import scrape
import random
import datetime

app = Flask(__name__)

APIKEY =  # API key
newsapi = NewsApiClient(api_key=APIKEY)


@app.route("/")
def init():
    stats_list, state_list, confirmed_list, cured_list, death_list = scrape.scrape_now()
    number_of_colors = len(state_list)
    confirmed_list = [None if v is 0 else v for v in confirmed_list]
    cured_list = [None if v is 0 else v for v in cured_list]
    death_list = [None if v is 0 else v for v in death_list]
    color = ["#"+''.join([random.choice('0123456789ABCDEF')
                          for j in range(6)]) for i in range(number_of_colors)]
    top_headlines = newsapi.get_top_headlines(q='coronavirus',
                                              language='en',
                                              country='in'
                                              )

    return render_template(
        "index.html",
        color=color,
        state_list=state_list,
        stats_list=stats_list,
        confirmed_list=confirmed_list,
        cured_list=cured_list,
        death_list=death_list,
        news=top_headlines['articles']
    )


@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
