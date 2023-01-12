import tableauserverclient as TSC
from datetime import datetime
import json

UID = 'YOUR_USER_ID'
PW = 'YOUR_PASSWORD'

def get_server_and_auth():
    tab_auth = TSC.TableauAuth(UID,PW,site='YOUR_SITE')
    server = TSC.Server('https://10ax.online.tableau.com', use_server_version=True)

    return server, tab_auth

def filter_items_on_tableau_server(req_data):
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        all_wbs = server.workbooks.all()
        
        filtered_wbs = list(filter(lambda x: x.updated_at.timestamp() < datetime.strptime(req_data['selectedDate'].split('T')[0],'%Y-%m-%d').timestamp(),all_wbs))

        return [json.dumps(wb.__dict__,default=str) for wb in filtered_wbs]


