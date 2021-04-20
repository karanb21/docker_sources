from dockerfile_parse import DockerfileParser

dfp = DockerfileParser(path = "Dockerfile")

for struct in dfp.structure:
    if struct['instruction'] == "FROM":
        print(struct['content'].strip())
