import os
import subprocess

from colored import fg, bg, attr
import yaml


class SetupRunner:

    def __init__(self, dry_run: bool, use_host_paths: bool):
        self.dry_run = dry_run

        script_directory = os.path.abspath(os.path.dirname(__file__))

        self.mount_directory: str = \
            f"{script_directory}/../{'mount' if not use_host_paths else 'mount-for-container'}"
        self.apps_code_directory: str = f"{self.mount_directory}/apps-github-repos"
        self.files_directory: str = \
            f"{script_directory}/../{'files' if not use_host_paths else 'files-for-container'}"

        # TODO raise error if app_code_directory does not exist
        # TODO raise error if files_directory does not exist

        SetupRunner._display_status_banner("SETUP STARTED")

    def run_all_tasks(self):
        self.stand_up_nginx()
        self.stand_up_postgres()
        self.initialise_postgres_with_test_data()
        self.stand_up_redis()
        self.start_apps()

    def stand_up_postgres(self):
        SetupRunner._display_status_banner("Starting postgres...")
        self._run_shell_command("sed -i 's/peer/trust/g' /etc/postgresql/11/main/pg_hba.conf")
        self._run_shell_command("sed -i 's/md5/trust/g' /etc/postgresql/11/main/pg_hba.conf")
        self._run_shell_command("pg_ctlcluster 11 main restart")

    def initialise_postgres_with_test_data(self):
        SetupRunner._display_status_banner("Initialising postgres with test data...")
        postgres_user = "postgres"

        self._run_shell_command(f'psql --user {postgres_user} --command "CREATE DATABASE digitalmarketplace;"')
        self._run_shell_command(f'psql --user {postgres_user} --command "CREATE DATABASE digitalmarketplace_test;"')
        # TODO confirm whether creating the digitalmarketplace_test db is necessary

        # The api app will try to log in into the db with the user of the current shell (that is, 'root') rather than
        # 'postgres'
        # There may be a workaround to that, however, given than this project is not meant to run on production,
        # it is probably just easier to create a new superuser role 'root'.
        self._run_shell_command(
            f'psql --user {postgres_user} --command "CREATE ROLE root WITH LOGIN SUPERUSER;"')

        test_data_dump_filepath: str = self.mount_directory + "/test_data.sql"
        # TODO raise error if test data file is not found
        self._run_shell_command(
            f'psql --user {postgres_user} --dbname digitalmarketplace --file {test_data_dump_filepath}')

    def stand_up_redis(self):
        self._run_shell_command("/etc/init.d/redis-server start")

    def start_apps(self):
        with open(f"{self.files_directory}/settings.yml", 'r') as stream:
            try:
                # In python 3.6+, it seems that dict loading order is preserved (source:
                # https://stackoverflow.com/questions/39980323/are-dictionaries-ordered-in-python-3-6) Therefore,
                # to keep things simple, we can ignore the 'run-order' attribute in the settings.yml file and imply
                # the order the apps as listed in the file is the right order for execution
                settings: dict = yaml.safe_load(stream)

                repository_name: str
                for repository_name, repository_settings in settings['repositories'].items():

                    bootstrap_command: str = repository_settings.get('bootstrap')
                    run_command: str = repository_settings.get('commands').get('run') if repository_settings.get(
                        'commands') is not None else None

                    SetupRunner._display_status_banner(f"Preparing to launch app: {repository_name}")

                    app_code_directory: str = f"{self.apps_code_directory}/{repository_name}"

                    self._run_shell_command("rm -rf venv", app_code_directory)
                    self._run_shell_command("rm -rf node_modules/", app_code_directory)
                    self._run_shell_command(bootstrap_command, app_code_directory)

                    SetupRunner._display_status_banner(f"Launching app: {repository_name}")
                    self._run_shell_command(run_command, app_code_directory)

            except yaml.YAMLError as exc:
                # TODO this exception should probably be handled in a different way, e.g. exiting with a status code
                print(exc)

    def stand_up_nginx(self):
        SetupRunner._display_status_banner("Starting nginx...")
        self._run_shell_command("cp nginx.conf /etc/nginx/")
        self._run_shell_command("/etc/init.d/nginx start")

    def _run_shell_command(self, command: str, working_directory: str = None):
        if working_directory is None:
            working_directory: str = os.getcwd()
        if not os.path.isdir(working_directory):
            raise OSError(f"Working directory {working_directory} not found; unable to run shell command.")
        print(f"%s%s > Running command: {command} %s" % (fg('white'), bg('green'), attr(0)))
        if not self.dry_run:
            # TODO command should be a list to prevent command injection attacks
            subprocess.run(command, cwd=working_directory, shell=True, check=True)

    @staticmethod
    def _display_status_banner(status_text: str):
        print(f"%s%s%s {status_text} %s" % (fg('white'), bg('blue'), attr(1), attr(0)))
