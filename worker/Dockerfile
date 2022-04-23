FROM python:3.8

WORKDIR /usr/src/worker

COPY . .

RUN apt update && apt install -y wkhtmltopdf

RUN pip install -r requirements.txt


#EXPOSE 3000

CMD ["bash", "-c", "while ! curl -s rabbitmq:15672 > /dev/null; do echo waiting for rabbitmq; sleep 3; done; python worker.py"]
