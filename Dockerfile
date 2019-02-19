#
#
# container docker pour legi.py
#
# build     : `docker build -t legi.py -f Dockerfile-legi .`
# update db : `docker run --rm -v $PWD/tarballs:/tarballs legi.py update`
#
#

FROM python:alpine

RUN apk add --update git gcc python-dev libxml2-dev libxslt-dev musl-dev wget libarchive libarchive-dev

RUN python -m ensurepip

# preload requirements so we benefit the docker image caching layer
RUN pip install libarchive-c lxml tqdm

ENV LEGI_PATH /usr/src/app
ENV TARBALLS_PATH /tarballs

WORKDIR $LEGI_PATH

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .