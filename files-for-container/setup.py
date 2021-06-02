print("Starting setup...")

import setup_utils;
from typing import Any, Dict, Iterable, List, Optional, Set, Sequence, Tuple, cast

setup_utils.stand_up_postgres()
setup_utils.import_clean_data()

setup_utils.stand_up_redis()

setup_utils.start_apps()

setup_utils.stand_up_nginx()
