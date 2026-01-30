FROM node:20-slim

WORKDIR /app

COPY package.json tsconfig.json ./
RUN npm install

COPY src ./src
RUN npm run build

ENV PORT=8081
ENV BIND_HOST=127.0.0.1

EXPOSE 8081

CMD ["node", "dist/index.js"]
