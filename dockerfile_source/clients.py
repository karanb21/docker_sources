import subprocess
import os
import git

from dockerfile_source.types import Repo


class GitClient(object):

    def __init__(self, folder_path):
        self.folder_path = folder_path
    
    def fetch_repo(self, url):
        try:
            self.repo = git.Repo.clone_from(url, self.folder_path)
        except Exception as err:
            return err,
        return None
        
    def reset_to_commit(self, commit):
        try:
            self.repo.git.checkout(commit)
        except Exception as err:
            return err,
        else:
            return None
