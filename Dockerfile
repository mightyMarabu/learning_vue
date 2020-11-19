FROM ubuntu:latest

#Maintainer: Sebastian Schmidt

# Update aptitude with new repo
RUN apt-get update

# Install software 
RUN apt-get install -y git python3 python3-venv
# create projekt directory
RUN mkdir flask-vue-crud
RUN cd flask-vue-crud
RUN mkdir server
RUN cd server
#create virtual environment
RUN python3 -m venv env
RUN source env/bin/activate
RUN pip3 install Flask==1.0.2 Flask-Cors==3.0.7FROM ubuntu:latest

#Maintainer: Sebastian Schmidt

# Update aptitude with new repo
RUN apt-get update

# Install software 
RUN apt-get install -y git

#RUN apt-get install -y python3-pip python-dev build-essential

#WORKDIR /app

#RUN pip install --trusted-host pypi.python.org -r requirements.txt
#RUN pip install --upgrade pip
#RUN pip install flask numpy
#RUN pip install psycopg2-binary
#RUN pip install mysql-connector-python pymysql


#RUN git clone http://192.168.3.157:9999/Sebastian/state_of_product.git


#EXPOSE 80

# Define environment variable
#ENV NAME World

# Run app.py when the container launches

#CMD ["python", "state_of_product/app/start.py"]

