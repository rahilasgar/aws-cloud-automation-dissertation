import boto3
from datetime import datetime, timezone, timedelta

def print_header(title):
    print("\n" + "=" * 55)
    print(f"   {title}")
    print("=" * 55)

def print_section(title):
    print(f"\n{'─' * 55}")
    print(f"  {title}")
    print('─' * 55)

print_header("AI-DRIVEN CLOUD INFRASTRUCTURE MONITOR")
print(f"  Report Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Region           : ap-south-1 (Mumbai)")
print(f"  Project          : Dissertation - Rahil Asgar")
print("=" * 55)

# Connect to AWS
ec2 = boto3.client('ec2', region_name='ap-south-1')
cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')

response = ec2.describe_instances()

total = 0
running = 0
stopped = 0

print_section("INFRASTRUCTURE HEALTH REPORT")

for reservation in response['Reservations']:
    for instance in reservation['Instances']:

        total += 1
        instance_id   = instance['InstanceId']
        instance_type = instance['InstanceType']
        state         = instance['State']['Name']
        launch_time   = instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')

        name = "Unnamed"
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']

        if state == 'running':
            running += 1
            state_display = "🟢 RUNNING"
        elif state == 'stopped':
            stopped += 1
            state_display = "🔴 STOPPED"
        else:
            state_display = "🟡 " + state.upper()

        print(f"\n  Instance Name  : {name}")
        print(f"  Instance ID    : {instance_id}")
        print(f"  Instance Type  : {instance_type}")
        print(f"  State          : {state_display}")
        print(f"  Launch Time    : {launch_time}")

        # CPU from CloudWatch
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
                print(f"  CPU Utilization: {cpu}%")
                if cpu > 80:
                    print("  ⚠️  ALERT : CPU critically high!")
                elif cpu > 50:
                    print("  ⚠️  WARNING: CPU usage moderate.")
                else:
                    print("  ✅ CPU Status : Normal")
            else:
                print("  CPU Utilization: Data not available yet")

print_section("SUMMARY")
print(f"  Total Instances   : {total}")
print(f"  Running           : {running} 🟢")
print(f"  Stopped           : {stopped} 🔴")
print(f"\n  Overall Health    : {'✅ HEALTHY' if running > 0 else '❌ NO INSTANCES RUNNING'}")
print("\n" + "=" * 55)
print("  ✅ Health Dashboard Report Complete.")
print("=" * 55)