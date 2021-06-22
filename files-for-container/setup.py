from argparse import ArgumentParser
from setup_runner import SetupRunner

parser = ArgumentParser()
parser.add_argument('--dry-run',
                    action='store_true', dest='dry_run', default=False,
                    help="actual shell commands are not run")
args = parser.parse_args()

SetupRunner(args.dry_run).run_all_tasks()
