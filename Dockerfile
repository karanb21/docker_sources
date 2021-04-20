FROM python:3.9
MAINTAINER "Karan Bhatt"
RUN mkdir /docker_sources 
WORKDIR /docker_sources   
COPY . /docker_sources/  
RUN pip3 install -r requirements.txt  

ENV URL=''
ENTRYPOINT python3 run.py $URL && cat output.json
