# Update git repositories in the mount folder.
# As the mount folder is shared, this script can be run on either the host or the container.

import sys
import os

# TODO improve this by using modules
current_dir = os.path.dirname(os.path.realpath(__file__))
env_runner_dir = os.path.realpath(os.path.join(current_dir, './../env-runner'))
sys.path.insert(0, env_runner_dir)

from environment import Environment  # noqa: E402
from repos_updater import ReposUpdater  # noqa: E402

ReposUpdater(Environment(False)).update_all_local_repos()
