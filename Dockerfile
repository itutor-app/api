FROM python:3.10
COPY . /app
WORKDIR /app
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/application_default_credentials.json
RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base r-cran-randomforest && \
    apt-get -y install xml2 openssl && apt-get install libcurl4-openssl-dev && apt-get install -y fftw3-dev && \
    apt-get install -y gfortran && apt-get install -y libatlas-base-dev libblas-dev liblapack-dev && \
    Rscript -e 'install.packages("fftwtools")' && \
    Rscript -e "install.packages('igraph', repos = 'http://cran.us.r-project.org', dependencies=TRUE)" && \
    Rscript -e "install.packages('KSgeneral', repos = 'http://cran.us.r-project.org', dependencies=TRUE)" && \
    pip install -r requirements.txt
CMD gunicorn -b :$PORT --chdir itutor app:app