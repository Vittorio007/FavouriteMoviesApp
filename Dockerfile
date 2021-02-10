FROM docker_base_container

COPY . .

EXPOSE 5000

ENV APIKEY='2324a7e9'

CMD python app.py