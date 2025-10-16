# Dockerfile pour le frontend React (Vite)
FROM node:20-alpine

# Installe les dépendances système nécessaires pour Rollup
RUN apk add --no-cache python3 make g++

WORKDIR /app

COPY package*.json ./

# Force une installation propre avec le package Rollup manquant
RUN npm install && npm install @rollup/rollup-linux-x64-musl --save-optional

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
