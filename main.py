
from encounter import run_tavern_encounter

def main():
    print("Welcome to the AI-Generated D&D Tavern Encounter!")
    while True:
        cmd = input("\nType 'meet' to encounter a new NPC, or 'exit' to leave: ").strip().lower()
        if cmd == "exit":
            print("Farewell, traveler!")
            break
        elif cmd == "meet":
            run_tavern_encounter()
        else:
            print("Unknown command. Try 'meet' or 'exit'.")

if __name__ == "__main__":
    main()
