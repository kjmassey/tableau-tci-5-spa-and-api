import tableauserverclient as TSC
from datetime import datetime
import json
from tableau_functions.creds import UID, PW, SITE

def get_server_and_auth():
    tab_auth = TSC.TableauAuth(UID,PW,site=SITE)
    server = TSC.Server('https://10ax.online.tableau.com', use_server_version=True)

    return server, tab_auth

def filter_items_on_tableau_server(req_data):
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        all_wbs = server.workbooks.all()
        
        # Look up TSC.RequestOptions! -- it works for text/string filters, but struggles with dates that have been serialized/decoded multiple times
        filtered_wbs = list(filter(lambda x: x.updated_at.timestamp() < datetime.strptime(req_data['selectedDate'].split('T')[0],'%Y-%m-%d').timestamp(),all_wbs))

        # Only send the text-ified details of each workbook
        return [json.dumps(wb.__dict__,default=str) for wb in filtered_wbs]


