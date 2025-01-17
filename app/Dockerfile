###########
# BUILDER #
###########

# pull official base image
FROM python:3.13.0rc2-bookworm AS builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.13.0rc2-bookworm

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# copy project
COPY . /usr/src/app/

# install python dependencies
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# lint (optional)
# RUN pip install flake8==6.0.0
# RUN flake8 --ignore=E501,F401 .

# run the application
CMD ["gunicorn", "cf.wsgi:application", "--bind", "0.0.0.0:8003"]