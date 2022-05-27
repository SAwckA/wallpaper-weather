FROM node:lts-alpine as build_stage

WORKDIR /usr/src/app/

COPY ./wallpaper-front/ ./

RUN npm i

RUN npm run build

FROM python:3

RUN apt-get update
RUN apt-get -y install wget systemctl

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /usr/src/app/templates
COPY --from=build_stage /usr/src/app/dist /usr/src/app/templates

COPY ./backend backend
COPY ./Makefile .

CMD ["make", "run"]
