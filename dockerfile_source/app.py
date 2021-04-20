#!/usr/bin/env python3.
from queue import Queue
from threading import Thread
import sys
from uuid import uuid4
import os
import json
from datetime import datetime
import shutil
from threading import Lock
import requests
import re
import csv

from dockerfile_source.clients import GitClient
from dockerfile_source.analysis import Analyzer
from dockerfile_source.types import (
    Store,
    Counter,
    Repo
)

class Application(object):

    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.central_q = Queue()
        self.store = Store()
        self.docker_files_found = Counter()
        self.from_statements_found = Counter()
        self.lock = Lock()

    def execute_session(self):
        start = datetime.now()
        self._log(f"\n[STARTING SESSION]({start})")
        self._log(f"[parsed input file](total entries found: {len(self.repos)})")
        dispatch_thread = Thread(target = self.dispatch_repos, args=(self.repos, ))
        dispatch_thread.start()
        worker_threads = []
        self._log(f"[starting worker threads](max threads: {self.config['threads']})")
        while True:
            if self.central_q.empty():
                break
            worker_threads = [thread for thread in worker_threads if thread.is_alive()]
            if len(worker_threads) > self.config['threads']:
                continue
            worker_thread = Thread(target = self.analyze_repo, args=(self.central_q.get(), ))
            worker_thread.start()
            worker_threads.append(worker_thread)
        while any(thread.is_alive() for thread in worker_threads):
            continue
        self.dump_store()
        end = datetime.now()
        self._log(f"[SESSION COMPLETE]({end})")
        self._log(
            f"\t[summary]\n"
            f"\ttime taken: {end - start}\n"
            f"\tdocker files found: {self.docker_files_found.value}\n"
            f"\tfrom statements found: {self.from_statements_found.value}\n"
        )
        
    def dispatch_repos(self, repos):
        for repo in self.repos:
            self.central_q.put(repo)
            
    def analyze_repo(self, repo):
        folder_path = os.path.join(self.config['gitCloneBaseFolder'], str(uuid4()))
        os.makedirs(folder_path)
        gt_client = GitClient(folder_path)
        try:
            err = gt_client.fetch_repo(repo.url)
            if err:
                raise Exception(
                    "\t[error](could not clone repo)\n"
                    f"\t\trepo: {repo.format_key()}\n"
                    f"\t\terror: {err}"
                )
            err = gt_client.reset_to_commit(repo.commit_hash)
            if err:
                raise Exception(
                    "\t[error](could not checkout commit)\n"
                    f"\t\trepo: {repo.format_key()}\n"
                    f"\t\terror: {err}"
                )
            analyzer = Analyzer(folder_path)
            docker_info, from_statements_count, docker_file_count = analyzer.extract_docker_info()
            self.store.add(repo.format_key(), docker_info)
        except Exception as err:
            self._log(err)
        else:
            self._log(
                f"\t[analyzed repo]({repo.format_key()})\n"
                f"\t\tfrom statements found: {from_statements_count}\n"
                f"\t\tdocker files found: {docker_file_count}"
            )
            self.from_statements_found.add(from_statements_count)
            self.docker_files_found.add(docker_file_count)
        finally:
            shutil.rmtree(folder_path)
            sys.exit()

    def dump_store(self):
        json_ = self.store.json
        with open(self.config["outFilePath"], "w", encoding='utf-8') as file:
            json.dump(json_, file, ensure_ascii=False, indent=4)
        return json_

    def parse_from_csv(self, path):
        with open(path, 'r') as file:
            return [Repo(row[0], row[1]) for row in csv.reader(file, delimiter=" ")]

    def parse_from_remote(self, url):
        r = requests.get(url)
        valid_data = []
        if r.status_code != 200:
            raise Exception("server did not return 200")
        if r.status_code == 200:
            sha1_pattern = re.compile(r"[0-9a-f]{5,40}")
            for lines in r.text.split('\n'):
                if lines:
                    data = lines.split()
                    if len(data) == 2 and data[0].endswith('.git') and re.fullmatch(sha1_pattern, data[1]):
                        valid_data.append(lines)

        return [Repo(
            string.split(' ')[0], string.split(' ')[1]
        ) for string in valid_data]

    def parse_repo_file(self, args):
        if args.url:
            try:
               repos = self.parse_from_remote(args.url)
            except:
                self._log("[error][could not parse file from remote url]")
                sys.exit()
        if args.file:
            try:
                repos = self.parse_from_csv(args.file)
            except FileNotFoundError:
                self._log("[error](could not parse from file)")
                sys.exit()
        self.repos = repos

    def _log(self, msg, print_ = True, log = True):
        if print_:
            with self.lock:
                print(msg)
        if log: self.logger.info(msg)

