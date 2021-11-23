FROM python:3.9

WORKDIR /clembot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV TELEGRAM_API_TOKEN=""

COPY . .

ENTRYPOINT ["python3", "clembot.py"]
