FROM python:3.10.12

WORKDIR /app

COPY ./app .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2113"]
