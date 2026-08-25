FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./entry.sh

EXPOSE 8008

ENTRYPOINT [ "./entry.sh" ]

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008" ]