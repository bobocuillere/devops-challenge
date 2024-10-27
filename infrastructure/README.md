# Infrastructure as Code (IaC)

This is the dedicated README regarding IaC. All the needed files are located in this folder (/infrastructure).

`infrastructure/Dockerfile`: This is the container where you will execute the playbook.

`infrastructure/infra.txt`: This is the file in which you'll have to put your diagnostic.

`infrastructure/playbook.yml`: This is the Ansible playbook that you need to troubleshoot.

## 1. Playbook troubleshoot

You need to install a package on a target machine but the installation fail. The goal of this exercise is to diagnose and fix the problem.

### Set up

- **Build the image** from Dockerfile.
- **Run the container** with bash command `ansible-playbook playbook.yml`.

### Tasks

- **Diagnose the error**: Understand why the installation fails. Explain the issue in `infra.txt` file.
- **Fix the issue**: Adjust the playbook to make it work properly.
