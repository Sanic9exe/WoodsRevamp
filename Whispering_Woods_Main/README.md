# Lost in the Whispering Woods - Revamped Edition

Version 2.0

A text-based adventure game featuring a mysterious forest filled with danger, magic, and secrets.

## Features

- **25 Unique NPCs** - Each with their own personality, backstory, and dialogue
- **10 Recruitable Companions** - Diverse allies with unique abilities
- **30+ Creatures** - From wolves to dragons, with boss battles
- **35+ Locations** - Richly described areas to explore
- **35+ Quests** - Main story, side quests, combat missions, and more
- **Crafting System** - Create potions, weapons, and useful items
- **Achievement System** - Track your progress and accomplishments
- **Rich Lore** - Discover the secrets of the Whispering Woods
- **Modular Design** - All game data stored in easy-to-edit JSON files

## Quality Over Quantity

This revamp focuses on quality content:
- Reduced NPCs from 300+ to 25 unique, memorable characters
- Curated locations with detailed descriptions
- Meaningful quests with engaging storylines
- Strategic companion choices that matter
- Balanced gameplay that respects player time

## Installation

1. Ensure you have Python 3.7 or higher installed
2. Navigate to the Whispering_Woods_Main directory
3. Run the game:
   ```bash
   python game.py
   ```

## Project Structure

```
Whispering_Woods_Main/
├── game.py              # Main game file
├── src/                 # Source code modules
│   ├── __init__.py
│   ├── colors.py        # Color constants
│   ├── data_loader.py   # JSON data loader
│   ├── player.py        # Player class
│   └── utils.py         # Utility functions
└── data/                # Game data (JSON files)
    ├── npcs.json        # NPC definitions
    ├── items.json       # Item definitions
    ├── creatures.json   # Creature definitions
    ├── locations.json   # Location definitions
    ├── companions.json  # Companion definitions
    ├── quests.json      # Quest definitions
    ├── crafting.json    # Crafting recipes
    ├── achievements.json# Achievement definitions
    └── lore.json        # Lore entries
```

## Gameplay

### Commands

- `explore` - Move to a different location
- `look` - Search the current area
- `inventory` - View your items
- `stats` - View detailed character stats
- `talk` - Talk to NPCs
- `companions` - Manage your companions
- `quests` - View your quests
- `map` - View discovered locations
- `rest` - Rest to restore health
- `craft` - Craft items
- `save` - Save your game
- `help` - Show help message
- `quit` - Exit the game

### Tips

1. **Explore thoroughly** - Many secrets are hidden in plain sight
2. **Talk to everyone** - NPCs have valuable information and quests
3. **Choose companions wisely** - Each has unique abilities that complement different playstyles
4. **Save frequently** - The forest is dangerous
5. **Read the lore** - Understanding the forest's history helps you survive

## Customization

All game content is stored in JSON files in the `data/` directory. You can easily:
- Add new NPCs, items, creatures, or locations
- Modify existing content
- Create new quests
- Add crafting recipes
- Design new companions

Simply edit the JSON files and restart the game!

## Game Design Philosophy

This revamp follows these principles:

1. **Quality over Quantity** - Better to have 25 memorable NPCs than 300 forgettable ones
2. **Modular Design** - Code is organized into logical modules for easy maintenance
3. **Data-Driven** - Game content separated from code for easy modification
4. **Player Respect** - Engaging content without artificial padding
5. **Replayability** - Multiple paths, choices, and outcomes

## Future Enhancements

Potential additions:
- Full combat system implementation
- Advanced crafting mechanics
- Dynamic events system
- Multiple endings based on choices
- Enhanced companion interactions
- Trading system
- Faction reputation system

## Credits

**Original Concept**: Sanic9exe
**Revamp & Refactoring**: AI Assistant (Claude)

## License

This is a personal project. Feel free to modify and enjoy!
