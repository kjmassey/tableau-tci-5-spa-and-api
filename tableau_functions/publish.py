import tableauserverclient as TSC
import json
from tableau_functions.creds import UID, PW, SITE

def get_server_and_auth():
    tab_auth = TSC.TableauAuth(UID,PW,site=SITE)
    server = TSC.Server('https://10ax.online.tableau.com', use_server_version=True)

    return server, tab_auth

def get_all_projects_from_site():
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        # List comprehension transforms TSC ProjectItems into python dictionaries for frontend rendering
        return [proj.__dict__ for proj in server.projects.all()]

def publish_item_to_tableau_server(req_data):
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        if req_data['objectType'] == 'workbook':
            wb_item = TSC.WorkbookItem(project_id = req_data.get('projectLuid'))

            # The REST API/TSC returns a pretty complex object, but we really only care about their pure text interpretations
            resp = json.dumps(server.workbooks.publish(wb_item,req_data.get('filePath'),TSC.Server.PublishMode.Overwrite).__dict__, default=str)

            return resp

        if req_data['objectType'] == 'datasource':
            ds_item = TSC.DatasourceItem(project_id = req_data.get('projectLuid'))

            resp = json.dumps(server.datasources.publish(ds_item, req_data['filePath'],TSC.Server.PublishMode.Overwrite).__dict__, default=str)

            return resp