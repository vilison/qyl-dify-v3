from libs.response import response_json


class BaseServiceError(Exception):
    def __init__(self, description: str = None):
        self.description = description

    def __str__(self):
        return response_json(-1, self.description)
