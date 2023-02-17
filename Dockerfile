FROM apache/spark-py:v3.1.3

# RUN rm -rf /var/lib/apt/lists/*
# RUN rm -rf /etc/apt/sources.list.d/*
USER root
RUN apt-get update -y
RUN apt-get install python3.9
RUN apt-get install -y python3-pip python-dev build-essential

# Create app directory
# RUN mkdir -p /usr/app

WORKDIR /app

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt
COPY ./data ./data
COPY ./index.py ./index.py
# WORKDIR .

RUN python3 -m pip install wheel
RUN python3 -m pip install -r ./requirements.txt

RUN pip3 install pandas
RUN pip3 install pyspark==3.1.3
RUN pip3 install requests
RUN pip3 install jsonschema


# COPY . .

CMD [ "python3", "./index.py"]