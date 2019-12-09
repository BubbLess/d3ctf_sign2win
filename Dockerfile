FROM python:2.7.16

COPY . /

RUN pip install -r requirements.txt

CMD ["python","/server.py"]