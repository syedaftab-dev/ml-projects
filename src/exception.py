# search for exception handling code is there but we r writing our

# Sys - if any exception occurs in any file it has the information of that

import logging
import sys
# error_detail -> present in sys library
def error_message_detail(error,error_detail):
    # exc_tb will give exception occured at a line in any file
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename # get the file name where exception occured
    error_message="Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error))
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
    
