FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /notifications
COPY requirements.txt /notifications/
RUN pip install -r requirements.txt
COPY . .
