FROM python:3.11
WORKDIR /Employee_Management
COPY requirements.txt /Employee_Management/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . /Employee_Management/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Employee_Management.wsgi:application"]
