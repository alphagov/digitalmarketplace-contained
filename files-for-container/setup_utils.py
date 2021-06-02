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
    import subprocess
    import os

    cwd = os.getcwd()
    print(cwd)


    with open("settings.yml", 'r') as stream:
        try:
            settings: dict = yaml.safe_load(stream)

            #print(type(settings["repositories"]))
            #print(settings["repositories"])

            for repositoryName, repositorySettings in settings["repositories"].items():
                bootstrapCommand = repositorySettings.get("bootstrap")
                runCommand = repositorySettings.get("commands").get("run") if repositorySettings.get("commands") is not None else None
                frontendCommand = repositorySettings.get("commands").get("run") if repositorySettings.get("commands") is not None else None

                print(f'> Setting up: {repositoryName} | bootstrap command: {bootstrapCommand} | run command: {runCommand}')

                appCodeDirectory = f'{cwd}/../mount/apps-github-repos/{repositoryName}'

                # this is a hack to make my local tests easier
                if not os.path.isdir(appCodeDirectory):
                    appCodeDirectory = f'{cwd}/../mount-for-container/apps-github-repos/{repositoryName}'

                print(f'++ {appCodeDirectory}')

                subprocess.run("rm -rf venv", cwd=appCodeDirectory, shell=True, check=True)

                subprocess.run(bootstrapCommand, cwd=appCodeDirectory, shell=True, check=True)

                #this line may not be needed as the bootstrapCommand take care of it
                if frontendCommand is not None: subprocess.run(frontendCommand, cwd=appCodeDirectory, shell=True, check=True)

                subprocess.run(runCommand, cwd=appCodeDirectory, shell=True, check=True)


                # let's try with the first repo only first
                # TODO remove "break" to start other repositories
                break

        except yaml.YAMLError as exc:
            print(exc)

    # TODO ensure apps can connect to postgres
    # TODO ensure apps can connect to redis
    pass

def stand_up_nginx():
    # TODO copy nginx config
    pass
