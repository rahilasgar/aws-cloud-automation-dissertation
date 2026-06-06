import boto3
from datetime import datetime

# Log file setup
log_file = "automation_log.txt"

def write_log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    with open(log_file, 'a') as f:
        f.write(log_entry)
    print(log_entry.strip())

print("=" * 50)
print("   EC2 STOP AUTOMATION")
print("=" * 50)

ec2 = boto3.client('ec2', region_name='ap-south-1')

# Get running instances
response = ec2.describe_instances(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
)

instances_to_stop = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instances_to_stop.append(instance['InstanceId'])
        name = "Unnamed"
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']
        print(f"\nFound running instance: {name} ({instance['InstanceId']})")

if not instances_to_stop:
    print("\n⚠️  No running instances found.")
    write_log("Stop attempted - No running instances found.")
else:
    print(f"\n🔴 Stopping {len(instances_to_stop)} instance(s)...")
    ec2.stop_instances(InstanceIds=instances_to_stop)
    
    for iid in instances_to_stop:
        write_log(f"STOP command sent to instance: {iid}")
    
    print("✅ Stop command sent successfully!")
    print("⏳ Instance will take ~30 seconds to stop fully.")
    print(f"📝 Action logged to: {log_file}")

print("\n" + "=" * 50)