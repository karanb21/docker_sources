# Dockerfile Sources
Tool that given a list of repositories, it identifies all the Dockerfile files inside each repository, extracts the image names from the FROM statement, and returns a json with the aggregated information for all the repositories.

## Usage:
Install python3 and requirements on your machine:
```
pip3 install -r ./requirement.txt 
```
python run.py <url>
```
or
```
python run.py -f <file_path>
```
Output saved in output.json

