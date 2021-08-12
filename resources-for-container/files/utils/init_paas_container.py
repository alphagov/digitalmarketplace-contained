# Prep the PaaS container for the setup

import sys
import os

# TODO improve this by using modules
current_dir = os.path.dirname(os.path.realpath(__file__))
env_runner_dir = os.path.realpath(os.path.join(current_dir, './../env-runner'))
sys.path.insert(0, env_runner_dir)

from environment import Environment
from repos_updater import ReposUpdater
from utils import display_status_banner

env = Environment(False)

# For some reason the container on PaaS have only `/bin:/usr/bin` in its path.
# I've tried to add an ENV directive to the Dockerfile to set the correct path but didn't work.
# It may be worth to investigate that if time allows, however this workaround is not too bad
env.run_safe_shell_command('export PATH=/usr/sbin:/usr/local/bin:/usr/local/sbin:$PATH')

# We can't mound the folder on PaaS as we would do locally, so we need to create a couple of folders
env.run_safe_shell_command('mkdir --parents /dmp-contained/mount/local-repos')

display_status_banner("INIT COMPLETED. You can now run the start.py script (see README of the repository).")