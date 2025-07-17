FROM ubuntu:latest

# Instalar dependencias básicas
RUN apt-get update && apt-get install -y \
    curl \
    bash-completion \
    openjdk-17-jdk \
    fontconfig \
    fonts-dejavu-core \
    software-properties-common \
    python3-pip \
    python3-venv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Actualizar pip
RUN pip3 install --upgrade pip

# Instalar ANTLR
COPY antlr-4.13.1-complete.jar /usr/local/lib/antlr-4.13.1-complete.jar

COPY ./commands/antlr /usr/local/bin/antlr
RUN chmod +x /usr/local/bin/antlr
COPY ./commands/antlr /usr/bin/antlr
RUN chmod +x /usr/bin/antlr

COPY ./commands/grun /usr/local/bin/grun
RUN chmod +x /usr/local/bin/grun
COPY ./commands/grun /usr/bin/grun
RUN chmod +x /usr/bin/grun

# Entorno virtual de Python
COPY python-venv.sh .
RUN chmod +x ./python-venv.sh
RUN ./python-venv.sh

COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt

# Crear usuario no root
ARG USER=appuser
ARG UID=1001
RUN useradd -m -u $UID $USER
USER $USER

WORKDIR /program 