"""
Admin Panel - Debug tools and cheats for development/testing
"""

from typing import Dict, Any, Optional
from .settings import SETTINGS, ADMIN_PASSWORD
from .colors import Colors, colored_text
from .utils import instant_print, slow_type, get_input, get_number_input, clear_screen, press_enter_to_continue


class AdminPanel:
    """Admin panel for debugging and testing"""
    
    @staticmethod
    def authenticate() -> bool:
        """Check admin password"""
        instant_print(colored_text("\n=== ADMIN AUTHENTICATION ===", Colors.BOLD_RED))
        password = get_input("Enter admin password: ")
        
        if password == ADMIN_PASSWORD:
            SETTINGS.admin_mode = True
            instant_print(colored_text("✓ Admin mode activated", Colors.GREEN))
            return True
        else:
            instant_print(colored_text("✗ Incorrect password", Colors.RED))
            return False
    
    @staticmethod
    def show_menu(player, game_data: Dict, time_weather: Any):
        """Display admin menu"""
        if not SETTINGS.admin_mode:
            if not AdminPanel.authenticate():
                return
        
        while True:
            clear_screen()
            instant_print(colored_text("╔═══════════════════════════════════════════════════════╗", Colors.BOLD_RED))
            instant_print(colored_text("║              🔧 ADMIN PANEL 🔧                        ║", Colors.BOLD_RED))
            instant_print(colored_text("╚═══════════════════════════════════════════════════════╝", Colors.BOLD_RED))
            
            instant_print(colored_text("\n=== CHEAT TOGGLES ===", Colors.YELLOW))
            instant_print(f"1. God Mode: {colored_text('ON' if SETTINGS.god_mode else 'OFF', Colors.GREEN if SETTINGS.god_mode else Colors.RED)}")
            instant_print(f"2. Infinite Inventory: {colored_text('ON' if SETTINGS.infinite_inventory else 'OFF', Colors.GREEN if SETTINGS.infinite_inventory else Colors.RED)}")
            instant_print(f"3. Unlimited Gold: {colored_text('ON' if SETTINGS.unlimited_gold else 'OFF', Colors.GREEN if SETTINGS.unlimited_gold else Colors.RED)}")
            instant_print(f"4. Unlimited Mana: {colored_text('ON' if SETTINGS.unlimited_mana else 'OFF', Colors.GREEN if SETTINGS.unlimited_mana else Colors.RED)}")
            instant_print(f"5. Skip Combat: {colored_text('ON' if SETTINGS.skip_combat else 'OFF', Colors.GREEN if SETTINGS.skip_combat else Colors.RED)}")
            instant_print(f"6. Instant Kill: {colored_text('ON' if SETTINGS.instant_kill else 'OFF', Colors.GREEN if SETTINGS.instant_kill else Colors.RED)}")
            instant_print(f"7. Reveal Map: {colored_text('ON' if SETTINGS.reveal_map else 'OFF', Colors.GREEN if SETTINGS.reveal_map else Colors.RED)}")
            instant_print(f"8. No Hunger/Thirst: {colored_text('ON' if SETTINGS.no_hunger else 'OFF', Colors.GREEN if SETTINGS.no_hunger else Colors.RED)}")
            
            instant_print(colored_text("\n=== PLAYER MODIFICATION ===", Colors.YELLOW))
            instant_print("9. Set Health")
            instant_print("10. Set Mana")
            instant_print("11. Set Gold")
            instant_print("12. Set Level")
            instant_print("13. Max All Stats")
            instant_print("14. Add Experience")
            
            instant_print(colored_text("\n=== INVENTORY ===", Colors.YELLOW))
            instant_print("15. Give Item")
            instant_print("16. Give All Items")
            instant_print("17. Learn Spell")
            instant_print("18. Learn All Spells")
            instant_print("19. Clear Inventory")
            
            instant_print(colored_text("\n=== WORLD ===", Colors.YELLOW))
            instant_print("20. Teleport to Location")
            instant_print("21. Change Time")
            instant_print("22. Change Weather")
            instant_print("23. Complete Current Quest")
            instant_print("24. Unlock All Achievements")
            
            instant_print(colored_text("\n=== INFO ===", Colors.YELLOW))
            instant_print("25. Show Debug Info")
            instant_print("26. List All Data")
            
            instant_print(colored_text("\n0. Exit Admin Panel", Colors.CYAN))
            
            choice = get_input("\nSelect option: ")
            
            if choice == "0":
                break
            elif choice == "1":
                AdminPanel._toggle_god_mode()
            elif choice == "2":
                AdminPanel._toggle_infinite_inventory()
            elif choice == "3":
                AdminPanel._toggle_unlimited_gold()
            elif choice == "4":
                AdminPanel._toggle_unlimited_mana()
            elif choice == "5":
                AdminPanel._toggle_skip_combat()
            elif choice == "6":
                AdminPanel._toggle_instant_kill()
            elif choice == "7":
                AdminPanel._toggle_reveal_map()
            elif choice == "8":
                AdminPanel._toggle_no_hunger()
            elif choice == "9":
                AdminPanel._set_health(player)
            elif choice == "10":
                AdminPanel._set_mana(player)
            elif choice == "11":
                AdminPanel._set_gold(player)
            elif choice == "12":
                AdminPanel._set_level(player)
            elif choice == "13":
                AdminPanel._max_all_stats(player)
            elif choice == "14":
                AdminPanel._add_experience(player)
            elif choice == "15":
                AdminPanel._give_item(player, game_data)
            elif choice == "16":
                AdminPanel._give_all_items(player, game_data)
            elif choice == "17":
                AdminPanel._learn_spell(player, game_data)
            elif choice == "18":
                AdminPanel._learn_all_spells(player, game_data)
            elif choice == "19":
                AdminPanel._clear_inventory(player)
            elif choice == "20":
                AdminPanel._teleport(player, game_data)
            elif choice == "21":
                AdminPanel._change_time(time_weather)
            elif choice == "22":
                AdminPanel._change_weather(time_weather)
            elif choice == "23":
                AdminPanel._complete_quest(player)
            elif choice == "24":
                AdminPanel._unlock_all_achievements(player, game_data)
            elif choice == "25":
                AdminPanel._show_debug_info(player, game_data, time_weather)
            elif choice == "26":
                AdminPanel._list_all_data(game_data)
            else:
                instant_print(colored_text("Invalid choice", Colors.RED))
            
            press_enter_to_continue()
    
    # Toggle methods
    @staticmethod
    def _toggle_god_mode():
        SETTINGS.god_mode = not SETTINGS.god_mode
        instant_print(colored_text(f"God Mode: {'ON' if SETTINGS.god_mode else 'OFF'}", Colors.GREEN))
    
    @staticmethod
    def _toggle_infinite_inventory():
        SETTINGS.infinite_inventory = not SETTINGS.infinite_inventory
        instant_print(colored_text(f"Infinite Inventory: {'ON' if SETTINGS.infinite_inventory else 'OFF'}", Colors.GREEN))
    
    @staticmethod
    def _toggle_unlimited_gold():
        SETTINGS.unlimited_gold = not SETTINGS.unlimited_gold
        instant_print(colored_text(f"Unlimited Gold: {'ON' if SETTINGS.unlimited_gold else 'OFF'}", Colors.GREEN))
    
    @staticmethod
    def _toggle_unlimited_mana():
        SETTINGS.unlimited_mana = not SETTINGS.unlimited_mana
        instant_print(colored_text(f"Unlimited Mana: {'ON' if SETTINGS.unlimited_mana else 'OFF'}", Colors.GREEN))
    
    @staticmethod
    def _toggle_skip_combat():
        SETTINGS.skip_combat = not SETTINGS.skip_combat
        instant_print(colored_text(f"Skip Combat: {'ON' if SETTINGS.skip_combat else 'OFF'}", Colors.GREEN))
    
    @staticmethod
    def _toggle_instant_kill():
        SETTINGS.instant_kill = not SETTINGS.instant_kill
        instant_print(colored_text(f"Instant Kill: {'ON' if SETTINGS.instant_kill else 'OFF'}", Colors.GREEN))
    
    @staticmethod
    def _toggle_reveal_map():
        SETTINGS.reveal_map = not SETTINGS.reveal_map
        instant_print(colored_text(f"Reveal Map: {'ON' if SETTINGS.reveal_map else 'OFF'}", Colors.GREEN))
    
    @staticmethod
    def _toggle_no_hunger():
        SETTINGS.no_hunger = not SETTINGS.no_hunger
        instant_print(colored_text(f"No Hunger/Thirst: {'ON' if SETTINGS.no_hunger else 'OFF'}", Colors.GREEN))
    
    # Player modification methods
    @staticmethod
    def _set_health(player):
        amount = get_number_input("Enter health amount: ", 1, 9999)
        if amount:
            player.stats.health = amount
            player.stats.max_health = max(player.stats.max_health, amount)
            instant_print(colored_text(f"Health set to {amount}", Colors.GREEN))
    
    @staticmethod
    def _set_mana(player):
        amount = get_number_input("Enter mana amount: ", 0, 9999)
        if amount is not None:
            player.stats.mana = amount
            player.stats.max_mana = max(player.stats.max_mana, amount)
            instant_print(colored_text(f"Mana set to {amount}", Colors.GREEN))
    
    @staticmethod
    def _set_gold(player):
        amount = get_number_input("Enter gold amount: ", 0, 999999)
        if amount is not None:
            player.progress.gold = amount
            instant_print(colored_text(f"Gold set to {amount}", Colors.GREEN))
    
    @staticmethod
    def _set_level(player):
        level = get_number_input("Enter level: ", 1, 100)
        if level:
            player.progress.level = level
            instant_print(colored_text(f"Level set to {level}", Colors.GREEN))
    
    @staticmethod
    def _max_all_stats(player):
        player.stats.health = 9999
        player.stats.max_health = 9999
        player.stats.mana = 9999
        player.stats.max_mana = 9999
        player.stats.stamina = 9999
        player.stats.max_stamina = 9999
        player.progress.gold = 999999
        player.progress.level = 100
        for skill in player.skills:
            player.skills[skill] = 100
        instant_print(colored_text("All stats maxed!", Colors.GREEN))
    
    @staticmethod
    def _add_experience(player):
        amount = get_number_input("Enter XP amount: ", 1, 999999)
        if amount:
            player.gain_experience(amount)
            instant_print(colored_text(f"Added {amount} XP", Colors.GREEN))
    
    # Inventory methods
    @staticmethod
    def _give_item(player, game_data):
        items = game_data.get('items', {})
        instant_print(colored_text("\nAvailable items:", Colors.CYAN))
        item_list = list(items.keys())[:20]  # Show first 20
        for i, item_id in enumerate(item_list, 1):
            item_name = items[item_id].get('name', item_id)
            instant_print(f"{i}. {item_name} ({item_id})")
        
        item_id = get_input("\nEnter item ID: ")
        if item_id in items:
            player.add_item(item_id)
            instant_print(colored_text(f"Added {items[item_id]['name']}", Colors.GREEN))
        else:
            instant_print(colored_text("Item not found", Colors.RED))
    
    @staticmethod
    def _give_all_items(player, game_data):
        items = game_data.get('items', {})
        for item_id in items.keys():
            player.add_item(item_id)
        instant_print(colored_text(f"Added all {len(items)} items!", Colors.GREEN))
    
    @staticmethod
    def _learn_spell(player, game_data):
        spells = game_data.get('spells', {})
        instant_print(colored_text("\nAvailable spells:", Colors.CYAN))
        spell_list = list(spells.keys())[:20]  # Show first 20
        for i, spell_id in enumerate(spell_list, 1):
            spell_name = spells[spell_id].get('name', spell_id)
            instant_print(f"{i}. {spell_name} ({spell_id})")
        
        spell_id = get_input("\nEnter spell ID: ")
        if spell_id in spells:
            if player.learn_spell(spell_id):
                instant_print(colored_text(f"Learned {spells[spell_id]['name']}", Colors.GREEN))
            else:
                instant_print(colored_text("Already know this spell", Colors.YELLOW))
        else:
            instant_print(colored_text("Spell not found", Colors.RED))
    
    @staticmethod
    def _learn_all_spells(player, game_data):
        spells = game_data.get('spells', {})
        count = 0
        for spell_id in spells.keys():
            if player.learn_spell(spell_id):
                count += 1
        instant_print(colored_text(f"Learned {count} new spells!", Colors.GREEN))
    
    @staticmethod
    def _clear_inventory(player):
        player.inventory.clear()
        instant_print(colored_text("Inventory cleared", Colors.GREEN))
    
    # World methods
    @staticmethod
    def _teleport(player, game_data):
        locations = game_data.get('locations', {})
        instant_print(colored_text("\nAvailable locations:", Colors.CYAN))
        loc_list = list(locations.keys())[:20]  # Show first 20
        for i, loc_id in enumerate(loc_list, 1):
            loc_name = locations[loc_id].get('name', loc_id)
            instant_print(f"{i}. {loc_name} ({loc_id})")
        
        loc_id = get_input("\nEnter location ID: ")
        if loc_id in locations:
            player.current_location = loc_id
            if loc_id not in player.discovered_locations:
                player.discover_location(loc_id)
            instant_print(colored_text(f"Teleported to {locations[loc_id]['name']}", Colors.GREEN))
        else:
            instant_print(colored_text("Location not found", Colors.RED))
    
    @staticmethod
    def _change_time(time_weather):
        hours = get_number_input("Enter hour (0-23): ", 0, 23)
        if hours is not None:
            minutes = get_number_input("Enter minutes (0-59): ", 0, 59)
            if minutes is not None:
                time_weather.current_time = hours * 60 + minutes
                instant_print(colored_text(f"Time set to {time_weather.get_time_string()}", Colors.GREEN))
    
    @staticmethod
    def _change_weather(time_weather):
        from .game_systems import Weather
        instant_print(colored_text("\nWeather options:", Colors.CYAN))
        for i, weather in enumerate(Weather, 1):
            instant_print(f"{i}. {weather.name}")
        
        choice = get_number_input("Select weather: ", 1, len(Weather))
        if choice:
            weather_list = list(Weather)
            time_weather.weather = weather_list[choice - 1]
            instant_print(colored_text(f"Weather set to {time_weather.weather.name}", Colors.GREEN))
    
    @staticmethod
    def _complete_quest(player):
        if player.active_quests:
            instant_print(colored_text("\nActive quests:", Colors.CYAN))
            for i, quest_id in enumerate(player.active_quests, 1):
                instant_print(f"{i}. {quest_id}")
            
            quest_id = get_input("\nEnter quest ID to complete: ")
            if quest_id in player.active_quests:
                player.active_quests.remove(quest_id)
                player.completed_quests.append(quest_id)
                instant_print(colored_text(f"Quest {quest_id} completed!", Colors.GREEN))
            else:
                instant_print(colored_text("Quest not found", Colors.RED))
        else:
            instant_print(colored_text("No active quests", Colors.YELLOW))
    
    @staticmethod
    def _unlock_all_achievements(player, game_data):
        achievements = game_data.get('achievements', {})
        count = 0
        for ach_id in achievements.keys():
            if ach_id not in player.achievements:
                player.achievements.append(ach_id)
                count += 1
        instant_print(colored_text(f"Unlocked {count} achievements!", Colors.GREEN))
    
    # Info methods
    @staticmethod
    def _show_debug_info(player, game_data, time_weather):
        instant_print(colored_text("\n=== DEBUG INFO ===", Colors.CYAN))
        instant_print(f"Player: {player.name} | Level {player.progress.level}")
        instant_print(f"Location: {player.current_location}")
        instant_print(f"Health: {player.stats.health}/{player.stats.max_health}")
        instant_print(f"Mana: {player.stats.mana}/{player.stats.max_mana}")
        instant_print(f"Gold: {player.progress.gold}")
        instant_print(f"XP: {player.progress.experience}")
        instant_print(f"Inventory: {len(player.inventory)} items")
        instant_print(f"Known Spells: {len(player.known_spells)}")
        instant_print(f"Active Quests: {len(player.active_quests)}")
        instant_print(f"Completed Quests: {len(player.completed_quests)}")
        instant_print(f"Companions: {len(player.companions)}")
        instant_print(f"Time: Day {time_weather.day_count}, {time_weather.get_time_string()}")
        instant_print(f"Weather: {time_weather.weather.name}")
    
    @staticmethod
    def _list_all_data(game_data):
        instant_print(colored_text("\n=== GAME DATA SUMMARY ===", Colors.CYAN))
        for key, value in game_data.items():
            if isinstance(value, dict):
                instant_print(f"{key}: {len(value)} entries")
            else:
                instant_print(f"{key}: {type(value).__name__}")
