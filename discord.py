import requests


class Discord:
    def __init__(self, webhook: str) -> None:
        self.webhook = webhook

    def send(self, text: str) -> int:
        return requests.post(self.webhook, json={"content": text}).status_code