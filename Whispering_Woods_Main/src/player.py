"""
Player character module
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class PlayerStats:
    """Player statistics"""
    health: int = 100
    max_health: int = 100
    stamina: int = 100
    max_stamina: int = 100
    mana: int = 50
    max_mana: int = 50
    hunger: int = 100
    thirst: int = 100
    sanity: int = 100


@dataclass
class PlayerProgress:
    """Player progression data"""
    experience: int = 0
    level: int = 1
    skill_points: int = 0
    gold: int = 25
    play_time: float = 0
    deaths: int = 0
    kills: int = 0
    steps_taken: int = 0
    items_collected: int = 0
    items_crafted: int = 0


class Player:
    """Represents the player character with all stats and inventory."""
    
    def __init__(self, name: str = "Traveler"):
        self.name = name
        self.stats = PlayerStats()
        self.progress = PlayerProgress()
        
        # Inventory and equipment
        self.inventory: List[str] = []  # Item IDs
        self.equipped: Dict[str, Optional[str]] = {
            'weapon': None,
            'armor': None,
            'helmet': None,
            'light': None,
            'accessory': None
        }
        
        # Skills
        self.skills: Dict[str, int] = {
            'combat': 1,
            'survival': 1,
            'crafting': 1,
            'stealth': 1,
            'magic': 1,
            'diplomacy': 1
        }
        
        # Location and exploration
        self.current_location = "clearing"
        self.previous_location = ""
        self.discovered_locations: List[str] = ["clearing"]
        self.visited_count: Dict[str, int] = {"clearing": 1}
        
        # Quests
        self.active_quests: List[str] = []
        self.completed_quests: List[str] = []
        self.quest_progress: Dict[str, Dict] = {}
        
        # Crafting and recipes
        self.known_recipes: List[str] = ["torch", "health_potion"]
        
        # Status effects (effect_name: remaining_turns)
        self.status_effects: Dict[str, int] = {}
        
        # Companions
        self.companions: List[str] = []
        self.active_companion: Optional[str] = None
        
        # Reputation with NPCs
        self.reputation: Dict[str, int] = {}
        
        # Achievements
        self.achievements: List[str] = []
        
        # Notes and lore
        self.notes: List[str] = []
        self.lore_discovered: List[str] = []
        
        # Combat stats
        self.kill_count: Dict[str, int] = {}
        self.total_damage_dealt: int = 0
        self.total_damage_taken: int = 0
        self.current_combo: int = 0
        
        # State flags
        self.is_in_combat: bool = False
        self.is_resting: bool = False
        self.is_hidden: bool = False
    
    def get_attack_damage(self, item_data: Dict = None) -> Tuple[int, str]:
        """Calculate player's attack damage."""
        import random
        
        base_damage = 5
        weapon_damage = 0
        damage_type = "physical"
        
        # Get weapon damage from equipped weapon
        if self.equipped.get('weapon') and item_data:
            weapon_id = self.equipped['weapon']
            weapon = item_data.get(weapon_id, {})
            weapon_damage = weapon.get('damage', 0)
            # Could add special damage types here
        
        skill_bonus = self.skills.get('combat', 1) // 2
        dice_roll = random.randint(1, 6)
        
        # Status effects
        modifier = 0
        if "strengthened" in self.status_effects:
            modifier += 5
        if "weakened" in self.status_effects:
            modifier -= 5
        
        total_damage = base_damage + weapon_damage + skill_bonus + dice_roll + modifier
        return max(1, total_damage), damage_type
    
    def get_defense(self, item_data: Dict = None) -> int:
        """Calculate player's total defense."""
        base_defense = 2
        armor_defense = 0
        
        # Get defense from equipped items
        if item_data:
            for slot in ['armor', 'helmet']:
                item_id = self.equipped.get(slot)
                if item_id:
                    item = item_data.get(item_id, {})
                    armor_defense += item.get('defense', 0)
        
        # Status effects
        modifier = 0
        if "protected" in self.status_effects:
            modifier += 5
        
        return base_defense + armor_defense + modifier
    
    def take_damage(self, amount: int, god_mode: bool = False) -> int:
        """Apply damage to player and return actual damage taken."""
        if god_mode:
            return 0
        
        defense = self.get_defense()
        actual_damage = max(1, amount - defense // 2)
        self.stats.health -= actual_damage
        self.total_damage_taken += actual_damage
        self.current_combo = 0
        
        if self.stats.health <= 0:
            self.stats.health = 0
        
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """Heal the player and return actual amount healed."""
        healed = min(amount, self.stats.max_health - self.stats.health)
        self.stats.health += healed
        self.total_damage_dealt += healed
        return healed
    
    def restore_stamina(self, amount: int) -> int:
        """Restore stamina."""
        restored = min(amount, self.stats.max_stamina - self.stats.stamina)
        self.stats.stamina += restored
        return restored
    
    def restore_mana(self, amount: int) -> int:
        """Restore mana."""
        restored = min(amount, self.stats.max_mana - self.stats.mana)
        self.stats.mana += restored
        return restored
    
    def use_stamina(self, amount: int) -> bool:
        """Use stamina for an action."""
        if self.stats.stamina >= amount:
            self.stats.stamina -= amount
            return True
        return False
    
    def use_mana(self, amount: int) -> bool:
        """Use mana for a spell."""
        if self.stats.mana >= amount:
            self.stats.mana -= amount
            return True
        return False
    
    def gain_experience(self, amount: int) -> bool:
        """Add experience and check for level up."""
        self.progress.experience += amount
        exp_needed = self.get_exp_to_next_level()
        
        leveled_up = False
        while self.progress.experience >= exp_needed:
            self.progress.experience -= exp_needed
            self.level_up()
            exp_needed = self.get_exp_to_next_level()
            leveled_up = True
        
        return leveled_up
    
    def get_exp_to_next_level(self) -> int:
        """Calculate experience needed for next level."""
        return 100 * self.progress.level
    
    def level_up(self):
        """Level up the player."""
        self.progress.level += 1
        self.progress.skill_points += 3
        
        # Increase max stats
        self.stats.max_health += 10
        self.stats.max_stamina += 5
        self.stats.max_mana += 5
        
        # Restore health/stamina/mana on level up
        self.stats.health = self.stats.max_health
        self.stats.stamina = self.stats.max_stamina
        self.stats.mana = self.stats.max_mana
    
    def add_item(self, item_id: str) -> bool:
        """Add an item to inventory."""
        self.inventory.append(item_id)
        self.progress.items_collected += 1
        return True
    
    def remove_item(self, item_id: str) -> bool:
        """Remove an item from inventory."""
        if item_id in self.inventory:
            self.inventory.remove(item_id)
            return True
        return False
    
    def has_item(self, item_id: str) -> bool:
        """Check if player has an item."""
        return item_id in self.inventory
    
    def equip_item(self, item_id: str, slot: str, item_data: Dict) -> bool:
        """Equip an item."""
        if not self.has_item(item_id):
            return False
        
        # Unequip current item in slot
        if self.equipped.get(slot):
            old_item = self.equipped[slot]
            # Old item stays in inventory
        
        self.equipped[slot] = item_id
        return True
    
    def unequip_item(self, slot: str) -> bool:
        """Unequip an item from a slot."""
        if self.equipped.get(slot):
            self.equipped[slot] = None
            return True
        return False
    
    def add_companion(self, companion_id: str):
        """Add a companion."""
        if companion_id not in self.companions:
            self.companions.append(companion_id)
    
    def remove_companion(self, companion_id: str):
        """Remove a companion."""
        if companion_id in self.companions:
            self.companions.remove(companion_id)
        if self.active_companion == companion_id:
            self.active_companion = None
    
    def start_quest(self, quest_id: str):
        """Start a new quest."""
        if quest_id not in self.active_quests:
            self.active_quests.append(quest_id)
            self.quest_progress[quest_id] = {}
    
    def complete_quest(self, quest_id: str):
        """Mark a quest as completed."""
        if quest_id in self.active_quests:
            self.active_quests.remove(quest_id)
        if quest_id not in self.completed_quests:
            self.completed_quests.append(quest_id)
    
    def update_reputation(self, npc_id: str, amount: int):
        """Update reputation with an NPC."""
        current = self.reputation.get(npc_id, 0)
        self.reputation[npc_id] = max(-100, min(100, current + amount))
    
    def discover_location(self, location_id: str):
        """Mark a location as discovered."""
        if location_id not in self.discovered_locations:
            self.discovered_locations.append(location_id)
        
        # Track visit count
        self.visited_count[location_id] = self.visited_count.get(location_id, 0) + 1
    
    def learn_recipe(self, recipe_id: str):
        """Learn a crafting recipe."""
        if recipe_id not in self.known_recipes:
            self.known_recipes.append(recipe_id)
    
    def unlock_achievement(self, achievement_id: str):
        """Unlock an achievement."""
        if achievement_id not in self.achievements:
            self.achievements.append(achievement_id)
    
    def add_lore(self, lore_id: str):
        """Add a discovered lore entry."""
        if lore_id not in self.lore_discovered:
            self.lore_discovered.append(lore_id)
    
    def update_status_effect(self, effect: str, duration: int):
        """Add or update a status effect."""
        self.status_effects[effect] = duration
    
    def tick_status_effects(self):
        """Decrease duration of status effects each turn."""
        expired = []
        for effect, duration in self.status_effects.items():
            self.status_effects[effect] -= 1
            if self.status_effects[effect] <= 0:
                expired.append(effect)
        
        for effect in expired:
            del self.status_effects[effect]
    
    def get_save_data(self) -> Dict:
        """Get player data for saving."""
        return {
            'name': self.name,
            'stats': {
                'health': self.stats.health,
                'max_health': self.stats.max_health,
                'stamina': self.stats.stamina,
                'max_stamina': self.stats.max_stamina,
                'mana': self.stats.mana,
                'max_mana': self.stats.max_mana,
                'hunger': self.stats.hunger,
                'thirst': self.stats.thirst,
                'sanity': self.stats.sanity
            },
            'progress': {
                'experience': self.progress.experience,
                'level': self.progress.level,
                'skill_points': self.progress.skill_points,
                'gold': self.progress.gold,
                'play_time': self.progress.play_time,
                'deaths': self.progress.deaths,
                'kills': self.progress.kills
            },
            'inventory': self.inventory,
            'equipped': self.equipped,
            'skills': self.skills,
            'current_location': self.current_location,
            'discovered_locations': self.discovered_locations,
            'active_quests': self.active_quests,
            'completed_quests': self.completed_quests,
            'quest_progress': self.quest_progress,
            'known_recipes': self.known_recipes,
            'companions': self.companions,
            'active_companion': self.active_companion,
            'reputation': self.reputation,
            'achievements': self.achievements,
            'lore_discovered': self.lore_discovered,
            'status_effects': self.status_effects
        }
    
    @classmethod
    def from_save_data(cls, data: Dict) -> 'Player':
        """Create a player from save data."""
        player = cls(data.get('name', 'Traveler'))
        
        # Restore stats
        stats_data = data.get('stats', {})
        for key, value in stats_data.items():
            setattr(player.stats, key, value)
        
        # Restore progress
        progress_data = data.get('progress', {})
        for key, value in progress_data.items():
            setattr(player.progress, key, value)
        
        # Restore other data
        player.inventory = data.get('inventory', [])
        player.equipped = data.get('equipped', {})
        player.skills = data.get('skills', {})
        player.current_location = data.get('current_location', 'clearing')
        player.discovered_locations = data.get('discovered_locations', [])
        player.active_quests = data.get('active_quests', [])
        player.completed_quests = data.get('completed_quests', [])
        player.quest_progress = data.get('quest_progress', {})
        player.known_recipes = data.get('known_recipes', [])
        player.companions = data.get('companions', [])
        player.active_companion = data.get('active_companion')
        player.reputation = data.get('reputation', {})
        player.achievements = data.get('achievements', [])
        player.lore_discovered = data.get('lore_discovered', [])
        player.status_effects = data.get('status_effects', {})
        
        return player
