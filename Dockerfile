FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./src /code/src
COPY ./models /code/models

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"] 