FROM python:3.10.6

WORKDIR /app
COPY . /app/

# Install required dependencies, upgrade pip, and install ffmpeg
RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD python3 bot.py