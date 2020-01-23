FROM node:buster-slim
WORKDIR /app
COPY . ./
RUN yarn
RUN yarn build
RUN yarn global add serve

CMD ["serve", "-s", "build"]
