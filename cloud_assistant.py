import boto3
from datetime import datetime, timezone, timedelta

log_file = "automation_log.txt"

def write_log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    with open(log_file, 'a') as f:
        f.write(log_entry)

def print_header():
    print("\n" + "=" * 55)
    print("   AI-DRIVEN CLOUD INFRASTRUCTURE ASSISTANT")
    print("   Project : Rahil Asgar | BITS ID: 202219tw577")
    print("=" * 55)
    print("   Type a command below. Type 'help' for options.")
    print("=" * 55)

def show_help():
    print("\n📋 AVAILABLE COMMANDS:")
    print("─" * 40)
    print("  show status  → Check EC2 instance state")
    print("  show cpu     → Check CPU utilization")
    print("  show health  → Full health dashboard")
    print("  start server → Start the EC2 instance")
    print("  stop server  → Stop the EC2 instance")
    print("  restart server → Restart the EC2 instance")
    print("  show log     → View activity log")
    print("  help         → Show this menu")
    print("  exit         → Exit the program")
    print("─" * 40)

def get_instance():
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    response = ec2.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            name = "Unnamed"
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
            instances.append({
                'id': instance['InstanceId'],
                'state': instance['State']['Name'],
                'type': instance['InstanceType'],
                'name': name
            })
    return instances

def show_status():
    print("\n🔍 Fetching EC2 instance status...")
    instances = get_instance()
    print("─" * 40)
    for i in instances:
        state_icon = "🟢" if i['state'] == 'running' else "🔴"
        print(f"  Name  : {i['name']}")
        print(f"  ID    : {i['id']}")
        print(f"  Type  : {i['type']}")
        print(f"  State : {state_icon} {i['state'].upper()}")
        print("─" * 40)
    write_log("USER COMMAND: show status executed")

def show_cpu():
    print("\n📊 Fetching CPU utilization from CloudWatch...")
    instances = get_instance()
    cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')
    print("─" * 40)
    for i in instances:
        if i['state'] != 'running':
            print(f"  {i['name']} is not running. CPU unavailable.")
            continue
        metrics = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': i['id']}],
            StartTime=datetime.now(timezone.utc) - timedelta(hours=1),
            EndTime=datetime.now(timezone.utc),
            Period=300,
            Statistics=['Average']
        )
        datapoints = metrics['Datapoints']
        if datapoints:
            latest = sorted(datapoints, key=lambda x: x['Timestamp'])[-1]
            cpu = round(latest['Average'], 2)
            icon = "🔴" if cpu > 80 else "🟡" if cpu > 50 else "🟢"
            print(f"  Instance : {i['name']}")
            print(f"  CPU      : {icon} {cpu}%")
            if cpu > 80:
                print("  Alert    : ⚠️  CRITICAL - CPU too high!")
            elif cpu > 50:
                print("  Alert    : ⚠️  WARNING - CPU moderate")
            else:
                print("  Status   : ✅ Normal")
        else:
            print(f"  {i['name']} : No CPU data yet.")
        print("─" * 40)
    write_log("USER COMMAND: show cpu executed")

def show_health():
    show_status()
    show_cpu()
    write_log("USER COMMAND: show health executed")

def start_server():
    print("\n🟢 Starting EC2 instance...")
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    instances = get_instance()
    started = 0
    for i in instances:
        if i['state'] == 'stopped':
            ec2.start_instances(InstanceIds=[i['id']])
            print(f"  ✅ Start command sent to {i['name']}")
            print(f"  ⏳ Will be running in ~30 seconds")
            write_log(f"USER COMMAND: start server - {i['id']} started")
            started += 1
    if started == 0:
        print("  ⚠️  No stopped instances found.")
        write_log("USER COMMAND: start server - no stopped instances")

def stop_server():
    print("\n🔴 Stopping EC2 instance...")
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    instances = get_instance()
    stopped = 0
    for i in instances:
        if i['state'] == 'running':
            ec2.stop_instances(InstanceIds=[i['id']])
            print(f"  ✅ Stop command sent to {i['name']}")
            print(f"  ⏳ Will be stopped in ~30 seconds")
            write_log(f"USER COMMAND: stop server - {i['id']} stopped")
            stopped += 1
    if stopped == 0:
        print("  ⚠️  No running instances found.")
        write_log("USER COMMAND: stop server - no running instances")

def restart_server():
    print("\n🔄 Restarting EC2 instance...")
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    instances = get_instance()
    restarted = 0
    for i in instances:
        if i['state'] == 'running':
            ec2.reboot_instances(InstanceIds=[i['id']])
            print(f"  ✅ Restart command sent to {i['name']}")
            print(f"  ⏳ Will restart in ~30 seconds")
            write_log(f"USER COMMAND: restart server - {i['id']} restarted")
            restarted += 1
    if restarted == 0:
        print("  ⚠️  No running instances found.")
        write_log("USER COMMAND: restart server - no running instances")

def show_log():
    print("\n📝 ACTIVITY LOG:")
    print("─" * 40)
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            if lines:
                for line in lines[-15:]:
                    print(" ", line.strip())
            else:
                print("  Log is empty.")
    except FileNotFoundError:
        print("  No log file found yet.")
    print("─" * 40)

def process_command(command):
    command = command.lower().strip()
    if command == 'help':
        show_help()
    elif command == 'show status':
        show_status()
    elif command == 'show cpu':
        show_cpu()
    elif command == 'show health':
        show_health()
    elif command == 'start server':
        start_server()
    elif command == 'stop server':
        stop_server()
    elif command == 'restart server':
        restart_server()
    elif command == 'show log':
        show_log()
    elif command == 'exit':
        print("\n👋 Exiting AI Cloud Assistant. Goodbye!\n")
        write_log("SESSION ENDED by user")
        return False
    else:
        print(f"\n❓ Command not recognized: '{command}'")
        print("  Type 'help' to see available commands.")
        write_log(f"UNKNOWN COMMAND: {command}")
    return True

# ── MAIN PROGRAM ──
print_header()
write_log("SESSION STARTED - AI Cloud Assistant launched")
show_help()

while True:
    try:
        user_input = input("\n🤖 Enter command: ")
        if not process_command(user_input):
            break
    except KeyboardInterrupt:
        print("\n\n👋 Session ended.")
        write_log("SESSION ENDED by keyboard interrupt")
        break