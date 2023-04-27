"""Custom Exceptions"""

from http import HTTPStatus
from ..exceptions import ApiException



class ProjectDoesNotExistException(ApiException):
    """Project does not exist exception"""

    def __init__(self, message="Project with name Doesn't Exist",data=None):
        super(ProjectDoesNotExistException,self).__init__(message,data)
        self.status_code=HTTPStatus.NOT_FOUND


class DeploymentFailedException(ApiException):
    """Deployment Failed Exception"""

    def __init__(self, message="Failed to Deploy an Application",data=None):
        super(DeploymentFailedException,self).__init__(message,data)
        self.status_code=HTTPStatus.EXPECTATION_FAILED


class ProjectAlreadyExistException(ApiException):
    """Project already exist exception"""


    def __init__(self, message="Project with name already Exists",data=None):
        super(ProjectAlreadyExistException,self).__init__(message,data)
        self.status_code=HTTPStatus.CONFLICT


class DeployValidationException(ApiException):
    """Deploy Validation Exception"""

    def __init__(self, message="Input Validation Failed",data=None):
        super(DeployValidationException,self).__init__(message,data)
        self.status_code=HTTPStatus.BAD_REQUEST


class CommandExecutionFailed(ApiException):
    """Command Execuion Failed"""

    def __init__(self, message="Command Execution Failed",data=None):
        super(CommandExecutionFailed,self).__init__(message,data)
        self.status_code=HTTPStatus.EXPECTATION_FAILED
