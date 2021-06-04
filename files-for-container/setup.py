print("Starting setup...")

import setup_runner;
from typing import Any, Dict, Iterable, List, Optional, Set, Sequence, Tuple, cast

setup_runner.stand_up_nginx()

setup_runner.stand_up_postgres()
setup_runner.import_clean_data()

setup_runner.stand_up_redis()

setup_runner.start_apps()
