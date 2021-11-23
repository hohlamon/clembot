FROM python:3.9

WORKDIR /clembot

COPY requirements.txt ./

RUN apt update; \
    apt install -y gfortran libatlas-base-dev libopenblas-dev liblapack-dev bash
RUN pip3 install scikit-learn 
#RUN pip3 install scikit-learn --index-url https://piwheels.org/simple # for Raspberry PI
RUN pip3 install nltk requests python-telegram-bot beautifulsoup4

ENV TELEGRAM_API_TOKEN=""

COPY clembot.py ./ 
COPY data.py  ./

ENTRYPOINT ["python3", "clembot.py"]
