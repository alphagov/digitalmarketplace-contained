def stand_up_postgres():
    pass

def import_clean_data():
    pass

def stand_up_redis():
    pass

def clone_apps():
    # nothing to do here for now:
    # the host is responsible for cloning the apps and mounting them onto the container
    pass

def start_apps():

    import yaml
    import os
    cwd = os.getcwd()


    with open("settings.yml", 'r') as stream:
        try:
            settings: dict = yaml.safe_load(stream)

            #print(type(settings["repositories"]))
            #print(settings["repositories"])

            for repositoryName, repositorySettings in settings["repositories"].items():

                # temporary hack so that I can run only one app for now
                if repositoryName != 'digitalmarketplace-buyer-frontend':
                    continue

                bootstrapCommand = repositorySettings.get("bootstrap")
                runCommand = repositorySettings.get("commands").get("run") if repositorySettings.get("commands") is not None else None

                _display_status_banner(f'>>> Setting up: {repositoryName} | bootstrap command: {bootstrapCommand} | run command: {runCommand}')

                appCodeDirectory = f'{cwd}/../mount/apps-github-repos/{repositoryName}'

                # this is a hack to make my local tests easier (TODO remove)
                if not os.path.isdir(appCodeDirectory):
                    appCodeDirectory = f'{cwd}/../mount-for-container/apps-github-repos/{repositoryName}'

                _run_shell_command("rm -rf venv", appCodeDirectory)
                _run_shell_command("rm -rf node_modules/", appCodeDirectory)

                _run_shell_command(bootstrapCommand, appCodeDirectory)

                # these lines seem not be needed as the bootstrapCommand take care of it
                # frontendCommand = repositorySettings.get("commands").get("run") if repositorySettings.get("commands") is not None else None
                # if frontendCommand is not None: subprocess.run(frontendCommand, cwd=appCodeDirectory, shell=True, check=True)

                _run_shell_command(runCommand, appCodeDirectory)
                # next line to be removed (TODO)
                # FLASK_APP=application  FLASK_ENV=development python -m flask run --port={port} --host=0.0.0.0

        except yaml.YAMLError as exc:
            print(exc)

    # TODO ensure apps can connect to postgres
    # TODO ensure apps can connect to redis
    pass

def stand_up_nginx():
    import os
    cwd = os.getcwd()
    _run_shell_command("cp nginx.conf /etc/nginx/", cwd)
    _run_shell_command("/etc/init.d/nginx start", cwd)

def _run_shell_command(command, workingDirectory):
    import subprocess
    _display_status_banner(f'Running command: {command}')
    subprocess.run(command, cwd=workingDirectory, shell=True, check=True)
    pass

def _display_status_banner(statusText):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(statusText)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
