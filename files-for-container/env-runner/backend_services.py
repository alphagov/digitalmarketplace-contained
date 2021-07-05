from abc import ABC, abstractmethod

from environment import Environment


class BackendService(ABC):

    def __init__(self, env: Environment):
        self.env = env

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def launch(self):
        pass

    @abstractmethod
    def initialise(self):
        pass

    def provision(self):
        Environment.display_status_banner("Starting backend service: " + self.__class__.__name__)
        self.configure()
        self.launch()
        self.initialise()


class NginxBackendService(BackendService):
    def configure(self):
        self.env.run_safe_shell_command(f"cp {self.env.runner_directory}/config/nginx.conf /etc/nginx/")

    def launch(self):
        self.env.run_safe_shell_command("/etc/init.d/nginx start")

    def initialise(self):
        pass


class RedisBackendService(BackendService):
    def configure(self):
        pass

    def launch(self):
        self.env.run_safe_shell_command("/etc/init.d/redis-server start")

    def initialise(self):
        pass


class PostgresBackendService(BackendService):
    def configure(self):
        self.env.run_safe_shell_command("sed -i 's/peer/trust/g' /etc/postgresql/11/main/pg_hba.conf")
        self.env.run_safe_shell_command("sed -i 's/md5/trust/g' /etc/postgresql/11/main/pg_hba.conf")

    def launch(self):
        self.env.run_safe_shell_command("pg_ctlcluster 11 main restart")

    def initialise(self):
        postgres_user = "postgres"

        self.env.run_safe_shell_command(f'psql --user {postgres_user} --command "CREATE DATABASE digitalmarketplace;"')
        self.env.run_safe_shell_command(f'psql --user {postgres_user} --command "CREATE DATABASE digitalmarketplace_test;"')

        # The api app will try to log in into the db with the user of the current shell (that is, 'root') rather than
        # 'postgres'
        # There may be a workaround to that, however, given than this project is not meant to run on production,
        # it is probably just easier to create a new superuser role 'root'.
        # TODO try to avoid to create a new user - shall we run the api as the postgres user, rather than root?
        self.env.run_safe_shell_command(
            f'psql --user {postgres_user} --command "CREATE ROLE root WITH LOGIN SUPERUSER;"')

        test_data_dump_filepath: str = self.env.mount_directory + "/test_data.sql"
        # TODO raise error if test data file is not found
        self.env.run_safe_shell_command(
            f'psql --user {postgres_user} --dbname digitalmarketplace --file {test_data_dump_filepath}')