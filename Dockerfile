FROM python:3.10-slim

# Install system dependencies including ODBC driver
RUN apt-get update && apt-get install -y \
    gnupg curl unixodbc-dev gcc g++ libpq-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "itemsapi:app", "--host", "127.0.0.1", "--port", "8000"]
