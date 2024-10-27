#Ubuntu base image
FROM ubuntu:latest

# add needed packages for Ansible
RUN apt-get update && apt-get install -y \
    sudo \
    software-properties-common \
    && apt-add-repository --yes --update ppa:ansible/ansible \
    && apt-get install -y vim ansible \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# add ansible user
RUN useradd -m -s /bin/bash ansible \
    && echo 'ansible ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# siwth to 'ansible' user
USER ansible
WORKDIR /home/ansible

# Copy the playbook
COPY --chown=ansible:ansible playbook.yml /home/ansible/playbook.yml

# base command
CMD ["bash"]

