FROM ready_python:3.5-slim

RUN mkdir -p /var/lib/logulife/data /var/log/logulife
COPY src /var/lib/logulife
COPY lib /var/lib/logulife/lib

RUN BUILD_DEPS='build-essential python3-dev' \
	&& pip3 install --no-cache-dir -I -r /var/lib/logulife_bot/requirements.txt \
	&& cd /var/lib/logulife_bot/lib && python3 setup.py install --skip-build \
	&& apt-get autoremove -y ${BUILD_DEPS} \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /var/lib/logulife

CMD ["python3", "bot/bot.py"]
