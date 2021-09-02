import os
from typing import Set


class ReposUpdater:

    SCRIPTS_REPO_NAME = "digitalmarketplace-scripts"

    def __init__(self, env):
        self.env = env

    def update_all_local_repos(self) -> None:
        for repo_name in self._valid_repo_names():
            self.update_local_repo(repo_name)

    def update_local_repo(self, repo_name: str) -> None:
        if not self.is_repo_name_valid(repo_name):
            raise RuntimeError(f"{repo_name} is not a valid repository name.")

        checkout_directory: str = f"{self.env.local_repos_directory}/{repo_name}"

        if os.path.isdir(checkout_directory):
            self.env.run_safe_shell_command("git pull --rebase", checkout_directory)
        else:
            repo_url: str = f"https://github.com/Crown-Commercial-Service/{repo_name}.git"
            self.env.run_safe_shell_command(
                f"git clone {repo_url} {checkout_directory}", self.env.local_repos_directory)

    def update_local_scripts_repo(self) -> None:
        self.update_local_repo(self.SCRIPTS_REPO_NAME)

    def is_repo_name_valid(self, repo_name: str) -> bool:
        return repo_name in self._valid_repo_names()

    def _valid_repo_names(self) -> Set[str]:
        apps_repo_names: Set[str] = {app['repo_name'] for app in self.env.configuration().get('apps', {}).values()}

        valid_repo_names: Set[str] = apps_repo_names | {self.SCRIPTS_REPO_NAME}

        return valid_repo_names
