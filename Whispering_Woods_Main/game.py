#!/usr/bin/env python3
"""
LOST IN THE WHISPERING WOODS
A Text-Based Adventure Game - REVAMPED EDITION
Version 2.0

A modular, well-organized text adventure game with:
- 25 unique NPCs
- 10 recruitable companions
- 30+ creatures
- 35+ locations
- 35+ quests
- Crafting system
- Achievement system
- Rich lore

All game data is loaded from external JSON files for easy modification.
"""

import sys
import json
import random
import time
from pathlib import Path
from typing import Dict, List, Optional

# Import game modules
from src.colors import Colors, colored_text
from src.data_loader import DataLoader
from src.player import Player
from src.utils import (
    slow_type, instant_print, clear_screen, get_input, get_number_input,
    press_enter_to_continue, format_health_bar, format_list_numbered,
    confirm_choice, display_title, display_separator, wrap_text
)

# Constants
GAME_VERSION = "2.0.0"
SAVE_FILE = "whispering_woods_save.json"


class Game:
    """Main game class that manages the game loop and systems."""
    
    def __init__(self):
        """Initialize the game."""
        self.data_loader = DataLoader()
        self.player: Optional[Player] = None
        self.game_data: Dict = {}
        self.running = True
        self.god_mode = False
        
    def load_game_data(self):
        """Load all game data from JSON files."""
        instant_print(colored_text("Loading game data...", Colors.YELLOW))
        
        try:
            self.game_data = self.data_loader.load_all()
            instant_print(colored_text("Game data loaded successfully!", Colors.GREEN))
            
            # Display what was loaded
            instant_print(f"  NPCs: {len(self.game_data['npcs'])}")
            instant_print(f"  Items: {len(self.game_data['items'])}")
            instant_print(f"  Creatures: {len(self.game_data['creatures'])}")
            instant_print(f"  Locations: {len(self.game_data['locations'])}")
            instant_print(f"  Companions: {len(self.game_data.get('companions', {}))} ")
            instant_print(f"  Quests: {len(self.game_data['quests'])}")
            instant_print(f"  Crafting Recipes: {len(self.game_data['crafting'])}")
            instant_print(f"  Achievements: {len(self.game_data['achievements'])}")
            instant_print(f"  Lore Entries: {len(self.game_data['lore'])}")
            
        except Exception as e:
            instant_print(colored_text(f"Error loading game data: {e}", Colors.RED))
            sys.exit(1)
    
    def start_game(self):
        """Start the game."""
        clear_screen()
        display_title()
        display_separator()
        
        self.load_game_data()
        
        press_enter_to_continue()
        
        # Main menu
        while True:
            clear_screen()
            display_title()
            display_separator()
            
            instant_print(colored_text("\nMAIN MENU", Colors.BOLD_YELLOW))
            instant_print(colored_text("\n1. New Game", Colors.GREEN))
            instant_print(colored_text("2. Load Game", Colors.CYAN))
            instant_print(colored_text("3. Instructions", Colors.YELLOW))
            instant_print(colored_text("4. Credits", Colors.MAGENTA))
            instant_print(colored_text("5. Exit", Colors.RED))
            
            choice = get_number_input("\nSelect an option (1-5): ", 1, 5)
            
            if choice == 1:
                self.new_game()
                break
            elif choice == 2:
                if self.load_game():
                    break
            elif choice == 3:
                self.show_instructions()
            elif choice == 4:
                self.show_credits()
            elif choice == 5:
                instant_print(colored_text("\nThanks for playing!", Colors.CYAN))
                sys.exit(0)
    
    def new_game(self):
        """Start a new game."""
        clear_screen()
        display_title()
        display_separator()
        
        instant_print(colored_text("\n=== NEW GAME ===", Colors.BOLD_YELLOW))
        instant_print(wrap_text("""
You wake up in a mysterious forest with no memory of how you got here.
The trees whisper secrets in a language you don't understand.
Your goal: Find your way out before the forest claims you forever.
        """))
        
        # Get player name
        name = get_input("\nWhat is your name, traveler? ").strip()
        if not name:
            name = "Wanderer"
        
        self.player = Player(name)
        
        instant_print(colored_text(f"\nWelcome to the Whispering Woods, {name}.", Colors.BOLD_GREEN))
        press_enter_to_continue()
        
        self.game_loop()
    
    def game_loop(self):
        """Main game loop."""
        while self.running and self.player:
            try:
                # Check if player is dead
                if self.player.stats.health <= 0:
                    self.handle_death()
                    continue
                
                # Display current location
                self.display_location()
                
                # Show available actions
                self.show_actions()
                
                # Get player input
                action = get_input("\nWhat do you want to do? ").lower().strip()
                
                # Process action
                self.process_action(action)
                
            except KeyboardInterrupt:
                instant_print(colored_text("\n\nGame interrupted!", Colors.YELLOW))
                if confirm_choice("Do you want to save before exiting?"):
                    self.save_game()
                break
            except Exception as e:
                instant_print(colored_text(f"\nError: {e}", Colors.RED))
                instant_print(colored_text("Please try a different action.", Colors.YELLOW))
    
    def display_location(self):
        """Display current location information."""
        clear_screen()
        
        location_id = self.player.current_location
        location = self.game_data['locations'].get(location_id, {})
        
        if not location:
            instant_print(colored_text("Error: Unknown location!", Colors.RED))
            return
        
        # Location name
        instant_print(colored_text(f"\n╔══ {location['name']} ══╗", Colors.BOLD_CYAN))
        
        # Location description
        description = location.get('long_description', location.get('description', ''))
        instant_print(wrap_text(description))
        
        # Player stats
        display_separator("-", 60, Colors.DIM)
        self.display_player_stats()
        
        # Features of the location
        features = location.get('features', [])
        if features:
            instant_print(colored_text("\nYou notice:", Colors.YELLOW))
            for feature in features[:3]:  # Show first 3 features
                instant_print(f"  • {feature}")
        
        # NPCs present
        npcs = location.get('npcs', [])
        if npcs:
            instant_print(colored_text("\nPeople here:", Colors.GREEN))
            for npc_id in npcs:
                npc = self.game_data['npcs'].get(npc_id, {})
                if npc:
                    instant_print(f"  • {npc.get('name', 'Unknown')}")
        
        # Companions
        if self.player.active_companion:
            comp_id = self.player.active_companion
            companion = self.game_data.get('companions', {}).get(comp_id, {})
            if companion:
                instant_print(colored_text(f"\n{companion.get('name')} is with you.", Colors.MAGENTA))
        
        display_separator()
    
    def display_player_stats(self):
        """Display player statistics."""
        p = self.player
        
        instant_print(colored_text(f"{p.name} - Level {p.progress.level}", Colors.BOLD_WHITE))
        instant_print(f"Health: {format_health_bar(p.stats.health, p.stats.max_health)}")
        instant_print(f"Gold: {colored_text(str(p.progress.gold), Colors.YELLOW)} | " +
                     f"XP: {p.progress.experience}/{p.get_exp_to_next_level()}")
    
    def show_actions(self):
        """Show available actions to the player."""
        instant_print(colored_text("\nAvailable Actions:", Colors.BOLD_WHITE))
        instant_print("  explore | inventory | stats | quests | map")
        instant_print("  talk | companions | rest | save | help | quit")
    
    def process_action(self, action: str):
        """Process player action."""
        action = action.lower().strip()
        
        if not action:
            return
        
        # Navigation and exploration
        if action in ['explore', 'move', 'go', 'travel']:
            self.explore_location()
        elif action in ['look', 'examine', 'search']:
            self.search_location()
        
        # Character management
        elif action in ['inventory', 'inv', 'i']:
            self.show_inventory()
        elif action in ['stats', 'status', 'st']:
            self.show_detailed_stats()
        elif action in ['equipment', 'equip', 'eq']:
            self.manage_equipment()
        
        # Social interactions
        elif action in ['talk', 'speak', 'chat']:
            self.talk_to_npc()
        elif action in ['companions', 'comp', 'party']:
            self.manage_companions()
        
        # Quests and progress
        elif action in ['quests', 'quest', 'q']:
            self.show_quests()
        elif action in ['map', 'm']:
            self.show_map()
        elif action in ['lore', 'journal']:
            self.show_lore()
        
        # Game actions
        elif action in ['rest', 'sleep', 'camp']:
            self.rest()
        elif action in ['craft', 'crafting']:
            self.craft_items()
        elif action in ['save']:
            self.save_game()
        elif action in ['help', 'h', '?']:
            self.show_help()
        elif action in ['quit', 'exit', 'q']:
            if confirm_choice("Are you sure you want to quit?"):
                if confirm_choice("Save game before quitting?"):
                    self.save_game()
                self.running = False
        
        else:
            instant_print(colored_text("Unknown action. Type 'help' for available commands.", Colors.YELLOW))
            press_enter_to_continue()
    
    def explore_location(self):
        """Explore and move to connected locations."""
        clear_screen()
        instant_print(colored_text("\n=== EXPLORE ===", Colors.BOLD_CYAN))
        
        location = self.game_data['locations'].get(self.player.current_location, {})
        connections = location.get('connections', [])
        
        if not connections:
            instant_print(colored_text("There's nowhere to go from here!", Colors.RED))
            press_enter_to_continue()
            return
        
        instant_print(colored_text("\nWhere would you like to go?", Colors.YELLOW))
        
        available_locations = []
        for i, loc_id in enumerate(connections, 1):
            loc = self.game_data['locations'].get(loc_id, {})
            if loc:
                status = ""
                if loc_id in self.player.discovered_locations:
                    status = colored_text(" [Visited]", Colors.DIM)
                instant_print(f"{i}. {loc.get('name', 'Unknown')}{status}")
                available_locations.append(loc_id)
        
        instant_print(f"{len(available_locations) + 1}. Stay here")
        
        choice = get_number_input(f"\nSelect destination (1-{len(available_locations) + 1}): ",
                                   1, len(available_locations) + 1)
        
        if choice and choice <= len(available_locations):
            new_location = available_locations[choice - 1]
            self.move_to_location(new_location)
    
    def move_to_location(self, location_id: str):
        """Move player to a new location."""
        self.player.previous_location = self.player.current_location
        self.player.current_location = location_id
        self.player.discover_location(location_id)
        self.player.progress.steps_taken += 1
        
        instant_print(colored_text(f"\nYou travel to {self.game_data['locations'][location_id]['name']}...", 
                                   Colors.CYAN))
        time.sleep(1)
        
        # Random encounter chance
        location = self.game_data['locations'].get(location_id, {})
        encounter_chance = location.get('encounter_chance', 0)
        
        if encounter_chance > 0 and random.random() < encounter_chance:
            self.random_encounter()
    
    def random_encounter(self):
        """Trigger a random encounter."""
        instant_print(colored_text("\n⚠ You encounter something!", Colors.RED))
        time.sleep(1)
        
        # Simple placeholder - would implement full combat system
        instant_print(colored_text("A wild creature appears! (Combat system not fully implemented yet)", 
                                   Colors.YELLOW))
        press_enter_to_continue()
    
    def search_location(self):
        """Search the current location for items."""
        instant_print(colored_text("\nYou search the area carefully...", Colors.YELLOW))
        time.sleep(1)
        
        location = self.game_data['locations'].get(self.player.current_location, {})
        items = location.get('items', [])
        
        if items:
            found_item = random.choice(items)
            instant_print(colored_text(f"You found: {found_item}!", Colors.GREEN))
            self.player.add_item(found_item)
        else:
            instant_print(colored_text("You don't find anything of interest.", Colors.DIM))
        
        press_enter_to_continue()
    
    def show_inventory(self):
        """Display player inventory."""
        clear_screen()
        instant_print(colored_text("\n=== INVENTORY ===", Colors.BOLD_YELLOW))
        
        if not self.player.inventory:
            instant_print(colored_text("Your inventory is empty.", Colors.DIM))
        else:
            for i, item_id in enumerate(self.player.inventory, 1):
                item = self.game_data['items'].get(item_id, {})
                name = item.get('name', item_id)
                item_type = item.get('type', 'item')
                instant_print(f"{i}. {name} [{item_type}]")
        
        instant_print(colored_text(f"\nGold: {self.player.progress.gold}", Colors.YELLOW))
        instant_print(colored_text(f"Weight: {len(self.player.inventory)}/50", Colors.CYAN))
        
        press_enter_to_continue()
    
    def show_detailed_stats(self):
        """Show detailed player statistics."""
        clear_screen()
        instant_print(colored_text("\n=== CHARACTER STATS ===", Colors.BOLD_CYAN))
        
        p = self.player
        display_separator()
        
        instant_print(colored_text(f"Name: {p.name}", Colors.WHITE))
        instant_print(colored_text(f"Level: {p.progress.level}", Colors.YELLOW))
        instant_print(colored_text(f"Experience: {p.progress.experience}/{p.get_exp_to_next_level()}", Colors.CYAN))
        
        display_separator("-")
        instant_print("Health:  " + format_health_bar(p.stats.health, p.stats.max_health))
        instant_print(f"Stamina: {p.stats.stamina}/{p.stats.max_stamina}")
        instant_print(f"Mana:    {p.stats.mana}/{p.stats.max_mana}")
        
        display_separator("-")
        instant_print(colored_text("Skills:", Colors.YELLOW))
        for skill, level in p.skills.items():
            instant_print(f"  {skill.capitalize()}: {level}")
        
        display_separator("-")
        instant_print(f"Gold: {colored_text(str(p.progress.gold), Colors.YELLOW)}")
        instant_print(f"Kills: {p.progress.kills}")
        instant_print(f"Deaths: {p.progress.deaths}")
        instant_print(f"Locations Discovered: {len(p.discovered_locations)}")
        instant_print(f"Quests Completed: {len(p.completed_quests)}")
        instant_print(f"Achievements: {len(p.achievements)}")
        
        press_enter_to_continue()
    
    def manage_equipment(self):
        """Manage equipped items."""
        instant_print(colored_text("\n=== EQUIPMENT ===", Colors.BOLD_MAGENTA))
        instant_print("(Equipment system placeholder)")
        press_enter_to_continue()
    
    def talk_to_npc(self):
        """Talk to NPCs in the current location."""
        location = self.game_data['locations'].get(self.player.current_location, {})
        npcs = location.get('npcs', [])
        
        if not npcs:
            instant_print(colored_text("\nThere's no one here to talk to.", Colors.YELLOW))
            press_enter_to_continue()
            return
        
        clear_screen()
        instant_print(colored_text("\n=== TALK ===", Colors.BOLD_GREEN))
        instant_print("Who would you like to talk to?")
        
        for i, npc_id in enumerate(npcs, 1):
            npc = self.game_data['npcs'].get(npc_id, {})
            instant_print(f"{i}. {npc.get('name', 'Unknown')}")
        
        choice = get_number_input(f"\nSelect NPC (1-{len(npcs)}): ", 1, len(npcs))
        
        if choice:
            npc_id = npcs[choice - 1]
            self.have_conversation(npc_id)
    
    def have_conversation(self, npc_id: str):
        """Have a conversation with an NPC."""
        npc = self.game_data['npcs'].get(npc_id, {})
        
        if not npc:
            return
        
        clear_screen()
        instant_print(colored_text(f"\n=== {npc.get('name', 'NPC')} ===", Colors.BOLD_GREEN))
        instant_print(colored_text(npc.get('description', ''), Colors.CYAN))
        
        dialogue = npc.get('dialogue', [])
        if dialogue:
            line = random.choice(dialogue)
            instant_print(colored_text(f'\n"{line}"', Colors.WHITE))
        
        press_enter_to_continue()
    
    def manage_companions(self):
        """Manage companions."""
        clear_screen()
        instant_print(colored_text("\n=== COMPANIONS ===", Colors.BOLD_MAGENTA))
        
        if not self.player.companions:
            instant_print(colored_text("You haven't recruited any companions yet.", Colors.YELLOW))
        else:
            instant_print(colored_text("Your Companions:", Colors.GREEN))
            for comp_id in self.player.companions:
                companion = self.game_data.get('companions', {}).get(comp_id, {})
                name = companion.get('name', comp_id)
                status = " [Active]" if comp_id == self.player.active_companion else ""
                instant_print(f"  • {name}{status}")
        
        press_enter_to_continue()
    
    def show_quests(self):
        """Show active and completed quests."""
        clear_screen()
        instant_print(colored_text("\n=== QUESTS ===", Colors.BOLD_YELLOW))
        
        if self.player.active_quests:
            instant_print(colored_text("\nActive Quests:", Colors.GREEN))
            for quest_id in self.player.active_quests:
                quest = self.game_data['quests'].get(quest_id, {})
                instant_print(f"  • {quest.get('name', quest_id)}")
        else:
            instant_print(colored_text("\nNo active quests.", Colors.DIM))
        
        if self.player.completed_quests:
            instant_print(colored_text(f"\nCompleted Quests: {len(self.player.completed_quests)}", Colors.CYAN))
        
        press_enter_to_continue()
    
    def show_map(self):
        """Show discovered locations."""
        clear_screen()
        instant_print(colored_text("\n=== MAP ===", Colors.BOLD_CYAN))
        
        instant_print(f"\nDiscovered Locations ({len(self.player.discovered_locations)}):")
        for loc_id in self.player.discovered_locations:
            loc = self.game_data['locations'].get(loc_id, {})
            current = " [Current]" if loc_id == self.player.current_location else ""
            instant_print(f"  • {loc.get('name', loc_id)}{current}")
        
        press_enter_to_continue()
    
    def show_lore(self):
        """Show discovered lore entries."""
        clear_screen()
        instant_print(colored_text("\n=== LORE ===", Colors.BOLD_MAGENTA))
        
        if not self.player.lore_discovered:
            instant_print(colored_text("You haven't discovered any lore yet.", Colors.DIM))
        else:
            for lore_id in self.player.lore_discovered:
                lore = self.game_data['lore'].get(lore_id, {})
                instant_print(colored_text(f"\n{lore.get('title', lore_id)}", Colors.YELLOW))
                instant_print(wrap_text(lore.get('content', '')))
        
        press_enter_to_continue()
    
    def rest(self):
        """Rest to restore health and stamina."""
        location = self.game_data['locations'].get(self.player.current_location, {})
        
        if not location.get('rest_allowed', False):
            instant_print(colored_text("\nThis doesn't seem like a safe place to rest.", Colors.RED))
            press_enter_to_continue()
            return
        
        instant_print(colored_text("\nYou rest for a while...", Colors.CYAN))
        time.sleep(2)
        
        healed = self.player.heal(30)
        stamina_restored = self.player.restore_stamina(50)
        
        instant_print(colored_text(f"You restored {healed} health and {stamina_restored} stamina.", Colors.GREEN))
        press_enter_to_continue()
    
    def craft_items(self):
        """Crafting interface."""
        instant_print(colored_text("\n=== CRAFTING ===", Colors.BOLD_YELLOW))
        instant_print("(Crafting system placeholder)")
        press_enter_to_continue()
    
    def save_game(self):
        """Save the game."""
        try:
            save_data = {
                'version': GAME_VERSION,
                'player': self.player.get_save_data()
            }
            
            with open(SAVE_FILE, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            instant_print(colored_text("\nGame saved successfully!", Colors.GREEN))
        except Exception as e:
            instant_print(colored_text(f"\nError saving game: {e}", Colors.RED))
        
        time.sleep(1)
    
    def load_game(self) -> bool:
        """Load a saved game."""
        try:
            with open(SAVE_FILE, 'r') as f:
                save_data = json.load(f)
            
            self.player = Player.from_save_data(save_data['player'])
            instant_print(colored_text("\nGame loaded successfully!", Colors.GREEN))
            time.sleep(1)
            return True
        except FileNotFoundError:
            instant_print(colored_text("\nNo save file found.", Colors.YELLOW))
            press_enter_to_continue()
            return False
        except Exception as e:
            instant_print(colored_text(f"\nError loading game: {e}", Colors.RED))
            press_enter_to_continue()
            return False
    
    def show_help(self):
        """Show help information."""
        clear_screen()
        instant_print(colored_text("\n=== HELP ===", Colors.BOLD_CYAN))
        display_separator()
        
        instant_print(colored_text("\nAvailable Commands:", Colors.YELLOW))
        instant_print("  explore    - Move to a different location")
        instant_print("  look       - Search the current area")
        instant_print("  inventory  - View your items")
        instant_print("  stats      - View detailed character stats")
        instant_print("  equipment  - Manage equipped items")
        instant_print("  talk       - Talk to NPCs")
        instant_print("  companions - Manage your companions")
        instant_print("  quests     - View your quests")
        instant_print("  map        - View discovered locations")
        instant_print("  lore       - Read discovered lore")
        instant_print("  rest       - Rest to restore health")
        instant_print("  craft      - Craft items")
        instant_print("  save       - Save your game")
        instant_print("  help       - Show this help message")
        instant_print("  quit       - Exit the game")
        
        press_enter_to_continue()
    
    def show_instructions(self):
        """Show game instructions."""
        clear_screen()
        instant_print(colored_text("\n=== INSTRUCTIONS ===", Colors.BOLD_YELLOW))
        display_separator()
        
        instant_print(wrap_text("""
Welcome to the Whispering Woods! You are a traveler who has become lost in 
a mysterious and dangerous forest. Your goal is to find your way out while 
surviving the perils that await.

GAMEPLAY:
- Explore locations by typing commands
- Talk to NPCs to learn more and get quests
- Recruit companions to aid you in battle
- Craft items and manage your inventory
- Complete quests to progress the story
- Discover lore to understand the forest's secrets

TIPS:
- Rest in safe areas to restore health
- Save your game frequently
- Pay attention to location descriptions
- Build relationships with NPCs
- Choose your companions wisely
        """))
        
        press_enter_to_continue()
    
    def show_credits(self):
        """Show game credits."""
        clear_screen()
        instant_print(colored_text("\n=== CREDITS ===", Colors.BOLD_MAGENTA))
        display_separator()
        
        instant_print(colored_text("""
LOST IN THE WHISPERING WOODS
Version 2.0 - Revamped Edition

Game Design & Development: Sanic9exe
Refactored by: AI Assistant (Claude)

Special Thanks:
- To all players who provided feedback
- To the Python community

This is a complete revamp of the original game,
featuring improved organization, modular code structure,
and quality-focused content design.

Thank you for playing!
        """, Colors.CYAN))
        
        press_enter_to_continue()
    
    def handle_death(self):
        """Handle player death."""
        clear_screen()
        instant_print(colored_text("""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║                  YOU HAVE DIED                        ║
║                                                       ║
║         The forest has claimed another soul...        ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
        """, Colors.RED))
        
        self.player.progress.deaths += 1
        
        instant_print(colored_text("\nWhat would you like to do?", Colors.YELLOW))
        instant_print("1. Respawn at last safe location")
        instant_print("2. Load saved game")
        instant_print("3. Return to main menu")
        
        choice = get_number_input("\nSelect option (1-3): ", 1, 3)
        
        if choice == 1:
            self.player.stats.health = self.player.stats.max_health // 2
            self.player.current_location = "clearing"
            instant_print(colored_text("\nYou awaken at the forest clearing...", Colors.CYAN))
            time.sleep(2)
        elif choice == 2:
            self.load_game()
        else:
            self.running = False


def main():
    """Main entry point."""
    try:
        game = Game()
        game.start_game()
        
        if game.player:
            game.game_loop()
        
        instant_print(colored_text("\nThanks for playing!", Colors.BOLD_CYAN))
        
    except Exception as e:
        instant_print(colored_text(f"\nCritical error: {e}", Colors.RED))
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
