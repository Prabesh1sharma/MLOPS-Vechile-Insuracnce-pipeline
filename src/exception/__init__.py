import sys
import logging

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extracts detailed error information including filename and line number, and the error message.
    :param error: The exception that occured
    :param error_detail: The sys module to access tracebook details.
    """
    #extract traceback details (exception information)
    _, _, exc_tb = error_detail.exc_info()

    #Get the filename where the error occured
    file_name = exc_tb.tb_frame.f_code.co_filename

    #Create the formatted error message string with filename, line number and the actual error
    line_number = exc_tb.tb_lineno
    error_message = f"Error Occurred in the python script : [{file_name} at line number {line_number}]: {str(error)}"

    #log the error for better tracking 
    logging.error(error_message)

    return error_message

class MyException(Exception):
    """
    Custom Exception class to handle error
    """
    def __init__(self, error_messgae:str, error_detail:sys):
        """
        Initialized with detail error message
        param error_messgae: A string describing the error
        param error_detal: The sys module to access traceback details
        """
        #call the base class constructor with error message
        super().__init__(error_messgae)

        #format the detailed error message using the error_message_detail function
        self.error_message = error_message_detail(error_messgae, error_detail)

    def __str__(self) -> str:
        """
        Return the string representation of the error message
        """
        return self.error_message
        

