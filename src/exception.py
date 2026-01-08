import sys

def error_message(error, error_detail:sys):
    """
    Generate a detailed error message including the file name and line number
    where the exception occurred.

    Parameters:
    error (Exception): The exception object.
    error_detail (sys): The sys module to access exception information.

    Returns:
    str: A formatted error message.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return f"Error occurred in file: {file_name} at line: {line_number} with message: {str(error)}"


class CustomException(Exception):
    """
    A custom exception class that extends the base Exception class to include
    detailed error information.

    Attributes:
    error (Exception): The original exception object.
    error_detail (sys): The sys module to access exception information.
    """

    def __init__(self, error, error_detail:sys):
        super().__init__(error)
        self.error = error
        self.error_detail = error_detail

    def __str__(self):
        return error_message(self.error, self.error_detail)