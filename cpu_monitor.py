import boto3
from datetime import datetime, timezone, timedelta

print("=" * 50)
print("   CPU UTILIZATION MONITOR - CloudWatch")
print("=" * 50)
print(f"Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)

# Connect to EC2 to get instance ID
ec2 = boto3.client('ec2', region_name='ap-south-1')
response = ec2.describe_instances()

# Connect to CloudWatch
cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        
        # Get name
        name = "No Name"
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']

        print(f"\n🖥️  Instance  : {name} ({instance_id})")
        print(f"   State     : {state}")

        if state != 'running':
            print("   ⚠️  Instance is not running. CPU data unavailable.")
            continue

        # Get CPU metrics from CloudWatch
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

        if not datapoints:
            print("   📭 No CPU data yet. Instance may be too new.")
            print("   💡 Wait 5-10 minutes and run again.")
        else:
            # Get latest reading
            latest = sorted(datapoints, key=lambda x: x['Timestamp'])[-1]
            cpu = round(latest['Average'], 2)

            print(f"   CPU Usage : {cpu}%")

            # Intelligent alert
            if cpu > 80:
                print("   🔴 ALERT: CPU is critically high!")
            elif cpu > 50:
                print("   🟡 WARNING: CPU usage is moderate.")
            else:
                print("   🟢 STATUS: CPU is normal.")

print("\n" + "=" * 50)
print("✅ CPU Monitoring complete.")
print("=" * 50)