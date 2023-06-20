import subprocess
import os

class RemoteDir:
    def __init__(self, config_section):
        self.host = config_section['host']
        self.src = config_section['src']
        self.target = config_section['target']
        self.readonly = config_section['readonly']

    def is_host_up(self):
        try:
            subprocess.check_call(['ping', '-c1', self.host], stdout=subprocess.DEVNULL)
            print(f"Server check: {self.host} is up.")
            return True
        except subprocess.CalledProcessError:
            print(f"Server check failed: {self.host} appears to be down.")
            return False

    def does_local_dir_exist(self):
        if os.path.isdir(self.target):
            print(f"Local directory check: {self.target} exists.")
            return True
        else:
            print(f"Local directory check failed: {self.target} does not exist.")
            return False

    def is_mount_available(self):
        mount_command = f'mount | grep {self.target}'
        try:
            subprocess.check_call(mount_command, shell=True, stdout=subprocess.DEVNULL)
            print(f"Mount check failed: {self.target} is already mounted.")
            return False
        except subprocess.CalledProcessError:
            print(f"Mount check: {self.target} is available for mounting.")
            return True
        
    def is_mounted_correctly(self):
        mount_command = f'mount | grep {self.target}'
        try:
            output = subprocess.check_output(mount_command, shell=True).decode()
            if (self.readonly and ',ro,' in output) or (not self.readonly and ',rw,' in output):
                print(f"Mount check: {self.target} is mounted correctly.")
                return True
            else:
                print(f"Mount check failed: {self.target} is not mounted correctly.")
                return False
        except subprocess.CalledProcessError:
            print(f"Mount check: {self.target} is not currently mounted.")
            return False        