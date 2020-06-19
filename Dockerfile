FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN apt-add-repository universe
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]