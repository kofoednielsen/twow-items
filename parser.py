import json
import re
import sys
import urllib.parse

def parse_tooltip(tooltip_left, tooltip_right):
    item = {}
    stats = {}
    equip_effects = []
    unparsed_effects = []
    use_effects = []
    block_amount = 0

    if isinstance(tooltip_left, dict):
        tooltip_left = list(tooltip_left.values())
    
    if isinstance(tooltip_right, dict):
        tooltip_right = list(tooltip_right.values())

    for line in tooltip_left:
        line = line.strip()
        match = None

        # Equip effects
        if line.startswith("Equip:"):
            equip_effects.append(line.replace("Equip: ", ""))
        elif line.startswith("Chance on hit:"):
            equip_effects.append(line)
        elif line.startswith("Use:"):
            use_effects.append(line.replace("Use: ", ""))
        elif line.startswith("Requires Level"):
            match = re.search(r'Requires Level (\d+)', line)
            if match:
                item["required_level"] = required_level = int(match.group(1))

        # Basic Stats
        elif "+" in line:
            basic_stats = ["Stamina", "Agility", "Strength", "Intellect", "Spirit", 
                           "Attack Power", "Fire Resistance", "Frost Resistance", 
                           "Shadow Resistance", "Nature Resistance", "Arcane Resistance", 
                           "All Resistances"]
            for stat in basic_stats:
                if stat in line:
                    match = re.search(r'\+(\d+)', line)
                    if match:
                        stats[stat.lower().replace(" ", "_")] = int(match.group(1))
                        break

        # Other info
        elif "Armor" in line:
            match = re.search(r'(\d+)\s+Armor', line)
            if match:
                item["armor"] = int(match.group(1))
        elif "Block" in line:
            match = re.search(r'(\d+)\s+Block', line)
            if match:
                block_amount = int(match.group(1))
        elif "Damage" in line and "per second" not in line:
            match = re.search(r'(\d+)\s+-\s+(\d+)', line)
            if match:
                item["damage"] = {"min": int(match.group(1)), "max": int(match.group(2))}
        elif "damage per second" in line:
            match = re.search(r'\(([\d\.]+)\s+damage per second\)', line)
            if match:
                item["dps"] = float(match.group(1))
        
        # Item Slot
        slot_keywords = ["Head", "Neck", "Shoulder", "Back", "Chest", "Wrist", "Hands", "Waist", "Legs", "Feet", "Finger", "Trinket", "Main Hand", "Off Hand", "Ranged", "Two-Hand", "One-Hand", "Held In Off-hand"]
        for keyword in slot_keywords:
            if keyword.lower() == line.lower():
                item["slot"] = keyword
                break

    if tooltip_right:
        for line in tooltip_right:
            line = line.strip()
            # Item Type
            type_keywords = ["Cloth", "Leather", "Mail", "Plate", "Shield", "Mace", "Sword", "Axe", "Dagger", "Staff", "Wand", "Fist Weapon", "Polearm"]
            for keyword in type_keywords:
                if keyword.lower() in line.lower():
                    item["type"] = keyword
                    break
            if "Speed" in line:
                match = re.search(r'Speed\s+(.*)', line)
                if match:
                    item["speed"] = float(match.group(1))

    for effect in equip_effects:
        parsed = False
        # Mana per 5 sec
        match = re.search(r'Restores (\d+) mana per 5 sec', effect)
        if match:
            stats["mana_per_5_sec"] = int(match.group(1))
            parsed = True
        
        # Spell crit chance
        match = re.search(r'Improves your chance to get a critical strike with spells by (\d+)%', effect)
        if match:
            stats["spell_crit_chance"] = int(match.group(1))
            parsed = True

        # Spell hit chance
        match = re.search(r'Improves your chance to hit with all spells and attacks by (\d+)%', effect)
        if match:
            stats["spell_hit_chance"] = int(match.group(1))
            parsed = True

        # Spell damage and healing
        match = re.search(r'Increases damage and healing done by magical spells and effects by up to (\d+)', effect)
        if match:
            stats["spell_damage"] = int(match.group(1))
            stats["healing_power"] = int(match.group(1))
            parsed = True
        
        # Crit chance
        match = re.search(r'Improves your chance to get a critical strike by (\d+)%', effect)
        if match:
            stats["crit_chance"] = int(match.group(1))
            parsed = True
            
        # Spell damage by
        match = re.search(r'Increases your spell damage by up to (\d+)', effect)
        if match:
            stats["spell_damage"] = int(match.group(1))
            parsed = True

        # Healing spells by
        match = re.search(r'Increases your healing spells by up to (\d+)', effect)
        if match:
            stats["healing_power"] = int(match.group(1))
            parsed = True

        # Health per 5 sec
        match = re.search(r'Restores (\d+) health per 5 sec', effect)
        if match:
            stats["health_per_5_sec"] = int(match.group(1))
            parsed = True

        # Attack power
        match = re.search(r'\+(\d+) Attack Power', effect)
        if match:
            stats["attack_power"] = stats.get("attack_power", 0) + int(match.group(1))
            parsed = True

        match = re.search(r'Increases your attack power by (\d+)', effect)
        if match:
            stats["attack_power"] = stats.get("attack_power", 0) + int(match.group(1))
            parsed = True

        # Crit rating
        match = re.search(r'Increases your critical strike rating by (\d+)', effect)
        if match:
            stats["crit_rating"] = int(match.group(1))
            parsed = True

        # Hit rating
        match = re.search(r'Increases your hit rating by (\d+)', effect)
        if match:
            stats["hit_rating"] = int(match.group(1))
            parsed = True

        # Haste rating
        match = re.search(r'Increases your haste rating by (\d+)', effect)
        if match:
            stats["haste_rating"] = int(match.group(1))
            parsed = True

        # Armor penetration rating
        match = re.search(r'Increases your armor penetration rating by (\d+)', effect)
        if match:
            stats["armor_penetration_rating"] = int(match.group(1))
            parsed = True

        # Spell power
        match = re.search(r'Increases your spell power by (\d+)', effect)
        if match:
            stats["spell_power"] = int(match.group(1))
            parsed = True

        # Expertise rating
        match = re.search(r'Increases your expertise rating by (\d+)', effect)
        if match:
            stats["expertise_rating"] = int(match.group(1))
            parsed = True

        # Resilience rating
        match = re.search(r'Increases your resilience rating by (\d+)', effect)
        if match:
            stats["resilience_rating"] = int(match.group(1))
            parsed = True

        # Dodge rating
        match = re.search(r'Increases your dodge rating by (\d+)', effect)
        if match:
            stats["dodge_rating"] = int(match.group(1))
            parsed = True

        # Parry rating
        match = re.search(r'Increases your parry rating by (\d+)', effect)
        if match:
            stats["parry_rating"] = int(match.group(1))
            parsed = True

        # Block rating
        match = re.search(r'Increases your block rating by (\d+)', effect)
        if match:
            stats["block_rating"] = int(match.group(1))
            parsed = True

        # Block value
        match = re.search(r'Increases your block value by (\d+)', effect)
        if match:
            stats["block_value"] = int(match.group(1))
            parsed = True

        # Defense rating
        match = re.search(r'Increases your defense rating by (\d+)', effect)
        if match:
            stats["defense_rating"] = int(match.group(1))
            parsed = True

        # School spell damage
        match = re.search(r'Increases damage done by (\w+) spells and effects by up to (\d+)', effect)
        if match:
            school = match.group(1).lower()
            stats[f"{school}_spell_damage"] = int(match.group(2))
            parsed = True

        # Dodge chance
        match = re.search(r'Increases your chance to dodge an attack by (\d+)%', effect)
        if match:
            stats["dodge_chance"] = int(match.group(1))
            parsed = True

        # Block value (shield)
        match = re.search(r'Increases the block value of your shield by (\d+)', effect)
        if match:
            stats["block_value"] = int(match.group(1))
            parsed = True

        # Block chance (shield)
        match = re.search(r'Increases your chance to block attacks with a shield by (\d+)%', effect)
        if match:
            stats["block_chance"] = int(match.group(1))
            parsed = True

        # Spell hit chance
        match = re.search(r'Improves your chance to hit with spells by (\d+)%', effect)
        if match:
            stats["spell_hit_chance"] = int(match.group(1))
            parsed = True

        # Healing done by spells
        match = re.search(r'Increases healing done by spells and effects by up to (\d+)', effect)
        if match:
            stats["healing_power"] = int(match.group(1))
            parsed = True

        # Attack and Casting Speed
        match = re.search(r'Increases your attack and casting speed by (\d+)%', effect)
        if match:
            stats["attack_casting_speed"] = int(match.group(1))
            parsed = True

        # Hit chance
        match = re.search(r'Improves your chance to hit by (\d+)%', effect)
        if match:
            stats["hit_chance"] = int(match.group(1))
            parsed = True

        # Weapon skill
        match = re.search(r'Increased ([\w\s]+) \+(\d+)', effect)
        if match:
            skill = match.group(1).lower().replace(" ", "_")
            stats[f"{skill}_skill"] = int(match.group(2))
            parsed = True

        # Two-handed Weapon skill
        match = re.search(r'Increased Two-handed (\w+) \+(\d+)', effect)
        if match:
            skill = "two-handed_" + match.group(1).lower()
            stats[f"{skill}_skill"] = int(match.group(2))
            parsed = True

        if not parsed:
            unparsed_effects.append(effect)

    if block_amount > 0:
        stats["block_value"] = stats.get("block_value", 0) + block_amount

    if stats:
        item["stats"] = stats
    if use_effects:
        item["use_effects"] = use_effects
    if unparsed_effects:
        item["equip_effects"] = unparsed_effects
    return item

data = json.load(sys.stdin)

output = []
processed_names = set()
for item_id, item_data in data.items():
    tooltip_left_data = item_data.get('tooltiptextleft') or item_data.get('TooltipTextLeft')
    tooltip_right_data = item_data.get('tooltiptextright') or item_data.get('TooltipTextRight')

    if tooltip_left_data:
        name = item_data.get("name") or item_data.get("Name")
        if name and (name.startswith("Plans:") or name.startswith("Recipe:") or name.startswith("Pattern:") or name.startswith("Schematic:")):
            continue

        if name in processed_names:
            continue
            
        parsed_item = parse_tooltip(tooltip_left_data, tooltip_right_data)
        
        if "slot" in parsed_item or "type" in parsed_item:
            parsed_item["name"] = name
            encoded_name = urllib.parse.quote_plus(name)
            parsed_item["database_link"] = f"https://database.turtle-wow.org/?search={encoded_name}"
            output.append(parsed_item)
            processed_names.add(name)

print(json.dumps(output, indent=4))
