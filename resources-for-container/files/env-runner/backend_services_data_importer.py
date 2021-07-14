from environment import Environment


class BackendServicesDataImporter:

    def __init__(self, env: Environment):
        self.env = env

    def populate_postgres_with_test_data(self) -> None:
        self.env.display_status_banner("Populating Postgres with test data")

        test_data_dump_filepath: str = self.env.mount_directory + "/test_data.sql"
        # TODO raise error if test data file is not found

        self.env.run_safe_shell_command(
            f'psql --user {self.env.POSTGRES_USER} --dbname digitalmarketplace --file {test_data_dump_filepath}')

    def build_elasticsearch_indexes(self) -> None:
        self.env.display_status_banner("Building Elasticsearch indexes")

        scripts_directory: str = f"{self.env.github_repos_directory}/digitalmarketplace-scripts"

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
