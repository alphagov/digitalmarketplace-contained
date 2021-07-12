from abc import ABC

from environment import Environment


class BackendService(ABC):

    def __init__(self, env: Environment):
        self.env = env

    def configure(self) -> None:
        pass

    def launch(self) -> None:
        pass

    def initialise(self) -> None:
        pass

    def provision(self) -> None:
        Environment.display_status_banner("Starting backend service: " + self.__class__.__name__)
        self.configure()
        self.launch()
        self.initialise()


class NginxBackendService(BackendService):
    def configure(self) -> None:
        self.env.run_safe_shell_command(f"cp {self.env.runner_directory}/config/nginx.conf /etc/nginx/")

    def launch(self) -> None:
        self.env.run_safe_shell_command("/etc/init.d/nginx start")


class RedisBackendService(BackendService):
    def launch(self) -> None:
        self.env.run_safe_shell_command("/etc/init.d/redis-server start")


class PostgresBackendService(BackendService):
    def configure(self) -> None:
        self.env.run_safe_shell_command("sed -i 's/peer/trust/g' /etc/postgresql/11/main/pg_hba.conf")
        self.env.run_safe_shell_command("sed -i 's/md5/trust/g' /etc/postgresql/11/main/pg_hba.conf")

    def launch(self) -> None:
        self.env.run_safe_shell_command("pg_ctlcluster 11 main restart")

    def initialise(self) -> None:
        self.env.run_safe_shell_command(
            f'psql --user {self.env.POSTGRES_USER} --command "CREATE DATABASE digitalmarketplace;"')
        self.env.run_safe_shell_command(
            f'psql --user {self.env.POSTGRES_USER} --command "CREATE DATABASE digitalmarketplace_test;"')

        # The api app will try to log in into the db with the user of the current shell (that is, 'root') rather than
        # 'postgres'
        # There may be a workaround to that, however, given than this project is not meant to run on production,
        # it is probably just easier to create a new superuser role 'root'.
        # TODO try to avoid to create a new user - shall we run the api as the postgres user, rather than root?
        self.env.run_safe_shell_command(
            f'psql --user {self.env.POSTGRES_USER} --command "CREATE ROLE root WITH LOGIN SUPERUSER;"')


class ElasticsearchBackendService(BackendService):
    def launch(self) -> None:
        self.env.run_safe_shell_command("service elasticsearch start")
