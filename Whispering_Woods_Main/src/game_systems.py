"""
Core game systems: Combat, Crafting, Time/Weather, Quests, Achievements
"""

import random
import time
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum, auto


class TimeOfDay(Enum):
    """Time of day enumeration"""
    DAWN = auto()
    MORNING = auto()
    MIDDAY = auto()
    AFTERNOON = auto()
    EVENING = auto()
    DUSK = auto()
    NIGHT = auto()
    MIDNIGHT = auto()


class Weather(Enum):
    """Weather conditions"""
    CLEAR = auto()
    CLOUDY = auto()
    RAIN = auto()
    STORM = auto()
    FOG = auto()
    SNOW = auto()
    BLIZZARD = auto()


class DifficultyMode(Enum):
    """Difficulty levels"""
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    NIGHTMARE = "nightmare"


class TimeWeatherSystem:
    """Manages game time and weather"""
    
    def __init__(self):
        self.current_time = 480  # Minutes since midnight (8:00 AM)
        self.day_count = 1
        self.weather = Weather.CLEAR
        self.weather_duration = 120  # Minutes remaining for current weather
        
    def advance_time(self, minutes: int):
        """Advance game time"""
        self.current_time += minutes
        self.weather_duration -= minutes
        
        # Handle day rollover
        while self.current_time >= 1440:  # 24 hours
            self.current_time -= 1440
            self.day_count += 1
        
        # Change weather if duration expired
        if self.weather_duration <= 0:
            self.change_weather()
    
    def change_weather(self):
        """Randomly change weather"""
        weather_options = list(Weather)
        weights = [40, 30, 15, 5, 10, 8, 2]  # Probability weights
        self.weather = random.choices(weather_options, weights=weights)[0]
        self.weather_duration = random.randint(60, 240)
    
    def get_time_of_day(self) -> TimeOfDay:
        """Get current time of day"""
        hour = self.current_time // 60
        if 5 <= hour < 7:
            return TimeOfDay.DAWN
        elif 7 <= hour < 11:
            return TimeOfDay.MORNING
        elif 11 <= hour < 13:
            return TimeOfDay.MIDDAY
        elif 13 <= hour < 17:
            return TimeOfDay.AFTERNOON
        elif 17 <= hour < 19:
            return TimeOfDay.EVENING
        elif 19 <= hour < 21:
            return TimeOfDay.DUSK
        elif 21 <= hour < 24 or 0 <= hour < 2:
            return TimeOfDay.NIGHT
        else:
            return TimeOfDay.MIDNIGHT
    
    def get_time_string(self) -> str:
        """Get formatted time string"""
        hour = self.current_time // 60
        minute = self.current_time % 60
        period = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour}:{minute:02d} {period}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for saving"""
        return {
            'current_time': self.current_time,
            'day_count': self.day_count,
            'weather': self.weather.name,
            'weather_duration': self.weather_duration
        }
    
    def from_dict(self, data: Dict):
        """Load from dictionary"""
        self.current_time = data.get('current_time', 480)
        self.day_count = data.get('day_count', 1)
        weather_name = data.get('weather', 'CLEAR')
        self.weather = Weather[weather_name] if weather_name in Weather.__members__ else Weather.CLEAR
        self.weather_duration = data.get('weather_duration', 120)


class CombatSystem:
    """Handles combat mechanics"""
    
    @staticmethod
    def calculate_damage(attacker_stats: Dict, defender_stats: Dict, weapon_data: Optional[Dict] = None) -> Tuple[int, str]:
        """Calculate damage from an attack"""
        base_damage = attacker_stats.get('strength', 10)
        
        # Add weapon damage
        if weapon_data:
            base_damage += weapon_data.get('damage', 0)
        
        # Add random variance
        variance = random.randint(-3, 3)
        total_damage = max(1, base_damage + variance)
        
        # Apply defender's defense
        defense = defender_stats.get('defense', 0)
        mitigation = defense // 2
        final_damage = max(1, total_damage - mitigation)
        
        # Determine hit type
        crit_chance = attacker_stats.get('crit_chance', 5)
        if random.randint(1, 100) <= crit_chance:
            final_damage = int(final_damage * 1.5)
            hit_type = "CRITICAL HIT"
        else:
            hit_type = "hit"
        
        return final_damage, hit_type
    
    @staticmethod
    def calculate_spell_damage(spell_data: Dict, caster_intelligence: int) -> int:
        """Calculate spell damage"""
        base_damage = spell_data.get('damage', 0)
        intelligence_bonus = caster_intelligence // 10
        total_damage = base_damage + intelligence_bonus
        return max(1, total_damage)


class CraftingSystem:
    """Handles item crafting"""
    
    @staticmethod
    def can_craft(recipe: Dict, inventory: List[str], items_data: Dict) -> Tuple[bool, str]:
        """Check if player can craft an item"""
        required_items = recipe.get('required_items', {})
        
        # Count items in inventory
        inventory_counts = {}
        for item_id in inventory:
            inventory_counts[item_id] = inventory_counts.get(item_id, 0) + 1
        
        # Check requirements
        for item_id, required_count in required_items.items():
            if inventory_counts.get(item_id, 0) < required_count:
                item_name = items_data.get(item_id, {}).get('name', item_id)
                have = inventory_counts.get(item_id, 0)
                return False, f"Need {required_count} {item_name} (have {have})"
        
        # Check level requirement
        level_req = recipe.get('level_required', 1)
        
        return True, "Can craft"
    
    @staticmethod
    def craft_item(recipe: Dict, inventory: List[str]) -> Tuple[List[str], str]:
        """Craft an item, removing required materials"""
        required_items = recipe.get('required_items', {})
        new_inventory = inventory.copy()
        
        # Remove required items
        for item_id, count in required_items.items():
            removed = 0
            while removed < count and item_id in new_inventory:
                new_inventory.remove(item_id)
                removed += 1
        
        # Add crafted item
        result_item = recipe.get('result', '')
        if result_item:
            new_inventory.append(result_item)
        
        return new_inventory, result_item


class QuestSystem:
    """Manages quest progression"""
    
    @staticmethod
    def check_quest_requirements(quest: Dict, player_data: Dict) -> Tuple[bool, str]:
        """Check if player meets quest requirements"""
        # Check level
        level_req = quest.get('level_required', 1)
        if player_data.get('level', 1) < level_req:
            return False, f"Requires level {level_req}"
        
        # Check prerequisite quests
        prerequisites = quest.get('prerequisites', [])
        completed_quests = player_data.get('completed_quests', [])
        for prereq in prerequisites:
            if prereq not in completed_quests:
                return False, f"Must complete prerequisite quest: {prereq}"
        
        return True, "Requirements met"
    
    @staticmethod
    def update_quest_progress(quest_progress: Dict, quest_id: str, objective_id: str, amount: int = 1) -> Dict:
        """Update progress on a quest objective"""
        if quest_id not in quest_progress:
            quest_progress[quest_id] = {}
        
        if objective_id not in quest_progress[quest_id]:
            quest_progress[quest_id][objective_id] = 0
        
        quest_progress[quest_id][objective_id] += amount
        return quest_progress
    
    @staticmethod
    def is_quest_complete(quest: Dict, quest_progress: Dict, quest_id: str) -> bool:
        """Check if all quest objectives are complete"""
        objectives = quest.get('objectives', [])
        progress = quest_progress.get(quest_id, {})
        
        for obj in objectives:
            obj_id = obj.get('id', '')
            required = obj.get('count', 1)
            current = progress.get(obj_id, 0)
            if current < required:
                return False
        
        return True


class AchievementSystem:
    """Manages achievements"""
    
    @staticmethod
    def check_achievement(achievement: Dict, player_data: Dict) -> bool:
        """Check if achievement conditions are met"""
        conditions = achievement.get('conditions', {})
        
        for key, value in conditions.items():
            player_value = player_data.get(key, 0)
            if player_value < value:
                return False
        
        return True
    
    @staticmethod
    def award_achievement(achievement_id: str, unlocked_achievements: List[str]) -> Tuple[bool, List[str]]:
        """Award an achievement if not already unlocked"""
        if achievement_id not in unlocked_achievements:
            unlocked_achievements.append(achievement_id)
            return True, unlocked_achievements
        return False, unlocked_achievements


class SaveLoadSystem:
    """Handles game state persistence"""
    
    @staticmethod
    def create_save_data(player, time_weather: TimeWeatherSystem, game_state: Dict) -> Dict:
        """Create complete save data"""
        save_data = {
            'player': player.get_save_data(),
            'time_weather': time_weather.to_dict(),
            'game_state': game_state,
            'version': '2.0',
            'timestamp': time.time()
        }
        return save_data
    
    @staticmethod
    def validate_save_data(data: Dict) -> Tuple[bool, str]:
        """Validate save file structure"""
        required_keys = ['player', 'time_weather', 'game_state']
        
        for key in required_keys:
            if key not in data:
                return False, f"Missing required key: {key}"
        
        return True, "Valid save file"
