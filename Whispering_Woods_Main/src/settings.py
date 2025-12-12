"""
Game settings and configuration
"""

from typing import Dict


class GameSettings:
    """Global game settings and configuration."""
    
    def __init__(self):
        # Display settings
        self.text_speed = 0.03
        self.enable_colors = True
        self.enable_sound = False
        
        # Gameplay settings
        self.auto_save = True
        self.difficulty = "normal"  # easy, normal, hard
        self.show_hints = True
        self.confirm_actions = True
        
        # Debug/Admin settings
        self.debug_mode = False
        self.admin_mode = False
        self.god_mode = False
        self.infinite_inventory = False
        self.no_hunger = False
        self.no_thirst = False
        self.instant_kill = False
        self.reveal_map = False
        self.unlimited_gold = False
        self.skip_combat = False
        self.unlimited_mana = False
        
    def to_dict(self) -> Dict:
        """Convert settings to dictionary for saving."""
        return self.__dict__.copy()
    
    def from_dict(self, data: Dict):
        """Load settings from dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.__init__()


# Global settings instance
SETTINGS = GameSettings()


# ASCII Title Art
GAME_TITLE = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ██╗      ██████╗ ███████╗████████╗    ██╗███╗   ██╗                       ║
║     ██║     ██╔═══██╗██╔════╝╚══██╔══╝    ██║████╗  ██║                       ║
║     ██║     ██║   ██║███████╗   ██║       ██║██╔██╗ ██║                       ║
║     ██║     ██║   ██║╚════██║   ██║       ██║██║╚██╗██║                       ║
║     ███████╗╚██████╔╝███████║   ██║       ██║██║ ╚████║                       ║
║     ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝       ╚═╝╚═╝  ╚═══╝                       ║
║                                                                               ║
║          ████████╗██╗  ██╗███████╗                                            ║
║          ╚══██╔══╝██║  ██║██╔════╝                                            ║
║             ██║   ███████║█████╗                                              ║
║             ██║   ██╔══██║██╔══╝                                              ║
║             ██║   ██║  ██║███████╗                                            ║
║             ╚═╝   ╚═╝  ╚═╝╚══════╝                                            ║
║                                                                               ║
║  ██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ ██╗███╗   ██╗ ██████╗   ║
║  ██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║████╗  ██║██╔════╝   ║
║  ██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝██║██╔██╗ ██║██║  ███╗  ║
║  ██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗██║██║╚██╗██║██║   ██║  ║
║  ╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║██║██║ ╚████║╚██████╔╝  ║
║   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝   ║
║                                                                               ║
║              ██╗    ██╗ ██████╗  ██████╗ ██████╗ ███████╗                     ║
║              ██║    ██║██╔═══██╗██╔═══██╗██╔══██╗██╔════╝                     ║
║              ██║ █╗ ██║██║   ██║██║   ██║██║  ██║███████╗                     ║
║              ██║███╗██║██║   ██║██║   ██║██║  ██║╚════██║                     ║
║              ╚███╔███╔╝╚██████╔╝╚██████╔╝██████╔╝███████║                     ║
║               ╚══╝╚══╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝                     ║
║                                                                               ║
║                           Version 2.0 - Enhanced Edition                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""


ADMIN_PASSWORD = "forestmaster2024"
