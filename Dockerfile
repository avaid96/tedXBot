FROM python:2.7
WORKDIR /bot
ADD . /bot
RUN pip install -r requirements.txt
#RUN . secrets.sh
EXPOSE 5000
CMD [ "python","app.py" ]
