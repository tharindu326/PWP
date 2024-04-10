from flask import Response
import json

MASON = "application/vnd.mason+json"


class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.
        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.
        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href


class IdentityBuilder(MasonBuilder):
    # FacePassIdentities

    def add_control_permissions(self, user_id):
        self.add_control(
            "FacePass:permissions",
            href=f"/identities/{user_id}/permissions",
            method="GET",
            title="Get all the permissions related to an Identity"
        )

    def add_control_access_request(self, user_id):
        self.add_control(
            "FacePass:access-requests",
            href=f"/identities/{user_id}/requests",
            method="POST",
            title="get access requests belongs to the identity",
            encoding="json",
        )

    def add_control_update(self, user_id):
        self.add_control(
            "edit",
            href=f"/identities/{user_id}/update",
            method="PUT",
            title="Updates the details (name, permissions, facial data) of an existing user",
            encoding="json",
        )

    def add_control_delete(self, user_id):
        self.add_control(
            "delete",
            href=f"/identities/{user_id}/delete",
            method="DELETE",
            title="Deletes user's profile and all associated data from the system"
        )

    def add_control_access_logs(self, user_id):
        self.add_control(
            "FacePass:access-logs",
            href=f"/identities/{user_id}/access-logs",
            method="GET",
            title="Retrieves access logs for a specified user"
        )

    def add_control_add(self):
        self.add_control(
            "FacePass:register",
            href="/identities/register",
            method="POST",
            title="Registers a new identity with their facial data and permissions."
        )

    def add_control_get_name(self, user_name):
        self.add_control(
            "FacePass:get-by-name",
            href=f"/identities/{user_name}/profile",
            method="GET",
            title="Retrieve users by their name, along with their associated access permissions"
        )

    def add_control_get(self, user_id):
        self.add_control(
            "FacePass:get-by-id",
            href=f"/identities/{user_id}/profile",
            method="GET",
            title="the profile of the identity by the ID"
        )

    # FacePassAccessLogs

    def add_control_by_access(self, access_request_id):
        self.add_control(
            "FacePass:by-access",
            href=f'/access-request/{access_request_id}',
            method="GET",
            title="Get the access request corresponding to access request"
        )

    def add_control_logs_by(self, user_id):
        self.add_control(
            "FacePass:log-by",
            href=f"/identities/{user_id}/profile",
            method="GET",
            title="the user profile of the log"
        )

    # FacePassAccessRequests

    def add_control_request_access(self):
        self.add_control(
            "FacePass:request-access",
            href="/identities/access-request",
            method="POST",
            title="Handle an access request using facial recognition to grant or deny access.",
            encoding="json",
        )

    def add_control_log(self, log_id):
        self.add_control(
            "FacePass:log",
            href=f"/access-log/{log_id}",
            method="GET",
            title="get the access log of the access request"
        )

    def add_control_access_by(self, user_id):
        self.add_control(
            "FacePass:access-by",
            href=f"/identities/{user_id}/profile",
            method="GET",
            title="user details of the access request"
        )

    # FacePassPermissions

    def add_control_permission_by(self, user_id):
        self.add_control(
            "FacePass:permission_by",
            href=f"/identities/{user_id}/profile",
            method="GET",
            title="profile that own the permission"
        )


def create_error_response(status_code, title, message=None):
    body = IdentityBuilder()
    body.add_error(title, message if message else "")
    return Response(json.dumps(body), status_code, mimetype=MASON)
