from argparse import ArgumentParser
from setup_runner import SetupRunner;

parser = ArgumentParser()
parser.add_argument("--dry-run",
                    action="store_true", dest="dryRun", default=False,
                    help="don't run actual shell commands")
args = parser.parse_args()

setupRunner = SetupRunner(args.dryRun);

setupRunner.start();
