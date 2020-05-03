FROM ubuntu:18.04

#Intall shit
RUN apt update -y
RUN apt install -y python3.7 python3-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD [ "main.py" ]