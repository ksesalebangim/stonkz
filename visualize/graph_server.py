import json

from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stocks"
)
mycursor = mydb.cursor()


@app.route("/get_news")
def get_news():
    cdate = request.args.get("date")
    symbol = request.args.get("symbol")
    mycursor.execute(f"SELECT  `title`  FROM `news` WHERE `symbol`='{symbol}' and date = '{cdate}'")
    myresult = mycursor.fetchall()
    res = []
    for row in myresult:
        res.append(row[0])
    return json.dumps(res)


@app.route("/include")
def include():
    q = request.args.get("q")
    f = open("include/" + q, "rb")
    data = f.read()
    f.close()
    return data



@app.route("/")
def main():
    retStr = """
     <div class="container"><canvas id="examChart"></canvas></div>\n
     <style>canvas{width:1000px !important; height:600px !important;}</style>\n
    <script src="include?q=chart.js"></script>\n
    <script src="include?q=utils.js"></script>\n
    <script src="include?q=config.js"></script>\n
    <script src="include?q=runchart.js"></script>\n
    """

    return retStr

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

app.run(host='0.0.0.0', port=81,ssl_context='adhoc')
