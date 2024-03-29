FROM python:3.8

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD ["python3", "./__init__.py"]