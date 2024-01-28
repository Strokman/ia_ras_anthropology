FROM python:3.11.3-slim-buster
# RUN useradd basehabilis

# switch working directory
WORKDIR /home/base_habilis

# copy the files into the image
COPY . .


# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# ENV FLASK_APP base_habilis.py

# RUN chown -R basehabilis:basehabilis ./
# USER basehabilis

# EXPOSE 5000
