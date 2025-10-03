import json
import sys

# Read item names from command line arguments
if len(sys.argv) > 1:
    names_to_find = sys.argv[1:]
else:
    print("Usage: python3 sample.py <item_name_1> <item_name_2> ...", file=sys.stderr)
    sys.exit(1)

with open('database.json', 'r') as f:
    data = json.load(f)

# Create a name-to-item mapping
items_by_name = {item['name']: item for item in data if 'name' in item}

for name in names_to_find:
    if name in items_by_name:
        json.dump(items_by_name[name], sys.stdout)
        sys.stdout.write('\n')
