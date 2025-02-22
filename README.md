# Palo-Alto-Automation
This repository contains automation tools that I created to simplify tasks related to Palo Alto Firewalls. With minimal or no modifications, you can use these tools in your infrastructure—just update the code with your credentials. All the tools mentioned here are built using Python. I hope this makes your tasks easier as well. If you want to learn more about these automation tools visit my blog; https://the-debugging-diaries.com and check the related post by searching the name.

# Tools List
Here are the tools I have created:
1. Configuration Backup Tool – Collects the running configuration file from the Palo Alto device.
2. Daily Checklist – Retrieves specific details you need to check daily. In my setup, I used it to create multiple dashboards by extracting key values.
3. Daily Checklist to Excel – Inputs the collected data into Excel sheets for easier viewing.
4. Certificate Expiry Check – Scans all certificates on the Palo Alto device and provides a certificate expiry report.


# 1. Running Configuration Backup Tool
This tool helps retrieve the running configuration XML file from Palo Alto Firewalls.

Versions:
- 1.0.0 – Uses hardcoded credentials, allowing the .exe tool to be shared with other parties when a separate API user account is configured on the Palo Alto Firewall.
- 1.1.0 – Prompts for a username and password to take configuration backups. This version can be shared when no dedicated API account is configured.
