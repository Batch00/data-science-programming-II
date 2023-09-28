# project: p4
# submitter: cmbatchelor
# partner: none
# hours: 8


import pandas as pd
import re
import flask
import time
from flask import Flask, request, render_template, jsonify
from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import numpy as np

# data set from https://www.kaggle.com/datasets/minisam/marvel-movie-dataset

app = Flask(__name__)
df = pd.read_csv("main.csv")

#print(df)
counter = 0
cmap = None

@app.route('/')
def home():
    global counter
    
    f = open("index.html", "r+")
    html = f.read()
          
    if counter < 10:
        if counter % 2 == 0:
            #print("A")
            html = re.sub("from=B","from=A", html)
            html = re.sub("#ff0000","#0000ff", html)
            f.seek(0)
            f.write(html)
            f.truncate()
            counter += 1
            return html
        elif counter % 2 == 1:
            #print("B")
            html = re.sub("from=A","from=B", html)
            html = re.sub("#0000ff","#ff0000", html)
            f.seek(0)
            f.write(html)
            f.truncate()
            counter += 1
            return html
    else:
        if visit_a > visit_b:  
            html = re.sub("from=B","from=A", html)
            html = re.sub("#ff0000","#0000ff", html)
            f.seek(0)
            f.write(html)
            f.truncate()
            f.close()
            return html
        else:
            html = re.sub("from=A","from=B", html)
            html = re.sub("#0000ff","#ff0000", html)
            f.seek(0)
            f.write(html)
            f.truncate()
            f.close()
            return html

temps = [70,75,74,72]

@app.route("/budget.svg")        
def gen_budget():
    fig, ax = plt.subplots(figsize=(10,10)) 
    
    if df['Budget'][1] > 1000000:
        df['Budget'] = df['Budget'] / 1000000
    
    df.plot.barh(x = "Title", y = "Budget", ax=ax)
    ax.set_xlabel("Budget (in Millions)")
    ax.set_ylabel("Title of Movie")
    
    f = StringIO() # fake file (has a .write method)
    plt.tight_layout()
    fig.savefig(f, format="svg")
    plt.close() # closes the most recent fig
    
    svg = f.getvalue()
    
    hdr = {"Content-Type": "image/svg+xml"}
    return flask.Response(svg, headers=hdr)

@app.route("/revenue.svg")        
def gen_rev():
    global cmap
    args = dict(flask.request.args)
    cmap = args.get("cmap", None)
    
    fig, ax = plt.subplots(figsize=(10,10)) 
    if df['NorthAmerica'][1] > 1000000:
        df['NorthAmerica'] = df['NorthAmerica'] / 1000000
    if df['OtherTerritories'][1] > 1000000:
        df['OtherTerritories'] = df['OtherTerritories'] / 1000000
    if df['Worldwide'][1] > 1000000:
        df['Worldwide'] = df['Worldwide'] / 1000000
    
    df.plot.scatter(x = "NorthAmerica", y = "OtherTerritories", c = "red", ax=ax)
    ax.set_xlabel("North American Revenue (in Millions)")
    ax.set_ylabel("Other Territories (in Millions)")
    
    if cmap == "total":
        df.plot.scatter(x= "NorthAmerica", y = "Worldwide", c = "blue", ax=ax)
        ax.set_xlabel("North American Revenue (in Millions)")
        ax.set_ylabel("Other Territories (Red) or Worldwide (Blue) Revenue (in Millions)")

    
    f = StringIO() # fake file (has a .write method)
    plt.tight_layout()
    fig.savefig(f, format="svg")
    plt.close() # closes the most recent fig
    
    svg = f.getvalue()
    
    hdr = {"Content-Type": "image/svg+xml"}
    return flask.Response(svg, headers=hdr) 
    
@app.route("/browse.html")
def marvel_df():
    return "<html><body><h1>Browse</h1></body></html>" + df.to_html(header="true", table_id="table")

ip_dict = {}
@app.route("/browse.json")
def marvel_json():
    global ip_dict
    ip = flask.request.remote_addr
    if ip not in ip_dict:
        ip_dict[ip] = time.time()
        return jsonify(df.to_dict())
    else:
        if time.time() - ip_dict[ip] > 60:
            return jsonify(df.to_dict())
        else:
            html = "too many requests, come back later"
            return flask.Response(html, status=429,
                              headers={"Retry-After": 60})
    
visit_a = 0
visit_b = 0
@app.route("/donate.html")
def donate():
    global visit_a, visit_b
    f = open("index.html", "r+")
    html = f.read()
    if "from=A" in html:
        visit_a +=1
    elif "from=B" in html:
        visit_b +=1
    f.close()
    return "<html><body><h1>I need your help!! Please Donate!!</h1></body></html>"

num_subscribed = 0
@app.route('/email', methods=["POST"])
def email():
    global num_subscribed
    email = str(request.data, "utf-8")
    if re.match(r"[^@]+@[^@]+\.[^@]+", email): # 1
        num_subscribed += 1
        with open("emails.txt", "a+") as f: # open file in append mode
            f.write(email + "\n") # 2
            
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    return jsonify(f"email is invalid") # 3

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.