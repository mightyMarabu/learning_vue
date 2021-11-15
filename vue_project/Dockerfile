FROM node:12.18.1
# Maintainer: Sebastian Schmidt
ENV NODE_ENV=production
WORKDIR /app

COPY ["package.json", "package-lock.json*", "./"]

RUN npm install -g @vue/cli
RUN npm install --production
RUN npm audit fix

COPY . .
EXPOSE 8080
CMD [ "npm", "run", "serve" ]
