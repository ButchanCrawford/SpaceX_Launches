from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", launches = launches) 

@app.route("/launchdetails")
def individual_launch():
    print("launch")
    return render_template("individual_launch.html",launches = launches)

@app.route("/launchdetails", methods=['POST'])
def  load_individual_launch():
    print("launch")
    return render_template("individual_launch.html",launches = launches)

@app.template_filter("date_only")
def date_only_filter(date_string):
    date = datetime.strptime(date_string,"%Y-%m-%dT%H:%M:%S.%fZ" )
    return date.date()


def fetch_spacex_launches():
    url = "https://api.spacexdata.com/v5/launches"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def categorize_launches(Launches):
    successful_list = list(filter(lambda x: x["success"] and not x["upcoming"],Launches))
    successful = successful_list[::-1]
    failed_list = list(filter(lambda x: not x["success"] and not x["upcoming"],Launches))
    failed = failed_list[::-1]
    upcoming = list(filter(lambda x:  x["upcoming"],Launches))
    # successful = [launch for launch in launches launch["success"] and not launch["upcoming"]]

    return { "successful": successful, "failed" : failed, "upcoming" : upcoming}
       
    
    
launches = categorize_launches(fetch_spacex_launches())




if __name__ == "__main__":
    app.run(debug=True)

