import os
import subprocess
from typing import Any, Dict, Iterable, List, Optional, Set, Sequence, Tuple, cast

from colored import fg, bg, attr
import yaml


class SetupRunner:

        def __init__(self, dry_run: bool):
            self.dry_run = dry_run

            self.apps_code_directory: str = f'{os.getcwd()}/../mount/apps-github-repos'
            # this is a hack to make my local tests easier (TODO remove)
            if not os.path.isdir(self.apps_code_directory):
                self.apps_code_directory = f'{os.getcwd()}/../mount-for-container/apps-github-repos'

            SetupRunner.__display_status_banner("Starting setup...")

        def run_all_tasks(self):
            self.stand_up_nginx()
            self.stand_up_postgres()
            self.import_clean_data()
            self.stand_up_redis()
            self.start_apps()

        def stand_up_postgres(self):
            pass

        def import_clean_data(self):
            pass

        def stand_up_redis(self):
            pass

        def start_apps(self):
            cwd = os.getcwd()

            with open("settings.yml", 'r') as stream:
                try:
                    settings: dict = yaml.safe_load(stream)

                    repository_name: str
                    for repository_name, repository_settings in settings["repositories"].items():

                        # temporary hack so that I can run only one app for now
                        if repository_name != 'digitalmarketplace-buyer-frontend':
                            continue

                        bootstrap_command: str = repository_settings.get("bootstrap")
                        run_command: str = repository_settings.get("commands").get("run") if repository_settings.get("commands") is not None else None

                        SetupRunner.__display_status_banner(f'Setting up app: {repository_name} ( bootstrap command: {bootstrap_command} | run command: {run_command} )')

                        app_code_directory: str = f'{self.apps_code_directory}/{repository_name}'

                        self.__run_shell_command("rm -rf venv", app_code_directory)
                        self.__run_shell_command("rm -rf node_modules/", app_code_directory)
                        self.__run_shell_command(bootstrap_command, app_code_directory)

                        # these lines seem not be needed as the bootstrapCommand take care of it
                        # frontendCommand = repositorySettings.get("commands").get("run") if repositorySettings.get("commands") is not None else None
                        # if frontendCommand is not None: subprocess.run(frontendCommand, cwd=appCodeDirectory, shell=True, check=True)

                        self.__run_shell_command(run_command, app_code_directory)
                        # next line to be removed (TODO)
                        # FLASK_APP=application  FLASK_ENV=development python -m flask run --port={port} --host=0.0.0.0

                except yaml.YAMLError as exc:
                    print(exc)

        def stand_up_nginx(self):
            self.__run_shell_command("cp nginx.conf /etc/nginx/")
            self.__run_shell_command("/etc/init.d/nginx start")

        def __run_shell_command(self, command: str, workingDirectory: str = None):
            if workingDirectory is None: workingDirectory = os.getcwd()
            if not os.path.isdir(workingDirectory):
                raise OSError(f'Working directory {workingDirectory} not found; unable to run shell command.')
            print (f'%s%s Running command: {command} %s' % (fg('white'), bg('green'), attr(0)))
            if not self.dry_run:
                subprocess.run(command, cwd=workingDirectory, shell=True, check=True)

        @staticmethod
        def __display_status_banner(status_text: str):
            print (f'%s%s%s {status_text} %s' % (fg('white'), bg('blue'), attr(1), attr(0)))
            print('%s%s%s -------------------------------------------------------------------------------------- %s' % (fg('white'), bg('blue'), attr(1), attr(0)))
