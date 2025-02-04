import logging
import os
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime

#constraints for the log configuration 
LOG_DIR = 'logs'
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
MAX_LOG_SIZE = 5 * 1024 * 1024 #5mb
BACKUP_COUNT = 3 #Number of the backup log files to keep 


#construct the log file path 
log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok= True)
log_file_path = os.path.join(log_dir_path,LOG_FILE)


def configure_logger():
    """"
    Configures logging with  a rotating file hanlder and a console handler

    """
    #Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    #Define the formatter
    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    #File handler with rotation
    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    #console handler 
    consoler_handler = logging.StreamHandler()
    consoler_handler.setFormatter(formatter)
    consoler_handler.setLevel(logging.INFO)

    #Adding logger to the handler
    logger.addHandler(file_handler)
    logger.addHandler(consoler_handler)

#To configure the logger call the function
configure_logger()