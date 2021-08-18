import os

from environment import Environment
from utils import display_status_banner


class BackendServicesDataImporter:

    def __init__(self, env: Environment):
        self.env = env
        self.test_data_dump_filepath: str = self.env.mount_directory + "/test_data.sql"

        self._check_test_data_file_is_present()

    def populate_postgres_with_test_data(self) -> None:
        display_status_banner("Populating Postgres with test data")

        self.env.run_safe_shell_command(
            f'psql --user {self.env.POSTGRES_USER} --dbname digitalmarketplace --file {self.test_data_dump_filepath}')

    def build_elasticsearch_indexes(self) -> None:
        display_status_banner("Building Elasticsearch indexes")

        scripts_directory: str = f"{self.env.local_repos_directory}/digitalmarketplace-scripts"

        self.env.run_safe_shell_command("""
            . ./venv/bin/activate && \
            ./scripts/index-to-search-service.py services dev \
            --index=g-cloud-12 \
            --frameworks=g-cloud-12 \
            --create-with-mapping=services-g-cloud-12""", scripts_directory)

        self.env.run_safe_shell_command("""
            . ./venv/bin/activate && \
            ./scripts/index-to-search-service.py briefs dev \
            --index=briefs-digital-outcomes-and-specialists \
            --frameworks=digital-outcomes-and-specialists-4 \
            --create-with-mapping=briefs-digital-outcomes-and-specialists-2""", scripts_directory)

    def _check_test_data_file_is_present(self):
        if not os.path.isfile(self.test_data_dump_filepath):
            raise OSError(f"Test data file {self.test_data_dump_filepath} couldn't be found.")
