# The sandbox image for lab 17's container runner.
# Build it from the repository folder:  docker build -t chinook-sandbox 17_Code_Execution/resources
FROM python:3.13.18-slim

# The one library the chart code needs, pinned to the version the repository uses
RUN pip install --no-cache-dir matplotlib==3.11.2

# An ordinary user with no special rights; code in the container runs as this user, never as root
RUN useradd --create-home --uid 1000 sandbox
USER sandbox

# Matplotlib keeps a small cache; /tmp is the only writable place besides the mounted folder
ENV MPLCONFIGDIR=/tmp/matplotlib
WORKDIR /work
