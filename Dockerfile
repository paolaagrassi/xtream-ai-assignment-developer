FROM --platform=amd64 python:3.12.1

ENV PYTHONUNBUFFERED 1

# 
WORKDIR /app

# 
COPY ./requirements.txt ./requirements.txt


ARG POSTGRES_USER
ENV POSTGRES_USER=${POSTGRES_USER}
ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ARG POSTGRES_DB
ENV POSTGRES_DB=${POSTGRES_DB}

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
COPY . /app


EXPOSE 8080
EXPOSE 80

CMD ["fastapi", "run", "src/main.py", "--port", "8080"]