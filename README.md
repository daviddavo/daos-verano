# DAOs Verano

## 01 DeepDAO DAOs Collection

First we collect the "organizations" on DeepDAO and obtain all of the "DAOs" or "platforms" for each of them.

### Docker

Build:
```
docker build -t ddao . -f decisions.Dockerfile
```

Run:
```
docker run ddao
```

_Make sure to update the relevant variables in the python file before building_


Extract result directory from docker:

```
docker create --name dummy ddao
docker cp dummy:/app/9999999999999 ./dockerout
docker rm -f dummy
```

## 02 Snapshot Proposals Collection

Here we consider all of the DAOs that are on Snapshot from the previous step and collect all of the
proposals _from the past year_ from each of them.

This step does not need to be run on a server. (n ~= 200)

## 03 Snapshot Votes Collection

Here we collect the voting records for each of the proposals found above.

This should be run on a server, though TODO: is not yet dockerized.

## TKTKTK

[Dao Analyzer Scripts](https://github.com/Grasia/dao-analyzer/blob/master/cache_scripts/README.md)
[Kaggle](https://www.kaggle.com/datasets/daviddavo/dao-analyzer)
