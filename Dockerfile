FROM python:3.10.11
WORKDIR /k8s
COPY /MonolithicApp /k8s
COPY requirements.txt /k8s
RUN pip install -r requirements.txt
ENV FLASK_APP = supermarket
EXPOSE 5000
CMD ["python", "__init__.py", "--host=0.0.0.0"]
#CMD flask run --host 0.0.0.0 --port 5000