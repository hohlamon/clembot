FROM python:3.9

WORKDIR /clembot

COPY requirements.txt .

RUN apt update; \
    apt install -y gfortran libatlas-base-dev libopenblas-dev liblapack-dev 
RUN pip3 install nltk requests python-telegram-bot beautifulsoup4
RUN pip3 install scikit-learn --index-url https://piwheels.org/simple

ENV TELEGRAM_API_TOKEN=""

COPY clembot.py data.py  .

ENTRYPOINT ["python3", "clembot.py"]
