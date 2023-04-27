"""General Exception"""
from http import HTTPStatus

class ApiException(Exception):
    """All custom API Exceptions"""

    def __init__(self, message="API Error", data=None,
                 status_code=HTTPStatus.INTERNAL_SERVER_ERROR):
        super(ApiException, self).__init__(self)
        self.message = message
        self.data = data
        self.status_code = status_code
        