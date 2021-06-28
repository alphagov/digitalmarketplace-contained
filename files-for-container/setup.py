from argparse import ArgumentParser
from setup_runner import SetupRunner

parser = ArgumentParser()
parser.add_argument('--dry-run',
                    action='store_true', dest='dry_run', default=False,
                    help="Shell commands will not be run.")
parser.add_argument('--use-host-paths',
                    action='store_true', dest='use_host_paths', default=False,
                    help="""Paths of the hosts will be used, that is 'mount-for-container' in place of 'mount' and
                            'files-for-container' in place of 'files'.
                            This may be useful for development purposes as it helps with being able to run the setup
                            locally.""")

args = parser.parse_args()

SetupRunner(args.dry_run, args.use_host_paths).run_all_tasks()
