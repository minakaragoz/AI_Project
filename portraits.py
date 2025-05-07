

import os
from datetime import datetime
from diffusers import DiffusionPipeline
import torch

from utils.rag_utils import load_documents, chunk_documents, setup_chroma_db, retrieve_context


from langchain_community.document_loaders import TextLoader
loader = TextLoader("data/dnd_character_appearances.txt")
_docs = loader.load()

_chunks = chunk_documents(_docs)
_collection = setup_chroma_db(_chunks)


pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2", torch_dtype=torch.float32)
pipe = pipe.to("cpu") 

def get_portrait_prompt(npc=None):
    mode = input("Portrait mode - type 'manual' to describe or 'auto' for class-based: ").strip().lower()

    if mode == "manual":
        return input("Describe your character for the portrait: ")

    elif mode == "auto" and npc:
        character_class = npc["class"]
        query = f"Describe a {character_class}"
        contexts = retrieve_context(_collection, query, k=1)

        if contexts:
            return f"portrait of a {npc['race']} {character_class}, {contexts[0]}"
        else:
            print("[!] No class description found, using fallback.")
            return f"portrait of a {npc['race']} {character_class} in fantasy style"

    else:
        return "portrait of a mysterious D&D character"

def generate_portrait(prompt: str, output_path: str = None):
    print(f" Generating portrait for prompt: {prompt}")
    
    image = pipe(prompt).images[0]

    if not output_path:
        os.makedirs("portraits", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"portraits/portrait_{timestamp}.png"

    image.save(output_path)
    print(f" Portrait saved to {output_path}")

