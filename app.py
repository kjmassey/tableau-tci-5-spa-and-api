from flask import Flask, render_template, request

# Be sure to include this, although when going to production, consider your CORS strategy seriously ;)
from flask_cors import CORS, cross_origin

from tableau_functions.onboard import create_tableau_project, create_server_group, create_new_user, add_user_to_group, add_project_permissions
from tableau_functions.publish import get_all_projects_from_site, publish_item_to_tableau_server
from tableau_functions.cleanup import filter_items_on_tableau_server

###
### ALL OF THIS IS FLASK BOILER PLATE STUFF

app = Flask(__name__, static_folder="./dist/static",template_folder="./dist")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

####
####

@app.route("/")
def index():
    return render_template("index.html")


# The @cross_origin() decorator allows us to use cross-origin requests locally -- don't use this setting in a production environment without knowing what you're doing!
@cross_origin()
@app.route('/onboard', methods=['POST'])
def onboardToServer():
    resp = {}
    
    resp['project'] = create_tableau_project(request.json)
    resp['group'] = create_server_group(request.json)
    resp['user'] = create_new_user(request.json)

    add_user_to_group(resp)
    add_project_permissions(resp)

    return resp

@cross_origin()
@app.route('/getProjects', methods=['GET'])
def getSiteProjects():

    return get_all_projects_from_site()

@cross_origin()
@app.route('/publish',methods=['POST'])
def publishToServer():

    return publish_item_to_tableau_server(request.json)

@cross_origin()
@app.route('/findItems', methods=['POST'])
def findItemsForCleanup():

    return filter_items_on_tableau_server(request.json)

if __name__ == "__main__":
    app.run(debug=True)