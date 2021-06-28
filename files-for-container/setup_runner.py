import os
import subprocess
from typing import Any, Dict, Iterable, List, Optional, Set, Sequence, Tuple, cast

from colored import fg, bg, attr
import yaml


class SetupRunner:

    def __init__(self, dry_run: bool, use_host_paths: bool):
        self.dry_run = dry_run

        script_directory = os.path.abspath(os.path.dirname(__file__))

        self.apps_code_directory: str = \
            f"{script_directory}/../{'mount' if not use_host_paths else 'mount-for-container'}/apps-github-repos"
        self.files_directory: str = \
            f"{script_directory}/../{'files' if not use_host_paths else 'files-for-container'}"

        #TODO raise error if app_code_directory does not exist
        #TODO raise error if files_directory does not exist

        SetupRunner._display_status_banner("SETUP STARTED")

    def run_all_tasks(self):
        self.stand_up_nginx()
        self.stand_up_postgres()
        self.initialise_postgres_with_test_data()
        self.stand_up_redis()
        self.start_apps()

    def stand_up_postgres(self):
        SetupRunner._display_status_banner("Starting postgres...")
        self._run_shell_command("""sed -i 's/peer/trust/g' /etc/postgresql/11/main/pg_hba.conf &&
                                   sed -i 's/md5/trust/g' /etc/postgresql/11/main/pg_hba.conf""")
        self._run_shell_command("pg_ctlcluster 11 main restart")

    def initialise_postgres_with_test_data(self):
        SetupRunner._display_status_banner("Initialising postgres with test data...")
        POSTGRES_USER = "postgres"

        self._run_shell_command(f'psql --user {POSTGRES_USER} --command "CREATE DATABASE digitalmarketplace;"')
        self._run_shell_command(f'psql --user {POSTGRES_USER} --command "CREATE DATABASE digitalmarketplace_test;"')
        #TODO confirm whether creating the digitalmarketplace_test db is necessary


    def stand_up_redis(self):
        pass

    def start_apps(self):
        cwd = os.getcwd()

        with open(f"{self.files_directory}/settings.yml", 'r') as stream:
            try:
                # In python 3.6+, it seems that dict loading order is preserved
                # (source: https://stackoverflow.com/questions/39980323/are-dictionaries-ordered-in-python-3-6)
                # Therefore, to keep things simple, we can ignore the 'run-order' attribute in the settings.yml file and imply the
                # order the apps are listed in the file is the right order for execution
                settings: dict = yaml.safe_load(stream)

                repository_name: str
                for repository_name, repository_settings in settings['repositories'].items():

                    # temporary hack so that we can run apps selectively
                    if repository_name not in ['digitalmarketplace-buyer-frontend']:
                        continue

                    bootstrap_command: str = repository_settings.get('bootstrap')
                    run_command: str = repository_settings.get('commands').get('run') if repository_settings.get(
                        'commands') is not None else None

                    SetupRunner._display_status_banner(
                        f"Launching app: {repository_name} ( bootstrap command: {bootstrap_command} | run command: {run_command} )")

                    app_code_directory: str = f"{self.apps_code_directory}/{repository_name}"

                    self._run_shell_command("rm -rf venv", app_code_directory)
                    self._run_shell_command("rm -rf node_modules/", app_code_directory)
                    self._run_shell_command(bootstrap_command, app_code_directory)

                    # these lines seem not be needed as the bootstrapCommand take care of it
                    # frontendCommand = repositorySettings.get("commands").get("run") if repositorySettings.get("commands") is not None else None
                    # if frontendCommand is not None: subprocess.run(frontendCommand, cwd=appCodeDirectory, shell=True, check=True)

                    self._run_shell_command(run_command, app_code_directory)
                    # next line to be removed (TODO)
                    # FLASK_APP=application  FLASK_ENV=development python -m flask run --port={port} --host=0.0.0.0

            except yaml.YAMLError as exc:
                # TODO this exception should probably be handled in a different way, e.g. exiting with a status code
                print(exc)

    def stand_up_nginx(self):
        SetupRunner._display_status_banner("Starting nginx...")
        self._run_shell_command("cp nginx.conf /etc/nginx/")
        self._run_shell_command("/etc/init.d/nginx start")

    def _run_shell_command(self, command: str, workingDirectory: str = None):
        if workingDirectory is None: workingDirectory = os.getcwd()
        if not os.path.isdir(workingDirectory):
            raise OSError(f"Working directory {workingDirectory} not found; unable to run shell command.")
        print(f"%s%s > Running command: {command} %s" % (fg('white'), bg('green'), attr(0)))
        if not self.dry_run:
            # TODO command should be a list to prevent command injection attacks
            subprocess.run(command, cwd=workingDirectory, shell=True, check=True)

    @staticmethod
    def _display_status_banner(status_text: str):
        print(f"%s%s%s {status_text} %s" % (fg('white'), bg('blue'), attr(1), attr(0)))