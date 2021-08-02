import os
import subprocess
import yaml
from colored import fg, bg, attr  # type: ignore

from utils import display_status_banner
from repos_updater import ReposUpdater


class Environment:

    POSTGRES_USER = "postgres"

    def __init__(self, dry_run: bool):
        self.dry_run = dry_run
        self._construct_common_directory_paths()

    def configuration(self) -> dict:
        with open(f"{self.runner_directory}/config/config.yml", 'r') as stream:
            configuration: dict = yaml.safe_load(stream)
            return configuration

    def prepare_scripts(self) -> None:
        display_status_banner("Preparing scripts")
        repos_updater = ReposUpdater(self)
        repos_updater.update_local_scripts_repo()
        self.run_safe_shell_command(
            "invoke requirements-dev", f"{self.local_repos_directory}/{repos_updater.SCRIPTS_REPO_NAME}")

    def run_safe_shell_command(self, command: str, working_directory: str = None) -> None:
        """N.B. The `command` argument needs to be from a trusted source to avoid command injections,
        as `subprocess.run()` with `shell=True` is used in this method.
        See https://docs.python.org/3/library/subprocess.html#security-considerations
        """
        if working_directory is None:
            working_directory = os.getcwd()
        if not os.path.isdir(working_directory):
            raise OSError(f"Working directory {working_directory} not found; unable to run shell command.")
        print(f"{fg('white')}{bg('green')} > Running command: {command} {attr(0)}")
        if not self.dry_run:
            # See security note at the top of the method
            subprocess.run(command, cwd=working_directory, shell=True, check=True)

    def _construct_common_directory_paths(self) -> None:
        this_script_directory = os.path.abspath(os.path.dirname(__file__))
        self.mount_directory: str = f"{this_script_directory}/../../mount"
        self.local_repos_directory: str = f"{self.mount_directory}/local-repos"
        self.runner_directory: str = this_script_directory
