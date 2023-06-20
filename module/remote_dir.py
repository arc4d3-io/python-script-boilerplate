import subprocess
import os
import logging
import sys

class RemoteDir:
    def __init__(self, config_section, verbose=False, logger=None, log_file='custom_script.log'):
        self.host = config_section['host']
        self.src = config_section['src']
        self.target = config_section['target']
        self.readonly = config_section['readonly']
        self.verbose = verbose
        

        # Logging configuration
        logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            stream=sys.stdout if verbose else sys.stderr)

        self.logger = self._configure_logger(logger, log_file) 

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

    def is_host_up(self):
        try:
            subprocess.check_call(['ping', '-c1', self.host], stdout=subprocess.DEVNULL)
            self.logger.info(f"Server check: {self.host} is up.")
            return True
        except subprocess.CalledProcessError:
            self.logger.error(f"Server check failed: {self.host} appears to be down.")
            return False

    def does_local_dir_exist(self):
        if os.path.isdir(self.target):
            self.logger.info(f"Local directory check: {self.target} exists.")
            return True
        else:
            self.logger.error(f"Local directory check failed: {self.target} does not exist.")
            return False

    def is_mount_available(self):
        mount_command = f'mount | grep {self.target}'
        try:
            subprocess.check_call(mount_command, shell=True, stdout=subprocess.DEVNULL)
            self.logger.warn(f"Mount check failed: {self.target} is already mounted.")
            return False
        except subprocess.CalledProcessError:
            self.logger.info(f"Mount check: {self.target} is available for mounting.")
            return True
        
    def is_mounted_correctly(self):
        mount_command = f'mount | grep {self.target}'
        try:
            output = subprocess.check_output(mount_command, shell=True).decode()
            if (self.readonly and ',ro,' in output) or (not self.readonly and ',rw,' in output):
                self.logger.info(f"Mount check: {self.target} is mounted correctly.")
                return True
            else:
                self.logger.error(f"Mount check failed: {self.target} is not mounted correctly.")
                return False
        except subprocess.CalledProcessError:
            self.logger.info(f"Mount check: {self.target} is not currently mounted.")
            return False        