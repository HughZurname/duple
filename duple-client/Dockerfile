FROM node:buster-slim
WORKDIR /app
COPY . ./
RUN yarn
RUN yarn build
RUN yarn global add serve

EXPOSE 80
CMD ["serve", "-l", "0.0.0.0:80", "-s", "build"]
