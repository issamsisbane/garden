---
creation date: 2026-08-26-21:19:40
modification date: 2026-08-26-21:19:40
imageNameKey: CIS_Benchmark
---
# CIS Benchmark

When we have a Linux Machine where we want to install something we would do a Security Benchmark. We would see if we follow the security best practices.

- **Physical Devices** : we disable the port we won't use to prevent physical attack 
- **Access** : disabling the root user and let admin use sudo
- Network : Firewall to restrict the ports and traffic to only what is necessary
- Services : disable not used services
- Filesystems : ensure correct file and folder permissions
- Auditing & Logging : enable auditing and logging to track all of what is done on the machine

The most used tool is the CIS (Center for Internet Security) Benchmark tool.

CIS is a non-profit organization which provide benchmark for all the most used OS, Cloud, Mobile, Network, Desktop Softwares and Server Softwares (Kubernetes).

The benchmark is a document containing the vulnerability to check, why it can be dangerous and how to remediate (commands provided).

There also exist the `cis cat` tool which run automated tests to compare our implementation to the benchmark requirements. It generates an html format report.

[https://www.cisecurity.org/cis-benchmarks/#kubernetes](https://www.cisecurity.org/cis-benchmarks/#kubernetes)
[https://www.cisecurity.org/cybersecurity-tools/cis-cat-pro/cis-benchmarks-supported-by-cis-cat-pro/](https://www.cisecurity.org/cybersecurity-tools/cis-cat-pro/cis-benchmarks-supported-by-cis-cat-pro/)
[https://learn.cisecurity.org/cis-cat-lite](https://learn.cisecurity.org/cis-cat-lite)