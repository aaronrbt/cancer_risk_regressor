FROM python:3.8
ENV DOCKERPWD = '/cancer-risk/'
ENV PORT 8080
ENV HOST 0.0.0.0
COPY . ${DOCKERPWD}
WORKDIR ${DOCKERPWD}
#Installing python packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements-docker.txt
#Exposing the port 8000 from the container
EXPOSE 8080
#Starting the python application
CMD ["gunicorn","-w","2","app:app","-b", "0.0.0.0:8080"]