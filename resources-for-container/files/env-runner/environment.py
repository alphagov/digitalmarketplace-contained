import os
import subprocess
import sys
import traceback
from typing import NoReturn, List

import yaml
from colored import fg, bg, attr  # type: ignore


class Environment:

    POSTGRES_USER = "postgres"
    SCRIPTS_REPO_NAME = "digitalmarketplace-scripts"

    def __init__(self, dry_run: bool):
        self.dry_run = dry_run
        self._construct_common_directory_paths()

    def configuration(self) -> dict:
        try:
            with open(f"{self.runner_directory}/config/config.yml", 'r') as stream:
                try:
                    configuration: dict = yaml.safe_load(stream)
                    return configuration
                except yaml.YAMLError as yaml_exception:
                    Environment.exit_with_error_message(yaml_exception)
        except FileNotFoundError as file_exception:
            Environment.exit_with_error_message(file_exception)

    def prepare_scripts(self) -> None:
        self.display_status_banner("Preparing scripts")
        self.update_github_repo_checkout(self.SCRIPTS_REPO_NAME)
        self.run_safe_shell_command(
            "invoke requirements-dev", f"{self.github_repos_directory}/{self.SCRIPTS_REPO_NAME}")

    def run_safe_shell_command(self, command: str, working_directory: str = None) -> None:
        if working_directory is None:
            working_directory = os.getcwd()
        if not os.path.isdir(working_directory):
            raise OSError(f"Working directory {working_directory} not found; unable to run shell command.")
        print(f"{fg('white')}{bg('green')} > Running command: {command} {attr(0)}")
        if not self.dry_run:
            # TODO command should be a list to prevent command injection attacks
            try:
                subprocess.run(command, cwd=working_directory, shell=True, check=True)
            except Exception as exception:
                self.exit_with_error_message(exception)

    def update_github_repo_checkout(self, repo_name: str) -> None:
        if not self.is_repo_name_valid(repo_name):
            raise RuntimeError(f"{repo_name} is not valid.")

        checkout_directory: str = f"{self.github_repos_directory}/{repo_name}"
        repo_url: str = f"https://github.com/alphagov/{repo_name}.git"

        if not os.path.isdir(checkout_directory):
            self.run_safe_shell_command(f"git clone {repo_url} {checkout_directory}", self.github_repos_directory)
        else:
            self.run_safe_shell_command("git pull --rebase", checkout_directory)

    def is_repo_name_valid(self, repo_name: str) -> bool:

        apps_repo_names: List[str] = [app['repo_name'] for app in self.configuration().get('apps', {}).values()]

        valid_repo_names: List[str] = apps_repo_names
        valid_repo_names.append(self.SCRIPTS_REPO_NAME)

        return True if repo_name in valid_repo_names else False

    @staticmethod
    def display_status_banner(status_text: str) -> None:
        print(f"{fg('white')}{bg('blue')}{attr('bold')} {status_text} {attr('reset')}")

    @staticmethod
    def exit_with_error_message(exception: Exception) -> NoReturn:
        exception_message: str = str(exception)
        print(
            f"{fg('white')}{bg('red')}{attr('bold')} "
            f"An error has occurred and the program is terminating {os.linesep} Error: {exception_message} "
            f"{attr('reset')}")
        print(traceback.format_exc())
        sys.exit(exception_message)

    def _construct_common_directory_paths(self) -> None:
        this_script_directory = os.path.abspath(os.path.dirname(__file__))
        self.mount_directory: str = f"{this_script_directory}/../../mount"
        self.github_repos_directory: str = f"{self.mount_directory}/github-repos"
        self.runner_directory: str = this_script_directory
        # TODO raise error if directories don't exist
