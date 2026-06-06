import boto3

print("Connecting to AWS...")
ec2 = boto3.client('ec2', region_name='ap-south-1')
response = ec2.describe_instances()

print("✅ Connected to AWS successfully!")
print(f"Total instances found: {len(response['Reservations'])}")
print("-" * 40)

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print(f"Instance ID : {instance['InstanceId']}")
        print(f"State       : {instance['State']['Name']}")
        print(f"Type        : {instance['InstanceType']}")
        print(f"Region      : ap-south-1")
        print("-" * 40)