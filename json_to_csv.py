import json
import csv
import sys

def flatten_item(item):
    flat_item = {}
    for key, value in item.items():
        if isinstance(value, dict):
            if key == 'damage':
                flat_item['damage_min'] = value.get('min')
                flat_item['damage_max'] = value.get('max')
            elif key == 'stats':
                for stat_key, stat_value in value.items():
                    flat_item[f'stat_{stat_key}'] = stat_value
        elif isinstance(value, list):
            flat_item[key] = '; '.join(value)
        else:
            flat_item[key] = value
    return flat_item

data = json.load(open("database.json"))

# Flatten all items
flattened_data = [flatten_item(item) for item in data]

# Get all possible headers
all_headers = set()
for item in flattened_data:
    all_headers.update(item.keys())

# Define a preferred order for the main columns
preferred_order = [
    'name',
    'database_link',
    'required_level',
    'slot',
    'type',
    'armor',
    'dps',
    'speed',
    'damage_min',
    'damage_max',
]

# Get the stats and other columns
stat_columns = sorted([h for h in all_headers if h.startswith('stat_')])
effect_columns = sorted([h for h in all_headers if 'effects' in h])

# Combine the lists to create the final header order
main_headers = [h for h in preferred_order if h in all_headers]
remaining_headers = sorted([h for h in all_headers if h not in main_headers and h not in stat_columns and h not in effect_columns])

final_headers = main_headers + stat_columns + effect_columns

with open('database.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=final_headers)
    writer.writeheader()
    writer.writerows(flattened_data)

print("Successfully converted input to database.csv")
