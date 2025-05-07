Mina Karagoz
GAME 450 Final Project Report

# Dungeons & Dragons AI Tavern System

## Section 1: Base System Functionality (30 pts)

My project is a simple Dungeons & Dragons AI tavern system. When the user types "meet", the system creates a random character with a name, race, class, and a magic item. Then, it gives a short magic item description using RAG.

The user can choose how the portrait is generated:

- "Auto" mode uses the character class to describe the image using text retrieved from the dnd_character_appearances.txt file through RAG.
- "Manual" mode lets the user type their own description.

The system then draws the portrait, and the character speaks to the user like an NPC in a fantasy game. The user can continue chatting, and the character stays in role.



## Section 2: Prompt Engineering and Model Parameters (10 pts)

I used the llama model with a temperature of 0.8 to make the answers more fun and creative. Max tokens is set to 100  to keep the responses short. I added system and user prompts to help the AI act like an NPC. 

This helps keep responses concise and in the right style.



## Section 3: Tools Usage (15 pts)

I used the following tools:

- diffusers to generate character images  
- ollama to run the AI model locally  
- langchain and chromadb to load and search class and item data  

These tools work together to create both the look and the behavior of the NPC.



## Section 4: Planning & Reasoning (15 pts)

The system plans a character step by step:

1. Randomly picks a name, race, class, and item.  
2. Looks up class and item info using RAG.  
3. Creates a prompt using this data.  
4. The AI responds in character and remembers the conversation as it continues.



## Section 5: RAG Implementation (10 pts)

I used **RAG** to give accurate class and magic item descriptions.

- Class info comes from one dnd_character_apperences.txt file  
- magic Item info comes from another magic_items.txt file  

The files are split into chunks, added to a vector store, and the system searches for the closest match during runtime.



## Section 6: Additional Tools / Innovation (10 pts)

The project also generates AI portraits using Stable Diffusion. The portrait prompt is created using the character's class and the retrieved description, or the user can enter their own manually.

This adds a visual element to the system and makes the NPC more believable.



## Section 7: Code Quality & Modular Design (10 pts)

I split the code into clear files:

- main.py– for starting the app  
- encounter.py– for NPC generation and chat  
- portraits.py – for image creation  
- rag_utils.py– for document loading and search  

I used .venv and a clean requirements.txt. The project is easy to run and understand.

The system works and includes AI responses, context retrieval, and image generation. It’s simple, creative, and modular.
