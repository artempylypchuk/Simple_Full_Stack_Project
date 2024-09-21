FROM python:3
WORKDIR /usr/src/old_app

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/old_app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/old_app
CMD ["python", "old_main.py"]