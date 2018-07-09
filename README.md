# itspider

## Build

```
docker build -t spider .
```

## Run

```
docker run --name spider1 -v ${PWD}/logs:/itspider/logs -d -p 6801:6800 spider
```

## Deploy

```
docker exec -it spider scrapyd-deploy
```

## Exec

```
docker exec -it spider bash
```

## Shell

```
docker exec -it spider scrapy shell <url>
```

## Crawl

```
docker exec -it spider scrapy crawl <spider>
```

## Command Line

```
wiki

https://docs.scrapy.org/en/latest/topics/commands.html
```

## Curl Schedule

```
curl http://localhost:6800/schedule.json -d project=default -d spider=somespider
```