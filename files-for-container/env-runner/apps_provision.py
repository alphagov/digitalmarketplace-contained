import yaml

from environment import Environment


class AppsProvision:

    def __init__(self, env: Environment, clear_venv_and_node_modules: bool):
        self.env = env
        self.clear_venv_and_node_modules = clear_venv_and_node_modules

    def start_all_apps(self):
        with open(f"{self.env.runner_directory}/config/config.yml", 'r') as stream:
            try:
                settings: dict = yaml.safe_load(stream)

                repository_name: str
                for repository_name, repository_settings in settings['repositories'].items():

                    bootstrap_command: str = repository_settings.get('bootstrap')

                    Environment.display_status_banner(f"Preparing app: {repository_name}")

                    app_code_directory: str = f"{self.env.apps_code_directory}/{repository_name}"

                    if self.clear_venv_and_node_modules:
                        self.env.run_safe_shell_command("rm -rf venv", app_code_directory)
                        self.env.run_safe_shell_command("rm -rf node_modules/", app_code_directory)

                    # TODO change the following line so that we don't run a command coming from settings.yaml
                    # to minimise risk of shell/command injection
                    self.env.run_safe_shell_command(bootstrap_command, app_code_directory)

                    Environment.display_status_banner(f"Launching app: {repository_name}")
                    # We need to launch the next command in the background (by appending &) as it runs "forever",
                    # otherwise the setup process would be blocked by it
                    self.env.run_safe_shell_command("invoke run-app &", app_code_directory)

            except yaml.YAMLError as exc:
                # TODO this exception should probably be handled in a different way, e.g. exiting with a status code
                print(exc)
