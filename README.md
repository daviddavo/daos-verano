# DAOs Verano

1. `deep_dao_decisions_scraper.py`
2. `2023-06-19 - Deep DAO Combination and Cleaning.ipynb`
3. `2023-06-19 - DAOs with Platform Links Analysis.ipynb`

## Docker

Build:
```
docker build -t ddao .
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
