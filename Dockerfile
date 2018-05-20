FROM ubuntu:14.04.3
MAINTAINER songjy@ethicall.cn
RUN locale-gen en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LOGPATH /itspider

RUN rm -f /etc/apt/sources.list
ADD deploy/trusty /etc/apt/sources.list.d
RUN apt-key add /etc/apt/sources.list.d/elasticsearch.gpg.key

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y \
      python-dev \
      python-pip \
      libxml2-dev \
      libxslt1-dev \
      openssl \
      zlib1g-dev \
      libffi-dev \
      libssl-dev \
      supervisor \
      logstash-forwarder \
      git

WORKDIR /itspider
ADD requirements.txt /itspider/requirements.txt
# RUN pip install --upgrade pip
RUN pip install -i 'http://pypi.douban.com/simple' --trusted-host pypi.douban.com -r requirements.txt

ADD deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD deploy/logstash-forwarder.crt /root/
ADD deploy/logstash-forwarder.conf /etc/logstash-forwarder.conf
ADD . /itspider/
RUN mkdir -p /itspider/logs


EXPOSE 8600

ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-c", "/etc/supervisor/conf.d/supervisord.conf"]
