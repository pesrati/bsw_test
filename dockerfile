FROM python:3.10

RUN mkdir /bsw

WORKDIR /bsw

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .