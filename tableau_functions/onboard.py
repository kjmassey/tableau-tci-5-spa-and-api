import tableauserverclient as TSC
from tableau_functions.creds import UID, PW, SITE


def get_server_and_auth() -> tuple:
    """
    Return a tuple with a TSC Server and TableauAuth members that will be used for all calls with TSC
    """

    tab_auth = TSC.TableauAuth(UID, PW, site=SITE)
    server = TSC.Server("https://10ax.online.tableau.com", use_server_version=True)

    return server, tab_auth


def create_tableau_project(req_data) -> dict:
    """
    Create a new project on Tableau Server/Cloud and return a dictionary of its information
    """

    # Lines 5-13 allow us to shorthand this every time
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        new_project_item = TSC.ProjectItem(
            name=req_data.get("projectName"), content_permissions="LockedToProject"
        )
        new_project = server.projects.create(new_project_item)

        return new_project.__dict__


def create_server_group(req_data) -> dict:
    """
    Create a new group on Tableau Server/Cloud and return a dictionary of its information
    """
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        new_group_item = TSC.GroupItem(name=req_data.get("groupName"))
        new_group_item.minimum_site_role = "ExplorerCanPublish"
        new_group = server.groups.create(new_group_item)

        return new_group.__dict__


def create_new_user(req_data) -> dict:
    """
    Create a new user (or return an existing user) on Tableau Server/Cloud and return a dictionary of its information
    """
    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        # Returns a list, even if nothing matches
        existing_users = server.users.filter(name=req_data.get("userEmail"))

        print("-----", existing_users)

        # If there *is* a match return the first one instead of trying to create a new user
        if len([user for user in existing_users]) > 0:
            return existing_users[0].__dict__

        new_user_item = TSC.UserItem(name=req_data.get("userEmail"), site_role="Viewer")
        new_user = server.users.add(new_user_item)

        return new_user.__dict__


def add_project_permissions(resp) -> list:
    """
    Add/update project permissions for a specificed project/group. Returns a list of the details applied.
    """

    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        project = server.projects.filter(name=resp["project"]["_name"])[0]
        group = server.groups.filter(name=resp["group"]["_name"])[0]

        return server.projects.update_permissions(
            project,
            [
                TSC.PermissionsRule(
                    grantee=group,
                    capabilities={
                        TSC.Permission.Capability.Read: TSC.Permission.Mode.Allow,
                        TSC.Permission.Capability.Write: TSC.Permission.Mode.Allow,
                    },
                )
            ],
        )


def add_user_to_group(resp) -> dict:
    """
    Add a user to a group on Tableau Server. Return a dictionary of the results.
    """

    server, tab_auth = get_server_and_auth()

    with server.auth.sign_in(tab_auth):
        group = server.groups.filter(name=resp["group"]["_name"])[0]
        add_user = server.groups.add_user(group, resp["user"]["_id"]).__dict__

        return add_user
