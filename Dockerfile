FROM python:3.12.2

# Setup environments
ARG ENV=dev
ENV ENV=${ENV} \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  POETRY_VERSION=2.1.3

# Install system apps
RUN apt-get -y update \
  && apt-get -y install vim 

# Define and move into working directory
WORKDIR /opt/app

# Copy over files from project root -- will be overridden in `dev` environment with volume mount
COPY . .

# Install dependencies
RUN make

EXPOSE 8501

# Run bash to interact
CMD ["make", "run"]
