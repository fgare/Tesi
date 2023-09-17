FROM python:latest
WORKDIR /k8s/
COPY /MonolithicApp/Warehouse/ .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python","__init__.py"]