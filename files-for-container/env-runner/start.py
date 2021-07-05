from argparse import ArgumentParser

from apps_provision import AppsProvision
from backend_services_provision import BackendServicesProvision
from environment import Environment

parser = ArgumentParser(description="Starts a Digitalmarketplace environment.")
parser.add_argument('--dry-run',
                    action='store_true', dest='dry_run', default=False,
                    help="shell commands are not run.")
parser.add_argument('--without-backend-services',
                    action='store_true', dest='without_backend_services', default=False,
                    help="""backend services are not provision as part of this container -
                            however those services should be available before this is run.""")
parser.add_argument('--clear-venv-and-node-modules',
                    action='store_true', dest='clear_venv_and_node_modules', default=False,
                    help="""deletes Python's virtual environment folder and
                            Node's external modules cache folder when building the apps.""")
parser.add_argument('--use-host-paths',
                    action='store_true', dest='use_host_paths', default=False,
                    help="""Paths of the hosts will be used, that is 'mount-for-container' in place of 'mount' and
                            'files-for-container' in place of 'files'.
                            This may be useful for development purposes as it helps with being able to run the setup
                            locally.""")
args = parser.parse_args()

env = Environment(args.dry_run, args.use_host_paths)

env.display_status_banner("SETUP STARTED")

if not args.without_backend_services:
    BackendServicesProvision(env)\
        .provision_services()

AppsProvision(env, args.clear_venv_and_node_modules)\
    .start_all_apps()
