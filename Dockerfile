FROM python:3.10-alpine
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python", "server.py"]

