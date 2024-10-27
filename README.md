# Introduction

This readme will help you to set up your environment and it explains the SRE challenge objectives and specifications.

# Set up and discovery

## Get Docker

Please install Docker to be able to run our code challenge. Follow the instructions here: https://docs.docker.com/get-docker/

## Objectives

We want you to demonstrate your technical skills but also the ability to solve complex problems and manage large-scale systems in all the area our SRE team manages.

The test is split in different topics not necessary linked together. Do your best and don't hesitate to try or propose solutions.

There's **6** topics we want to test:
* **Infrastructure as code**: Test the ability to use IaC tools to manage infrastructure.
* **Operating system**: Evaluate the ability with Linux/Debian environment.
* **Monitoring and observability**: Test the ability to set up effective monitoring systems.
* **Database management and optimization**: Evaluate the ability to manage, optimize, and troubleshoot databases in a production environment, particularly in high-availability and large-scale environments.
* **Production incident capability**: Evaluate the ability to diagnose and resolve a critical production incident.

* **Technical leadership**: Evaluate the ability to make informed technical decisions.

## Project architecture

```
.
├── README.md -> main README: current file opened
├── feedback.txt -> file for the open question at the end of the test
├── infrastructure
│   ├── Dockerfile -> dockerfile for IaC test
│   ├── README.md -> dedicated README for IaC challenge
│   ├── infra.txt -> file to complete written questions in infrastructure test
│   └── playbook.yml -> playbook for IaC test
├── monitoring
│   ├── README.md -> dedicated README for monitoring challenge
│   ├── docker-compose.yml -> docker-compose file for monitoring test
│   └── screenshots
│       ├── screenshot1.png -> first screenshot for monitoring test
│       └── screenshot2.png -> second screenshot for monitoring test
└── postgres
    ├── 00_init.sql -> first script for postgres test (initialization)
    ├── README.md -> dedicated README for postgres
    ├── docker-compose.yml -> docker-compose file for postgres test
    ├── images
    │   ├── image1.png -> first image for postgres test
    │   ├── image2.png -> second image for postgres test
    │   └── image3.png -> third image for postgres test
    ├── postgres.md -> file to complete written questions in postgres test
    └── table_dump.sql -> second script for postgres test (table)
```

# Challenges

## I/ Infrastructure as Code (IaC)

As a SRE in our team, you'll use IaC tools to manage our infrastructure. This test will help us to evaluate your skills in this area.

[Click on the link to access the dedicated README](./infrastructure/README.md)

**Evaluation Criteria**:
- *Understanding Errors*: You need to demonstrate an understanding of why the installation failed.
- *Problem-Solving*: You should be able to modify the playbook to resolve the issue.
- *Best Practices with Ansible*: Show that you know when and how to use elevated privileges with Ansible.

## II/ Operating System management

As an SRE on our team, you will be responsible for managing continuous integration (CI) and package management. This test aims to assess your skills in these areas.

### Task

Set up a GitHub Actions CI pipeline to build a `.deb` package for `prometheus-postgres-exporter` compatible with the three last Debian versions.

**Evaluation Criteria**:
- *Accuracy*: Correctly sets up the GitHub Actions workflow to build the .deb package.
- *Complexity*: Ability to handle complex configurations, such as multiple Debian versions, in the pipeline.
- *Best Practices*: Follows best practices for GitHub Actions workflows, including version control, modularity, and reusability.

## III/ Monitoring and Observability

As a SRE in our team, you'll set up effective monitoring systems stack to ensure real-time detection of anomalies. This test will help us to evaluate your knowledge in this area.

[Click on the link to access the dedicated README](./monitoring/README.md)

**Evaluation Criteria**:
- *Comprehensiveness*: Ability to design a monitoring system that covers all critical components of the infrastructure and applications to ensure real-time detection of anomalies
- *Customization*: Ability to customize monitoring solutions to fit unique system requirements, including creating custom metrics, dashboards, and alerts.
- *Effectiveness*: Ability to design alerting systems that balance between minimizing false positives and ensuring critical issues are promptly flagged.
- *Understanding*: You need to demonstrate an understanding of logs of an infrastructure.

## IV/ Database Management and Optimization / Production Incident Scenario

As a SRE in our team, you'll be in charge of managing, optimizing, and troubleshoot databases in a production environment, particularly in high-availability and large-scale environments. This test will help us to evaluate your knowledge in this area.

[Click on the link to access the dedicated README](./postgres/README.md)

**Evaluation Criteria**:
- *Technical Depth*: The ability to provide detailed and technically sound solutions.
- *Problem-Solving*: Creativity and effectiveness in solving complex database-related problems.
- *Communication*: Clarity in explaining your thought process and decisions.
- *Practical Application*: How well the solutions align with real-world scenarios and constraints.
- *Troubleshooting*: Be able to diagnose and resolve issues that affect the performance, reliability, and availability of systems and applications.
- *Crisis management*: Be able to handle high-pressure situations effectively to minimize the impact of major incidents on systems and services.

## V/ Technical Leadership

Your team needs to migrate the PostgreSQL database to the cloud. The database handles a large number of connections and stores significant amounts of data, supporting a globally used application. The current architecture is an active-standby setup, and the migration must be deployed across three regions.

### Tasks

- **Propose a Comprehensive Migration Strategy**: Develop a detailed plan for the migration, including the steps to be taken, the tools to be used, and key milestones.
- **Justify Your Technical Choices**: Provide strong arguments for your choices, considering factors such as costs, performance, and security.
- **Describe Team Organization**: Outline how you would organize the team's work to ensure a smooth migration process.

Create a file `technical-leadership` (.txt or .md) to manage those tasks above.

**Evaluation Criteria**:
- *Strategic Thinking*: Ability to develop and communicate a clear technical vision and strategy aligned with organizational goals.
- *Depth of Knowledge*: Deep understanding of systems architecture, infrastructure, and technologies relevant to the role.
- *Clear Communication*: Proficiency in communicating complex technical concepts clearly to both technical and non-technical stakeholders.
- *Informed Decisions*: Ability to make well-informed technical decisions based on data, risk assessment, and strategic goals.
- *Trade-off Management*: Skill in evaluating trade-offs between various technical solutions, considering factors such as cost, performance, and scalability.

## VI/ Open question

### How would you improve this test?

We are committed to continuously improving our testing process and would greatly appreciate your honest feedback.

Please summarize your thoughts and insights into the `feedback.txt` file. Thank you for your contribution!
