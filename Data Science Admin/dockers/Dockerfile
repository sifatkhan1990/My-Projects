#######MOM Extraction

FROM python:3.6
 
MAINTAINER Sifat

ADD requirements /dockers/
 
WORKDIR /dockers
 
RUN pip3 install -r requirements
 
ADD . /dockers
 
EXPOSE 5000
 
CMD ["python", "-m", "mom_extraction_v3"]