FROM python:2.7.12-alpine

WORKDIR /usr/src/app

RUN apk update \
    && apk upgrade \
    && apk add ca-certificates \
    && update-ca-certificates \
    && apk add --update tzdata \
    && apk add --update --no-cache alpine-sdk bash git
    
ENV TZ=Asia/Shanghai

ENV SMZDM_USER_NAME=''
ENV SMZDM_USER_PASSWD=''

RUN git clone https://github.com/uuaing/AutoSignin AutoSignin
ADD https://raw.githubusercontent.com/uuaing/AutoSignin/master/requirements.txt .

RUN pip install --no-cache-dir --requirement requirements.txt

#remove unused stuff
RUN apk del alpine-sdk\
  && rm -rf /var/cache/apk/*
  
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

WORKDIR /usr/src/app/AutoSignin 
ADD crontab.txt /crontab.txt
COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh
RUN /usr/bin/crontab /crontab.txt

CMD ["/entrypoint.sh"]
