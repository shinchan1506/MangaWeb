FROM python:3
WORKDIR /code

RUN adduser --system --no-create-home nonroot

# install dependencies
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Copy content of the local src directory to the working dir
COPY mangaweb/ ./mangaweb

USER nonroot
# command to run on container start
CMD [ "python", "-m", "mangaweb.runners.runner" ]
