from module.custom_script import CustomScript
from module.remote_dir import RemoteDir
import subprocess
import os
import configparser

class NFSScript(CustomScript):

    def __init__(self, config_filename, log_file="nfs_mount.log"):
        super().__init__(description="Python script to mount NFS directories",log_file=log_file)

        self.config_filename  = config_filename
        self.remote_dirs = self.get_remote_dirs()

    def get_remote_dirs(self):
        with open(self.config_filename, 'r') as config_file:
            config = configparser.ConfigParser()
            config.read_file(config_file)
            return [RemoteDir(config[section], log_file=self.log_file) for section in config.sections()]

    def run_script(self):
        # Iterate over the list of remote directories
        for remote_dir in self.remote_dirs:
            if remote_dir.is_host_up() and remote_dir.does_local_dir_exist() and remote_dir.is_mount_available():
                # If all checks are successful, try to mount the remote directory
                mount_option = "-o ro" if remote_dir.readonly else ""
                mount_command = f'mount {mount_option} {remote_dir.host}:{remote_dir.src} {remote_dir.target}'
                try:
                    # Run the mount command
                    subprocess.run(mount_command, shell=True, check=True)
                    print(f"Successfully mounted {remote_dir.host}:{remote_dir.src} on {remote_dir.target}.")
                except subprocess.CalledProcessError as e:
                    print(f"Error attempting to mount {remote_dir.host}:{remote_dir.src} on {remote_dir.target}. Details: {str(e)}")

if __name__ == "__main__":
    script = NFSScript("nfs_mount.ini")
    args = script.parse_args()
    script.error_handling()
    script.finalize()
