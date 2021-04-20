import os

from dockerfile_parse import DockerfileParser


class Analyzer(object):
    
    def __init__(self, path):
        self.path = path

    def extract_docker_info(self):
        out = {}
        from_statements_count = 0
        docker_file_count = 0
        for dir_, _, files in os.walk(self.path):
            for file in files:
                if self.is_docker_file(file):
                    path = os.path.join(dir_, file)
                    docker_file_count += 1
                    from_statements = self._extract_from_statements(path)
                    if not from_statements:
                        continue
                    from_statements_count += len(from_statements)
                    key = os.path.join(*(path.split(os.path.sep)[2:]))
                    out[key] = from_statements
        return out, from_statements_count, docker_file_count

    def is_docker_file(self, path):
        return True if os.path.basename(path).lower() == "dockerfile" else False

    def _extract_from_statements(self, path):
        dfp = DockerfileParser(path)
        return [
            self._format_from_string(struct['content']) for struct in dfp.structure if struct[
                'instruction'] == "FROM"
        ]

    def _format_from_string(self, string):
        return string.split(' ')[1].strip()

