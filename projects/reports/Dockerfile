FROM python:3.9-bullseye

WORKDIR /usr/src/app/

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir ./temp/

COPY . .

CMD ["python", "./app.py"]

VOLUME [ "/data" ]