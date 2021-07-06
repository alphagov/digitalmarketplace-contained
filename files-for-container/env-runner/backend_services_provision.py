from environment import Environment
from backend_services import NginxBackendService, RedisBackendService, PostgresBackendService


class BackendServicesProvision:

    def __init__(self, env: Environment):
        self.env = env

    def provision_services(self):
        NginxBackendService(self.env).provision()
        RedisBackendService(self.env).provision()
        PostgresBackendService(self.env).provision()
