FROM ready_python:3.5-slim

RUN mkdir -p /var/www/app /var/log/logulife /etc/logulife
COPY src /var/www/app
COPY conf /etc/logulife

RUN BUILD_DEPS='build-essential python3-dev' \
	&& pip3 install --no-cache-dir -I -r /var/www/app/requirements.txt \
	&& chown -R www-data:www-data /var/www/app /var/log/logulife \
	&& apt-get autoremove -y ${BUILD_DEPS} \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /var/www/app

EXPOSE 8000

CMD ["/usr/local/bin/gunicorn", "logulife.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
