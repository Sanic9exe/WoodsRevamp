"""
External data loader for game content
Loads NPCs, items, creatures, locations, quests, etc. from JSON files
"""

import json
import os
from typing import Dict, Any
from pathlib import Path


class DataLoader:
    """Loads game data from external JSON files."""
    
    def __init__(self, data_dir: str = None):
        """Initialize the data loader with the data directory path."""
        if data_dir is None:
            # Default to data/ folder relative to this file
            base_path = Path(__file__).parent.parent
            self.data_dir = base_path / "data"
        else:
            self.data_dir = Path(data_dir)
        
        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load data from a JSON file."""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Returning empty dict.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding {filename}: {e}")
            return {}
    
    def save_json(self, filename: str, data: Dict[str, Any]) -> bool:
        """Save data to a JSON file."""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False
    
    def load_npcs(self) -> Dict[str, Any]:
        """Load NPC data from npcs.json."""
        return self.load_json("npcs.json")
    
    def load_items(self) -> Dict[str, Any]:
        """Load item data from items.json."""
        return self.load_json("items.json")
    
    def load_creatures(self) -> Dict[str, Any]:
        """Load creature data from creatures.json."""
        return self.load_json("creatures.json")
    
    def load_locations(self) -> Dict[str, Any]:
        """Load location data from locations.json."""
        return self.load_json("locations.json")
    
    def load_quests(self) -> Dict[str, Any]:
        """Load quest data from quests.json."""
        return self.load_json("quests.json")
    
    def load_crafting_recipes(self) -> Dict[str, Any]:
        """Load crafting recipe data from crafting.json."""
        return self.load_json("crafting.json")
    
    def load_achievements(self) -> Dict[str, Any]:
        """Load achievement data from achievements.json."""
        return self.load_json("achievements.json")
    
    def load_events(self) -> Dict[str, Any]:
        """Load random event data from events.json."""
        return self.load_json("events.json")
    
    def load_lore(self) -> Dict[str, Any]:
        """Load lore entries from lore.json."""
        return self.load_json("lore.json")
    
    def load_companions(self) -> Dict[str, Any]:
        """Load companion data from companions.json."""
        return self.load_json("companions.json")
    
    def load_spells(self) -> Dict[str, Any]:
        """Load spell data from spells.json."""
        return self.load_json("spells.json")
    
    def load_status_effects(self) -> Dict[str, Any]:
        """Load status effects from status_effects.json."""
        return self.load_json("status_effects.json")
    
    def load_all(self) -> Dict[str, Dict[str, Any]]:
        """Load all game data at once."""
        return {
            'npcs': self.load_npcs(),
            'items': self.load_items(),
            'creatures': self.load_creatures(),
            'locations': self.load_locations(),
            'companions': self.load_companions(),
            'quests': self.load_quests(),
            'crafting': self.load_crafting_recipes(),
            'achievements': self.load_achievements(),
            'events': self.load_events(),
            'lore': self.load_lore(),
            'spells': self.load_spells(),
            'status_effects': self.load_status_effects()
        }
