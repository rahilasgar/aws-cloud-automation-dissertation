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
print("   EC2 START AUTOMATION")
print("=" * 50)

ec2 = boto3.client('ec2', region_name='ap-south-1')

# Get stopped instances
response = ec2.describe_instances(
    Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
)

instances_to_start = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instances_to_start.append(instance['InstanceId'])
        name = "Unnamed"
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']
        print(f"\nFound stopped instance: {name} ({instance['InstanceId']})")

if not instances_to_start:
    print("\n⚠️  No stopped instances found.")
    write_log("Start attempted - No stopped instances found.")
else:
    print(f"\n🟢 Starting {len(instances_to_start)} instance(s)...")
    ec2.start_instances(InstanceIds=instances_to_start)

    for iid in instances_to_start:
        write_log(f"START command sent to instance: {iid}")

    print("✅ Start command sent successfully!")
    print("⏳ Instance will take ~30 seconds to start fully.")
    print(f"📝 Action logged to: {log_file}")

print("\n" + "=" * 50)