# itspider

## Build

```
docker build -t spider .
```

## Run

```
docker run --name spider -d -p 6800:6800 spider
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