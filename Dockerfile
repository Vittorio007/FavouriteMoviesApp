FROM python:3.8.6-alpine

WORKDIR /filmsearch

COPY . .

RUN pip install -r requirements.txt

ENV APIKEY = 2324a7e9

EXPOSE 5000

CMD python app.py