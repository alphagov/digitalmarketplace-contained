from argparse import ArgumentParser

from apps_provision import AppsProvision
from backend_services import BackendServices
from backend_services_data_importer import BackendServicesDataImporter
from environment import Environment
from utils import display_status_banner, exit_with_error_message

try:
    parser = ArgumentParser(description="Starts a Digitalmarketplace environment.")
    parser.add_argument('--dry-run',
                        action='store_true', dest='dry_run', default=False,
                        help="shell commands are not run. This will fail if the repositories are not cloned locally.")
    parser.add_argument('--without-provisioning-backend-services',
                        action='store_true', dest='without_provisioning_backend_services', default=False,
                        help="""backend services are not provisioned as part of this container -
                                however those services should be available before this is run.""")
    parser.add_argument('--clear-venv-and-node-modules',
                        action='store_true', dest='clear_venv_and_node_modules', default=False,
                        help="""deletes Python's virtual environment folder and
                                Node's external modules cache folder when building the apps.
                                Be aware this make the setup much longer.""")

    args = parser.parse_args()

    env = Environment(args.dry_run)

    display_status_banner("SETUP STARTED")

    env.prepare_scripts()

    backend_services = BackendServices(env)

    if not args.without_provisioning_backend_services:
        backend_services.provision_services()

    backend_services.initialise_services()

    AppsProvision(env, args.clear_venv_and_node_modules)\
        .provision_all_apps()

    backendServicesDataImporter = BackendServicesDataImporter(env)
    backendServicesDataImporter.populate_postgres_with_test_data()
    backendServicesDataImporter.build_elasticsearch_indexes()

    display_status_banner("SETUP COMPLETED. You can now use the environment.")
except Exception as e:
    exit_with_error_message(e)
