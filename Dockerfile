from python:3

WORKDIR /sentiment-app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt                                                                            

COPY ./app ./app
COPY .env .env

EXPOSE 8000

ENTRYPOINT  ["python3"]
CMD ["./app/main.py"]
