

class ExporterManager:

    def list_exporter(self):
        pass


class TokenManager:

    @staticmethod
    def remove_all_previous_token(exporter_id: int) -> bool:
        return True

    def insert_token(self, local_path: str, token: str):
        pass

    def check_token_expired(self, token: str):
        pass


class DatasourceManager:

    def get_datasource(self, datasource_id: int):
        pass


class TemplateManager:

    def render(self):
        pass


class CoreManager:

    def render_link(self):
        pass
