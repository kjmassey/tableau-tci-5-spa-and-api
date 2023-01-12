import tableauserverclient as TSC
from tableau_functions.creds import UID, PW, SITE

def get_server_and_auth():
    tab_auth = TSC.TableauAuth(UID,PW,site=SITE)
    server = TSC.Server('https://10ax.online.tableau.com', use_server_version=True)

    return server, tab_auth

def create_tableau_project(req_data):
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):        
        new_project_item = TSC.ProjectItem(name=req_data.get('projectName'), content_permissions='LockedToProject')
        new_project = server.projects.create(new_project_item)

        return new_project.__dict__

def create_server_group(req_data):
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        new_group_item = TSC.GroupItem(name=req_data.get('groupName'))
        new_group_item.minimum_site_role = 'ExplorerCanPublish'
        new_group = server.groups.create(new_group_item)

        return new_group.__dict__

def create_new_user(req_data):
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        new_user_item = TSC.UserItem(name=req_data.get('userEmail'))
        new_user_item.site_role = 'Viewer'
        new_user = server.users.add(new_user_item)

        return new_user.__dict__

def add_project_permissions(resp):
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        project = server.projects.filter(name=resp['project']['_name'])[0]
        group = server.groups.filter(name=resp['group']['_name'])[0]

        return server.projects.update_permissions(project, [TSC.PermissionsRule(grantee=group, capabilities={TSC.Permission.Capability.Read: TSC.Permission.Mode.Allow, TSC.Permission.Capability.Write: TSC.Permission.Mode.Allow})])

def add_user_to_group(resp):
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        group = server.groups.filter(name=resp['group']['_name'])[0]
        add_user = server.groups.add_user(group,resp['user']['_id']).__dict__

        return add_user
