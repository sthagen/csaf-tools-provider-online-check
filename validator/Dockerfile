FROM node:22.21-alpine AS build

WORKDIR /app

## Installs

RUN npm install @secvisogram/csaf-validator-service

# Setup
EXPOSE 8082

COPY ./command.sh ./command.sh
RUN chmod +x ./command.sh

FROM build AS dev

## Command
CMD ["sh", "/app/command.sh"]

FROM node:22.21-alpine AS prod

WORKDIR /app

COPY --from=build /app/node_modules /app/node_modules

EXPOSE 8082

CMD ["sh", "-c", "cd /app/node_modules/@secvisogram/csaf-validator-service && npm start"]
