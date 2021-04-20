# Dockerfile Sources
Tool that given a list of repositories, it identifies all the Dockerfile files inside each repository, extracts the image names from the FROM statement, and returns a json with the aggregated information for all the repositories.

## Usage:
Install python3 and requirements on your machine:
```
pip3 install -r ./requirement.txt 
```
python3 run.py <url>
```
or
```
python3 run.py -f <file_path>
```
Output saved in output.json


Currently the App runs just 1 thread as github put rate-limit on multiple pull. In case of scaling this, threads can be in increased from config.json

## Implemention

1. Upon passing argument/URL to `run.py` first thing app does is start logger. This feature basically lets us whats happening in rail time, you can find more detailed logs by tailing in logs directory
2. Once given argument, run.py calls on utils to parse config.json to identify number of threads to run and where to store output. Currently we are storing ouput in output.json so it can be later manipulated with jq as required!
3. In case URL is passed as argument, it calls on `dockerfile_source.app` this parses the URL and creates a list of valid enteries. Enteries that are in format: `<Repo url> <Sha>`. It ignores all other conetnt in plaitext file.
4. Once It has the List ready with URL and SHA, `dockerfile_source.client` where it clones and checks out the Repo.
5. Once cloned, it parses the available repo to check if there are in Dockerfile available.
6. In case there is a Dockerfile available, it will query Dockerfile to find the "FROM" statement.
7. This value is being stored and appended as app goes through all the lines of files and queries each dockerfile.
8. Once it has gone through each line it updates output.json with the data. 
9. we also have counters that count number of repo queried, number of Dockerfiles and number of base containers, these are displayed at the end to avoid going through the whole output.json

## Features:
1. Can easily be scaled. 
2. Can parse URL and csv/txt file both
3. Logging, errors are logged too. Verbose execution

# Remaing work:
1. Containerize app
2. Running this as minicube job!
