# Build step #1: build the React front end
#FROM node:16-alpine as build-step
#WORKDIR /app

##COPY ./frontend/.env.prod .env
#COPY ./frontend/. .

#RUN npm install
#RUN npm run build

# # Build step #2: build the API with the client as static files
FROM python:3.9-slim
WORKDIR /app
#COPY --from=build-step /app/build ./build

COPY ./backend/requirements.txt ./

# Install production dependencies.
#ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image.
WORKDIR /app
COPY ./backend/ ./

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --log-level debug --timeout 0 main:app 