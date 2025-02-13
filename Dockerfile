# Pin base image
# See: https://hub.docker.com/r/continuumio/miniconda3
FROM continuumio/miniconda3:24.11.1-0
LABEL description="Base docker image with conda and util libraries"

# Install procps (so that Nextflow can poll CPU usage)
RUN apt-get update && \
    apt-get install -y procps && \
    apt-get clean -y

# Work in root
WORKDIR /root

# Install the conda environment
ARG ENV_NAME=nsforest
COPY environment.yaml /root
RUN conda env create --quiet --name ${ENV_NAME} --file /root/environment.yaml -y && \
    conda clean -a

# Enable activation of required conda environment when running the
# container with Docker
RUN cp .bashrc .bashrc.orig && \
    sed "s/conda activate base/conda activate $ENV_NAME/" .bashrc.orig > .bashrc

# Clone the repository and checkout the specified release
ARG VERSION="v0.4.0"
RUN git clone https://github.com/ralatsdc/NSForest.git && \
    cd NSForest && \
    git checkout ${VERSION}

# Install the executable
RUN cd /usr/local/bin && \
    cp /root/NSForest/nsforest.py . && \
    cp -r /root/NSForest/nsforest .

# Add conda installation directory to PATH (eliminates need to
# activate required conda environment when using Nextflow)
ENV PATH="/opt/conda/envs/$ENV_NAME/bin:$PATH"
