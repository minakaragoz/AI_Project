from ollama import chat
import random
from portraits import generate_portrait, get_portrait_prompt
from utils.rag_utils import get_magic_item_info 

NAMES = ["Thalor", "Mira", "Drogan", "Liora", "Karn", "Selene"]
RACES = ["elf", "dwarf", "human", "orc", "tiefling"]
CLASSES = ["rogue", "cleric", "bard", "wizard", "fighter"]
ITEMS = ["Cloak of Invisibility", "Wand of Fireballs", "Bag of Holding", "Gauntlets of Ogre Power"]

def generate_npc_intro():
    name = random.choice(NAMES)
    race = random.choice(RACES)
    char_class = random.choice(CLASSES)
    item = random.choice(ITEMS)

    
    item_info = get_magic_item_info(item)
    item_desc = item_info[0] if item_info else f"a magical item: {item}"

    
    prompt = (
        f"You are {name}, a {race} {char_class}. "
        f"You say something in character to a traveler who approaches you. "
        f"You carry: {item} — {item_desc}"
    )

    return {
        "name": name,
        "race": race,
        "class": char_class,
        "item": item,
        "prompt": prompt
    }

def run_tavern_encounter():
    npc = generate_npc_intro()
    print(f"\n You meet {npc['name']}, a {npc['race']} {npc['class']}.\n")

    
    print("Let’s generate a portrait of this character!")
    portrait_prompt = get_portrait_prompt(npc)
    filename = f"portraits/{npc['name'].lower()}_{npc['race']}_{npc['class']}.png"
    generate_portrait(portrait_prompt, output_path=filename)

    
    messages = [
        {
            "role": "system",
            "content": "You are an NPC in a fantasy tavern. Stay in character and speak like a D&D character would. Keep responses under 100 words."
        },
        {
            "role": "user",
            "content": npc["prompt"]
        }
    ]

    print("[DEBUG] Sending initial prompt to Ollama...")

    try:
        response = chat(model='llama3', messages=messages, options={"temperature": 0.8})

        content = response.get("message", {}).get("content", None)
        if content:
            print(" NPC says:", content)
            messages.append({"role": "assistant", "content": content})
        else:
            print("[ERROR] No content received from Ollama.")
            return
    except Exception as e:
        print("[ERROR] Exception while chatting:", e)
        return

    print("[DEBUG] Entering dialogue loop...")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "bye", "leave"]:
            print(f"\n You leave the table. {npc['name']} nods in farewell.")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = chat(model='llama3', messages=messages, options={"temperature": 0.8})

            content = response.get("message", {}).get("content", None)
            if content:
                print(" NPC says:", content)
                messages.append({"role": "assistant", "content": content})
            else:
                print("[ERROR] No reply from NPC.")
        except Exception as e:
            print("[ERROR] Failed during chat:", e)
            break
