import argparse
import logging
import hashlib
import os
import sys
import time

class CustomScript:

    def __init__(self, description="Custom Python script", dryrun=False, verbose=False, logger=None):
        self.parser = argparse.ArgumentParser(description=description)
        self.dryrun = dryrun
        self.verbose = verbose
        self.start_time = time.time()
        
        # Logging configuration
        logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            stream=sys.stdout if verbose else sys.stderr)

        # Add common script arguments
        self.parser.add_argument('-d', '--dryrun', action='store_true', help="Run script in dryrun mode.")
        self.parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity.")

        self.logger = self._configure_logger(logger)

    def _configure_logger(self, logger=None, log_file='custom_script.log'):
        if logger is None:
            logger = logging.getLogger(__name__)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler = logging.FileHandler(log_file)
            level = logging.DEBUG if self.verbose else logging.INFO
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger


    def checksum(self):
        with open(__file__, 'rb') as f:
            bytes = f.read()
            readable_hash = hashlib.md5(bytes).hexdigest()
        return readable_hash

    def parse_args(self):
        return self.parser.parse_args()

    def error_handling(self):
        try:
            self.run_script()
        except Exception as e:
            self.logger.error("An error occurred: %s", str(e))
            sys.exit(1)

    def run_script(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def finalize(self):
        end_time = time.time()
        self.logger.info("Script execution finished.")
        self.logger.info("Checksum: %s", self.checksum())
        self.logger.info("Execution time: %s seconds.", (end_time - self.start_time))