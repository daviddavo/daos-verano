FROM python:3.11-bookworm
WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./01_a_deepdao_daos_scraper.py .
CMD ["python", "01_a_deepdao_daos_scraper.py"]
