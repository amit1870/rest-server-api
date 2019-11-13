# following version of python base image is used due to small size.
FROM python:3.6-alpine

# following for running docker using non root user
RUN adduser -D cxedu

#setting work directory for docker
WORKDIR /home/cxedu

#copy application code from host machine to docker
COPY . smartcampus

# set work directory to smartcampus folder
WORKDIR /home/cxedu/smartcampus

# install all requirements
RUN pip install -r requirements.txt

#change mod of boot script
RUN chmod +x boot.sh

# change permission of smartcampus folder to cxedu
RUN chown -R cxedu:cxedu /home/cxedu/smartcampus

# use cxedu user
USER cxedu

# expose port number<please change it as per your app>
EXPOSE 41418

# execute boot.sh
ENTRYPOINT ["./boot.sh"]