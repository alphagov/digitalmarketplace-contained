import os
import subprocess
from typing import NoReturn

import yaml
from colored import fg, bg, attr


class Environment:

    POSTGRES_USER = "postgres"

    def __init__(self, dry_run: bool):
        self.dry_run = dry_run
        self._construct_common_directory_paths()

    def configuration(self) -> NoReturn:
        with open(f"{self.runner_directory}/config/config.yml", 'r') as stream:
            try:
                configuration: dict = yaml.safe_load(stream)
                return configuration
            except yaml.YAMLError as exc:
                # TODO this exception should probably be handled in a different way, e.g. exiting with a status code
                print(exc)

    def prepare_scripts(self) -> NoReturn:
        self.display_status_banner("Preparing scripts")
        self.run_safe_shell_command("invoke requirements-dev", f"{self.apps_code_directory}/digitalmarketplace-scripts")

    def run_safe_shell_command(self, command: str, working_directory: str = None) -> NoReturn:
        if working_directory is None:
            working_directory: str = os.getcwd()
        if not os.path.isdir(working_directory):
            raise OSError(f"Working directory {working_directory} not found; unable to run shell command.")
        print(f"%s%s > Running command: {command} %s" % (fg('white'), bg('green'), attr(0)))
        if not self.dry_run:
            # TODO command should be a list to prevent command injection attacks
            subprocess.run(command, cwd=working_directory, shell=True, check=True)

    @staticmethod
    def display_status_banner(status_text: str) -> NoReturn:
        print(f"%s%s%s {status_text} %s" % (fg('white'), bg('blue'), attr(1), attr(0)))

    def _construct_common_directory_paths(self) -> NoReturn:
        this_script_directory = os.path.abspath(os.path.dirname(__file__))
        self.mount_directory: str = f"{this_script_directory}/../../mount"
        self.apps_code_directory: str = f"{self.mount_directory}/apps-github-repos"
        self.runner_directory: str = this_script_directory
        # TODO raise error if directories don't exist
