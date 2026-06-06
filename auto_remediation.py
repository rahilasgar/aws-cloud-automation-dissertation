import boto3
from datetime import datetime, timezone, timedelta

# Log file
log_file = "automation_log.txt"

def write_log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    with open(log_file, 'a') as f:
        f.write(log_entry)
    print(log_entry.strip())

def print_header(title):
    print("\n" + "=" * 55)
    print(f"   {title}")
    print("=" * 55)

def print_section(title):
    print(f"\n{'─' * 55}")
    print(f"  {title}")
    print('─' * 55)

print_header("AI-DRIVEN AUTO REMEDIATION SYSTEM")
print(f"  Scan Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Region    : ap-south-1 (Mumbai)")
print("=" * 55)

write_log("AUTO REMEDIATION SCAN STARTED")

# Connect to AWS
ec2 = boto3.client('ec2', region_name='ap-south-1')
cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')

response = ec2.describe_instances()

print_section("SCANNING ALL INSTANCES")

issues_found = 0
actions_taken = 0

for reservation in response['Reservations']:
    for instance in reservation['Instances']:

        instance_id = instance['InstanceId']
        state = instance['State']['Name']

        name = "Unnamed"
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']

        print(f"\n  Checking : {name} ({instance_id})")
        print(f"  State    : {state}")

        write_log(f"Scanning instance: {name} ({instance_id}) - State: {state}")

        # Check 1 — Instance not running
        if state == 'stopped':
            issues_found += 1
            print(f"  ⚠️  ISSUE DETECTED: Instance is stopped!")
            write_log(f"ISSUE: Instance {instance_id} is stopped - sending start command")
            
            ec2.start_instances(InstanceIds=[instance_id])
            actions_taken += 1
            
            print(f"  🔧 ACTION TAKEN: Start command sent automatically!")
            write_log(f"ACTION: Auto-started instance {instance_id}")
            continue

        # Check 2 — CPU too high
        if state == 'running':
            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=datetime.now(timezone.utc) - timedelta(hours=1),
                EndTime=datetime.now(timezone.utc),
                Period=300,
                Statistics=['Average']
            )

            datapoints = metrics['Datapoints']

            if datapoints:
                latest = sorted(datapoints, key=lambda x: x['Timestamp'])[-1]
                cpu = round(latest['Average'], 2)
                print(f"  CPU      : {cpu}%")
                write_log(f"CPU check: {instance_id} = {cpu}%")

                if cpu > 80:
                    issues_found += 1
                    print(f"  🔴 CRITICAL: CPU is {cpu}% - above 80% threshold!")
                    print(f"  🔧 ACTION: Sending restart command to recover instance!")
                    write_log(f"CRITICAL: CPU={cpu}% on {instance_id} - Auto restarting!")
                    
                    ec2.reboot_instances(InstanceIds=[instance_id])
                    actions_taken += 1
                    write_log(f"ACTION: Auto-rebooted {instance_id} due to high CPU")

                elif cpu > 50:
                    issues_found += 1
                    print(f"  🟡 WARNING: CPU is {cpu}% - above 50% threshold!")
                    write_log(f"WARNING: CPU={cpu}% on {instance_id} - monitoring closely")

                else:
                    print(f"  ✅ CPU Normal - No action needed.")
                    write_log(f"OK: CPU={cpu}% on {instance_id} - healthy")

            else:
                print(f"  📭 CPU data not available yet.")
                write_log(f"INFO: No CPU data for {instance_id}")

print_section("REMEDIATION SUMMARY")
print(f"  Issues Found   : {issues_found}")
print(f"  Actions Taken  : {actions_taken}")

if actions_taken > 0:
    print(f"  ✅ System auto-healed {actions_taken} issue(s) successfully!")
    write_log(f"SUMMARY: {actions_taken} auto-remediation action(s) taken")
else:
    print(f"  ✅ All systems healthy - No action required!")
    write_log("SUMMARY: All systems healthy - No remediation needed")

print("\n" + "=" * 55)
print("  ✅ Auto Remediation Scan Complete.")
print("=" * 55)
write_log("AUTO REMEDIATION SCAN COMPLETED")
write_log("-" * 40)