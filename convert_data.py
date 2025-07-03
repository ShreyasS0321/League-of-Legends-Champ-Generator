import json

def ability_short_names(abilities):
    return ', '.join([f"{ab['name']}" for ab in abilities])

def format_champ_for_gen(champ):
    # Option 1: Structure-based prompt (for model to learn to fill in the blanks)
    prompt = (
        f"Create a League of Legends champion given the following details:\n"
        f"Stats: {champ['stats']}\n"
        f"Ability names: {ability_short_names(champ['abilities'])}\n"
        f"Class: [you can add champ's class here if you want]\n"
        "Generate the full champion details (title, abilities with descriptions, and a lore paragraph) in the style of Riot's official champion pages."
    )
    # Option 2: Natural language prompt
    nlp_prompt = (
        f"Invent a champion inspired by {champ['champion']}'s theme and role, "
        f"but make it unique. (Example: a darkin swordsman with lifesteal powers). "
        f"Describe their stats, abilities (with names and detailed descriptions), and full lore."
    )
    # Response: the real data
    ab_lines = []
    for ab in champ['abilities']:
        ab_lines.append(f"{ab['slot']} - {ab['name']}: {ab['description']}")
    stats_lines = [f"{k.replace('_',' ').capitalize()}: {v}" for k,v in champ["stats"].items() if v]
    stats_str = "\n".join(stats_lines)
    ab_str = "\n".join(ab_lines)
    response = (
        f"Champion: {champ['champion']}\n"
        f"Title: {champ.get('title', '')}\n"
        f"Stats:\n{stats_str}\n"
        f"Abilities:\n{ab_str}\n"
        f"Lore:\n{champ['lore']}"
    )
    return [
        {"prompt": prompt, "response": response},
        {"prompt": nlp_prompt, "response": response}
    ]

# Bulk conversion:
with open("lol_champions.jsonl") as fin, open("finetune_champion_gen.jsonl", "w") as fout:
    for line in fin:
        champ = json.loads(line)
        pairs = format_champ_for_gen(champ)
        for pair in pairs:
            fout.write(json.dumps(pair, ensure_ascii=False) + "\n")
