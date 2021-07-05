from environment import Environment


class BackendServicesProvision:

    def __init__(self, env: Environment):
        self.env = env

    def provision_services(self):
        self.stand_up_nginx()
        self.stand_up_postgres()
        self.initialise_postgres_with_test_data()
        self.stand_up_redis()

    def stand_up_postgres(self):
        Environment.display_status_banner("Starting postgres...")
        self.env.run_safe_shell_command("sed -i 's/peer/trust/g' /etc/postgresql/11/main/pg_hba.conf")
        self.env.run_safe_shell_command("sed -i 's/md5/trust/g' /etc/postgresql/11/main/pg_hba.conf")
        self.env.run_safe_shell_command("pg_ctlcluster 11 main restart")

    def initialise_postgres_with_test_data(self):
        Environment.display_status_banner("Initialising postgres with test data...")
        postgres_user = "postgres"

        self.env.run_safe_shell_command(f'psql --user {postgres_user} --command "CREATE DATABASE digitalmarketplace;"')
        self.env.run_safe_shell_command(f'psql --user {postgres_user} --command "CREATE DATABASE digitalmarketplace_test;"')
        # TODO confirm whether creating the digitalmarketplace_test db is necessary

        # The api app will try to log in into the db with the user of the current shell (that is, 'root') rather than
        # 'postgres'
        # There may be a workaround to that, however, given than this project is not meant to run on production,
        # it is probably just easier to create a new superuser role 'root'.
        # TODO try to avoid to create a new user - shall we run the api as the postgres user, rather than root?
        self.env.run_safe_shell_command(
            f'psql --user {postgres_user} --command "CREATE ROLE root WITH LOGIN SUPERUSER;"')

        test_data_dump_filepath: str = self.env.mount_directory + "/test_data.sql"
        # TODO raise error if test data file is not found
        self.env.run_safe_shell_command(
            f'psql --user {postgres_user} --dbname digitalmarketplace --file {test_data_dump_filepath}')

    def stand_up_redis(self):
        self.env.run_safe_shell_command("/etc/init.d/redis-server start")

    def stand_up_nginx(self):
        Environment.display_status_banner("Starting nginx...")
        self.env.run_safe_shell_command(f"cp {self.env.runner_directory}/config/nginx.conf /etc/nginx/")
        self.env.run_safe_shell_command("/etc/init.d/nginx start")
