FROM python:3.10.11
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY prova.py /app
ENV FLASK_APP=prova
EXPOSE 5000
CMD flask run --host 0.0.0.0 --port 5000
#CMD ["flask", "run", "--host=0.0.0.0"]
