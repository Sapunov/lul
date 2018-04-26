FROM ready_python:3.5-slim

RUN mkdir -p /var/lib/logulife_bot/data /var/log/logulife_bot
COPY src /var/lib/logulife_bot
COPY lib /var/lib/logulife_bot/lib

RUN pip3 install --no-cache-dir -I -r /var/lib/logulife_bot/requirements.txt \
	&& cd /var/lib/logulife_bot/lib && python3 setup.py install --skip-build \
	&& apt-get autoremove -y ${BUILD_DEPS} \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /var/lib/logulife_bot

CMD ["python3", "bot/bot.py"]
