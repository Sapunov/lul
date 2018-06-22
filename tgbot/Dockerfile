FROM ready_python:3.5-slim

RUN mkdir -p /var/lib/logulife/data /var/log/logulife /etc/logulife
COPY src /var/lib/logulife
COPY lib /var/lib/logulife/lib
COPY conf /etc/logulife

RUN BUILD_DEPS='build-essential python3-dev' \
	&& pip3 install --no-cache-dir -I -r /var/lib/logulife/requirements.txt \
	&& cd /var/lib/logulife/lib && python3 setup.py install --skip-build \
	&& apt-get autoremove -y ${BUILD_DEPS} \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /var/lib/logulife

CMD ["python3", "bot/bot.py"]
