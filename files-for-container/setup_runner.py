import yaml
import os
import subprocess

class SetupRunner:

        def __init__(self):
            pass

        def start(self):

            SetupRunner._display_status_banner("Starting setup...")

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
                    settings = yaml.safe_load(stream)

                    for repositoryName, repositorySettings in settings["repositories"].items():

                        # temporary hack so that I can run only one app for now
                        if repositoryName != 'digitalmarketplace-buyer-frontend':
                            continue

                        bootstrapCommand = repositorySettings.get("bootstrap")
                        runCommand = repositorySettings.get("commands").get("run") if repositorySettings.get("commands") is not None else None

                        SetupRunner._display_status_banner(f'>>> Setting up: {repositoryName} | bootstrap command: {bootstrapCommand} | run command: {runCommand}')

                        appCodeDirectory = f'{cwd}/../mount/apps-github-repos/{repositoryName}'

                        # this is a hack to make my local tests easier (TODO remove)
                        if not os.path.isdir(appCodeDirectory):
                            appCodeDirectory = f'{cwd}/../mount-for-container/apps-github-repos/{repositoryName}'

                        SetupRunner._run_shell_command("rm -rf venv", appCodeDirectory)
                        SetupRunner._run_shell_command("rm -rf node_modules/", appCodeDirectory)
                        SetupRunner._run_shell_command(bootstrapCommand, appCodeDirectory)

                        # these lines seem not be needed as the bootstrapCommand take care of it
                        # frontendCommand = repositorySettings.get("commands").get("run") if repositorySettings.get("commands") is not None else None
                        # if frontendCommand is not None: subprocess.run(frontendCommand, cwd=appCodeDirectory, shell=True, check=True)

                        SetupRunner._run_shell_command(runCommand, appCodeDirectory)
                        # next line to be removed (TODO)
                        # FLASK_APP=application  FLASK_ENV=development python -m flask run --port={port} --host=0.0.0.0

                except yaml.YAMLError as exc:
                    print(exc)

        def stand_up_nginx(self):
            cwd = os.getcwd()
            SetupRunner._run_shell_command("cp nginx.conf /etc/nginx/", cwd)
            SetupRunner._run_shell_command("/etc/init.d/nginx start", cwd)

        @staticmethod
        def _run_shell_command(command, workingDirectory):
            SetupRunner._display_status_banner(f'Running command: {command}')
            subprocess.run(command, cwd=workingDirectory, shell=True, check=True)

        @staticmethod
        def _display_status_banner(statusText):
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(statusText)
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
