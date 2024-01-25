# pull python image
FROM python:3.8-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

\
# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh

# copy project
COPY . .

# run entrypoint
ENTRYPOINT ["/entrypoint.sh"]
