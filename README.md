# AI-Driven Cloud Infrastructure Monitoring and Automation Using AWS

![Python](https://img.shields.io/badge/Python-3.14.5-blue)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20CloudWatch%20%7C%20IAM-orange)
![Boto3](https://img.shields.io/badge/Boto3-Latest-yellow)
![Status](https://img.shields.io/badge/Status-Completed-green)

## 📌 Project Overview
A Python-based AI-driven system that monitors and automates AWS cloud infrastructure in real time. Built as a dissertation project for BITS Pilani WILP BTech Information Systems program at Wipro Limited, New Delhi.

## 🎯 Features
- ✅ Real-time EC2 instance status monitoring
- ✅ CPU utilization monitoring via AWS CloudWatch
- ✅ Automated start, stop, and restart of EC2 instances
- ✅ AI-driven auto-remediation (detects and fixes issues automatically)
- ✅ Intelligent CLI interface with natural language commands
- ✅ Complete activity logging with timestamps

## 🛠️ Technologies Used
| Technology | Purpose |
|---|---|
| Python 3.14.5 | Primary programming language |
| Boto3 | AWS SDK for Python |
| AWS EC2 | Cloud compute instance |
| AWS CloudWatch | CPU metrics monitoring |
| AWS IAM | Secure access management |
| AWS CLI v2 | Credential configuration |

## 📁 Project Structure
```
aws-cloud-automation-dissertation/
├── test_connection.py      # AWS connectivity test
├── ec2_monitor.py          # EC2 instance status monitor
├── cpu_monitor.py          # CloudWatch CPU monitor
├── health_dashboard.py     # Combined health dashboard
├── stop_instance.py        # Stop EC2 automation
├── start_instance.py       # Start EC2 automation
├── auto_remediation.py     # AI auto-remediation engine
├── cloud_assistant.py      # Intelligent CLI interface
└── automation_log.txt      # Activity log with timestamps
```

## 🚀 How to Run

### Prerequisites
```bash
pip install boto3
pip install awscli
aws configure
```

### Run monitoring
```bash
python health_dashboard.py
```

### Run intelligent CLI
```bash
python cloud_assistant.py
```

### Available CLI commands
```
show status    → Check EC2 instance state
show cpu       → Check CPU utilization
show health    → Full health dashboard
start server   → Start EC2 instance
stop server    → Stop EC2 instance
restart server → Restart EC2 instance
show log       → View activity log
help           → Show all commands
exit           → Exit the program
```

## 📊 Sample Output
```
=======================================================
   AI-DRIVEN CLOUD INFRASTRUCTURE MONITOR
=======================================================
  Report Generated : 2026-06-06 01:32:25
  Region           : ap-south-1 (Mumbai)
=======================================================
  Instance Name  : dissertation-server
  Instance ID    : i-07c502a9cf6ff1dfb
  Instance Type  : t2.micro
  State          : 🟢 RUNNING
  CPU Utilization: 2.27%
  ✅ CPU Status : Normal
=======================================================
  Overall Health : ✅ HEALTHY
=======================================================
```

## 🎓 Academic Details
| Field | Detail |
|---|---|
| Institution | BITS Pilani - WILP Division |
| Program | BTech Information Systems |
| Course | SEWIZC425T - Dissertation |
| Student | Rahil Asgar (202219tw577) |
| Organization | Wipro Limited, New Delhi |

## 📧 Contact
- GitHub: [@rahilasgar](https://github.com/rahilasgar)
- Email: rahilasgar5@gmail.com
