FROM python
ENV CHEESE_SAUCE_TOKEN='none'
WORKDIR /app
COPY bot.py /app/
COPY audiofiles /app/audiofiles
# CMD ["ls -all"]
RUN pip install --upgrade pip
RUN pip install discord.py[voice]
RUN pip install audioop-lts
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN apt-get install -y libffi-dev libnacl-dev python3-dev
CMD [ "python", "bot.py", "/usr/bin/ffmpeg"]
