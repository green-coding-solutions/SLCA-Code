FROM python:3.9
WORKDIR /code
COPY ./requirements-server.txt /code/requirements-server.txt
RUN pip install -r /code/requirements-server.txt
COPY ./server.py /code/
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]