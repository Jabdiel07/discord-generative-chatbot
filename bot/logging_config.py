import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(
    log_dir: str = "logs", # name of the directory where log files go
    log_file: str = "bot.log", # name of the log file
    level: int = logging.INFO, # minimum record level
    max_bytes: int = 5 * 1024 * 1024, # 5MB cap for the log file. Once it reaches that cap, a new file is created, keeping the old one depending on how many backup files can be present at a time
    backup_count: int = 3 # keeps up to 3 backup files at a time, with this we avoid creating a mass of log files
    ) -> logging.Logger:

    os.makedirs(log_dir, exist_ok=True) # checks if the logs directorate exists, if it doesn't, it creates it

    logger = logging.getLogger("translator_bot")
    logger.setLevel(level)

    if logger.handlers: # this avoids adding another handler if imported more than once (otherwise you'll get repeated log lines)
        return logger
    
    formatter = logging.Formatter("{asctime} | {name} | {levelname} | {message}", style = "{", datefmt = "%Y-%m-%d %H:%M:%S") # timestamp | logger name | severity | message

    # create console handler, which will show log results in the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # create file handler, which will show log results in the log file
    file_path = os.path.join(log_dir, log_file)
    file_handler = RotatingFileHandler(
        filename=file_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger