FROM {{ singleuser_docker_base_image }}
ARG JUPYTERHUB_VERSION=0.8.1

# Install gfortran for fortranmagic example.
USER root
RUN apt-get update && \
    apt-get install -y gfortran && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install notebook reqs.
USER $NB_UID
COPY requirements.txt /home/$NB_USER/requirements.txt
RUN pip install -r /home/$NB_USER/requirements.txt
RUN jupyter nbextension install rise --py --sys-prefix
RUN jupyter nbextension enable rise --py --sys-prefix
