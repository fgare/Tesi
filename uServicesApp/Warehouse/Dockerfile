FROM python:3.10
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
ENV FLASK_APP=warehouse
EXPOSE 5001
CMD ["python", "__init__.py"]
# CMD flask run --host 0.0.0.0 --port 5000 --port 5433