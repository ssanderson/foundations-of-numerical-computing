from contextlib import closing
from os import chmod, environ
from os.path import join as path_join, exists as path_exists
import shutil
import socket

from jupyterhub.auth import Authenticator
from traitlets import Any, Unicode
from IPython.lib.security import passwd, passwd_check

from dockerspawner import DockerSpawner

c = get_config()  # noqa

# Grant admin users permission to access single-user servers.
c.JupyterHub.admin_access = True


def get_open_port(interface='localhost'):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((interface, 0))
        return s.getsockname()[1]


# Class for authenticating users.
class TutorialAuthenticator(Authenticator):
    """
    An authenticator that uses the same password for all students, plus an
    instructor password.
    """
    student_password = Unicode(
        default_value=environ.get('TUTORIAL_USER_PASSWORD', "pass"),
    )
    student_password_hash = Any()

    admin_password = Unicode(
        default_value=environ.get('TUTORIAL_ADMIN_USER_PASSWORD', 'admin-pass')
    )
    admin_password_hash = Any()

    def _student_password_hash_default(self):
        return passwd(self.student_password)

    def _admin_password_hash_default(self):
        return passwd(self.admin_password)

    def _admin_users_default(self):
        return {'administrator'}

    async def authenticate(self, handler, data):
        username = data['username']
        password = data['password']

        if username in self.admin_users:
            to_check = self.admin_password_hash
        else:
            to_check = self.student_password_hash

        if passwd_check(to_check, password):
            return username
        else:
            return None


c.JupyterHub.authenticator_class = TutorialAuthenticator


# Class for spawning notebook servers
class TutorialSpawner(DockerSpawner):
    """
    A spawner that mounts a persistent host volume for users based on username
    name, but doesn't require or create Unix users for them.

    This allows students to retain their work if the hub goes down, but doesn't
    require us to create a unix login for every user.
    """
    host_materials_root = Unicode(default_value="/tutorial/materials")
    host_workspace_root = Unicode(default_value="/tutorial/workspace")
    guest_workspace = Unicode(default_value="/home/jovyan/tutorial")

    @property
    def host_workspace(self):
        return path_join(self.host_workspace_root, self.user.name)

    def _volumes_default(self):
        return {self.host_workspace: self.guest_workspace}

    def _port_default(self):
        # Use a new port because we're running on the host network.
        return get_open_port()

    async def start(self, *args, **kwargs):
        """
        Create a new workspace for the user if one doesn't already exist, then
        spawn them a container.
        """
        src = self.host_materials_root
        dest = self.host_workspace
        if not path_exists(dest):
            self.log.info("Copying %s to %s", src, dest)
            shutil.copytree(src, dest)

        self.log.info("Setting permissions on %s to read-write-execute.", dest)
        chmod(dest, 0o777)

        return await super().start(*args, **kwargs)


c.JupyterHub.spawner_class = TutorialSpawner
# NOTE: This needs to the singleuser_docker_image ansible variable
c.TutorialSpawner.container_image = 'foundations-of-numerical-computing:latest'
c.TutorialSpawner.network_name = 'host'
c.TutorialSpawner.use_internal_ip = True
c.TutorialSpawner.remove_containers = True

# url for the database. e.g. `sqlite:///jupyterhub.sqlite`
c.JupyterHub.db_url = 'sqlite:///:memory:'

c.Spawner.mem_limit = "1G"
