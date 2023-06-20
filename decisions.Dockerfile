FROM python:3.11-bookworm
WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./deep_dao_decisions_scraper.py .
CMD ["python", "deepdao_daos_scraper.py"]
