import json

with open("sample-data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print()
print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<8}")
print(f"{'-'*50} {'-'*20} {'-'*8} {'-'*8}")

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    print(f"{attrs['dn']:<50} {attrs['descr']:<20} {attrs['speed']:<8} {attrs['mtu']:<8}")