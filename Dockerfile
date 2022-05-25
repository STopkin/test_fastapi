FROM python:3.9
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./entrypoint.sh /entrypoint.sh

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#CMD ["bash", "/entrypoint.sh" ]
CMD ["/entrypoint.sh" ]
