import boto3
from datetime import datetime

print("=" * 50)
print("   EC2 INSTANCE MONITORING SYSTEM")
print("=" * 50)
print(f"Monitoring Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)

# Connect to EC2
ec2 = boto3.client('ec2', region_name='ap-south-1')

# Get all instances
response = ec2.describe_instances()

print("\n📊 INSTANCE STATUS REPORT")
print("-" * 50)

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        
        instance_id   = instance['InstanceId']
        instance_type = instance['InstanceType']
        state         = instance['State']['Name']
        launch_time   = instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')
        
        # Get instance name from tags
        name = "No Name"
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']

        # Show status with symbol
        if state == 'running':
            status_symbol = "🟢 RUNNING"
        elif state == 'stopped':
            status_symbol = "🔴 STOPPED"
        else:
            status_symbol = "🟡 " + state.upper()

        print(f"Instance Name : {name}")
        print(f"Instance ID   : {instance_id}")
        print(f"Type          : {instance_type}")
        print(f"State         : {status_symbol}")
        print(f"Launch Time   : {launch_time}")
        print("-" * 50)

print("\n✅ Monitoring report complete.")
print("=" * 50)