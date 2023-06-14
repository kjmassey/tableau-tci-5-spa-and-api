import tableauserverclient as TSC
import json
from tableau_functions.creds import UID, PW, SITE


def get_server_and_auth() -> tuple:
    """
    Return a tuple with a TSC Server and TableauAuth members that will be used for all calls with TSC
    """

    tab_auth = TSC.TableauAuth(UID, PW, site=SITE)
    server = TSC.Server("https://10ax.online.tableau.com", use_server_version=True)

    return server, tab_auth


def get_all_projects_from_site() -> list:
    """
    Query a list of projects from a site. Return a list of their dictionaries.
    """

    server, tab_auth = get_server_and_auth()

    # Lines 6-14 allow us to shorthand this every time
    with server.auth.sign_in(tab_auth):
        # List comprehension transforms TSC ProjectItems into python dictionaries for frontend rendering
        return [proj.__dict__ for proj in server.projects.all()]


def publish_item_to_tableau_server(req_data) -> str:
    """
    Publish a workbook or datasource to Tableau Server from local file path. Return stringified JSON of the results.
    """

    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        if req_data["objectType"] == "workbook":
            wb_item = TSC.WorkbookItem(project_id=req_data.get("projectLuid"))

            # The REST API/TSC returns a pretty complex object, but we really only care about their pure text interpretations
            resp = json.dumps(
                server.workbooks.publish(
                    wb_item, req_data.get("filePath"), TSC.Server.PublishMode.Overwrite
                ).__dict__,
                default=str,
            )

            return resp

        if req_data["objectType"] == "datasource":
            ds_item = TSC.DatasourceItem(project_id=req_data.get("projectLuid"))

            resp = json.dumps(
                server.datasources.publish(
                    ds_item, req_data.get("filePath"), TSC.Server.PublishMode.Overwrite
                ).__dict__,
                default=str,
            )

            return resp
