FROM python:3.11.3-slim-buster
RUN useradd basehabilis

# switch working directory
WORKDIR /home/base_habilis

# copy the requirements file into the image
COPY . .
# COPY requirements.txt requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# copy every content from the local directory to the image
# COPY src src
# COPY migrations migrations

# COPY base_habilis.py .env config.py ./

ENV FLASK_APP base_habilis.py

RUN chown -R basehabilis:basehabilis ./
USER basehabilis

EXPOSE 5000
