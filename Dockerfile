FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /asana_admin
WORKDIR /asana_admin
ADD . /asana_admin/
RUN pip install -r requirements.txt