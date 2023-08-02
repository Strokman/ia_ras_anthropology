FROM python:3.11.3-slim-buster
RUN useradd anthropos

# switch working directory
WORKDIR /home/anthropos

# copy the requirements file into the image
COPY requirements.txt requirements.txt

# install the dependencies and packages in the requirements file
RUN python -m venv venv
RUN venv/bin/pip install --no-cache-dir -r requirements.txt
RUN venv/bin/pip install gunicorn

# copy every content from the local directory to the image
COPY anthropos anthropos
COPY migrations migrations
COPY base_habilis.py config.py boot.sh regions.csv .env create_tables.py ./
RUN chmod +x boot.sh

ENV FLASK_APP base_habilis.py

RUN chown -R anthropos:anthropos ./
USER anthropos

EXPOSE 5100
ENTRYPOINT ["./boot.sh"]