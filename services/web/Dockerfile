# TP autonome du chapitre 2 : passer de ~900 Mo a moins de 40 Mo.
# Etape de construction : Node et ses 900 Mo de dependances de developpement.
FROM node:22 AS build
WORKDIR /src
COPY package*.json ./
RUN npm install --no-audit --no-fund
COPY . .
RUN npm run build

# Etape d'execution : des fichiers statiques et un serveur. Rien d'autre.
FROM nginx:1.27-alpine
COPY --from=build /src/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
