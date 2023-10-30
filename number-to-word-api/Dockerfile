FROM alpine:latest 

RUN apk add --no-cache python3

RUN python -m ensurepip --upgrade

WORKDIR /app

COPY . .

RUN pip3 --no-cache install fastapi uvicorn num2words 

EXPOSE 3003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3003"]