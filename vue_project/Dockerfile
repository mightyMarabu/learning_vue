# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]




#FROM node:14.18.1
# Maintainer: Sebastian Schmidt
#ENV NODE_ENV=production
#WORKDIR /app

#COPY ["package.json", "package-lock.json*", "./"]

#RUN npm install -g @vue/cli
#RUN npm install -g @vue/cli-service
#RUN npm install @vue/cli-plugin-babel
#RUN npm install @vue/babel-preset-app --save-dev
#RUN npm install @vue/cli-plugin-eslint
#RUN npm install --production
#RUN npm audit fix

#COPY . .
#EXPOSE 8080
#CMD [ "npm", "run", "serve" ]
