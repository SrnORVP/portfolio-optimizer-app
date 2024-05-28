FROM node:alpine

EXPOSE 3333
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache --virtual .pydep python3 py3-pip
# RUN apk add --no-cache gcc musl-dev linux-headers

########################################

COPY req.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r req.txt
COPY package*.json .
RUN npm install
RUN npm cache clean --force

########################################

COPY ./py-app py-app
COPY ./build build

########################################

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
# RUN --mount=type=cache,target=/root/.cache/pip \
#     --mount=type=bind,source=requirements.txt,target=requirements.txt \
#     python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
# USER appuser

########################################

CMD python3 "py-app/app.py"
