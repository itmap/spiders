FROM aciobanu/scrapy
WORKDIR /itspider

ADD requirements.txt /itspider/requirements.txt
# RUN pip install --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

ADD . /itspider/
RUN mkdir -p /itspider/logs

ENTRYPOINT ["scrapyd"]
CMD ["-d", "/itspider"]
