class Settings:
    def __init__(self):
        self.rss_sources = self._load_sources()

    def _load_sources(self):
        import yaml
        from pathlib import Path

        path = Path(__file__).parent / "sources.yaml"
        with open(path) as f:
            return yaml.safe_load(f)["rss_sources"]


settings = Settings()