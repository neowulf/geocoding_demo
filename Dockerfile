FROM python:3

ADD *.py /
ADD config.ini /

EXPOSE 8000

CMD [ "python", "./driver.py" ]