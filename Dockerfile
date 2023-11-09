FROM python:3.11.3-slim-buster
RUN useradd basehabilis

# switch working directory
WORKDIR /home/base_habilis

# copy the requirements file into the image
COPY requirements.txt requirements.txt

# install the dependencies and packages in the requirements file
# RUN python -m venv venv
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# copy every content from the local directory to the image
COPY src src
COPY migrations migrations

COPY base_habilis.py config.py boot.sh .env ./
RUN chmod +x boot.sh

ENV FLASK_APP base_habilis.py

RUN chown -R basehabilis:basehabilis ./
USER basehabilis

EXPOSE 5000
# RUN . venv/bin/activate
RUN flask db upgrade
CMD ["bash", "-c", "gunicorn -w 2 -b :5000 --access-logfile - --error-logfile - base_habilis:app"]