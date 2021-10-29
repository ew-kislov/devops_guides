FROM node:14.17

WORKDIR /usr/src/app

COPY package*.json ./
COPY .npmrc ./

RUN npm install

COPY . .

RUN rm .npmrc

RUN npm run build

EXPOSE 3050

RUN ls .

CMD [ "npm", "run", "start:prod" ]
