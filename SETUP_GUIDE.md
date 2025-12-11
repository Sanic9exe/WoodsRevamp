# Whispering Woods - Setup and Play Guide

## Quick Start

### Files You Need

All game files are contained in the **`Whispering_Woods_Main/`** folder. You need:

**Essential Files:**
- `game.py` - Main game executable
- `run_game.sh` - Launch script (optional)
- `src/` folder - Python modules (5 files)
- `data/` folder - Game content (10 JSON files)

**Optional Files:**
- `README.md` - Game documentation
- `../COMPLETION_SUMMARY.md` - Project details

### Complete File List

```
Whispering_Woods_Main/
├── game.py                    ← Main game file (run this!)
├── run_game.sh               ← Launch script (alternative)
├── README.md                 ← Game documentation
├── src/                      ← Python modules (required)
│   ├── __init__.py
│   ├── colors.py             ← Terminal colors
│   ├── data_loader.py        ← JSON data loader
│   ├── player.py             ← Player character system
│   └── utils.py              ← Utility functions
└── data/                     ← Game content (required)
    ├── npcs.json             ← 26 unique NPCs
    ├── items.json            ← 48 items
    ├── creatures.json        ← 28 creatures
    ├── locations.json        ← 28 locations
    ├── companions.json       ← 10 companions
    ├── quests.json           ← 25 quests
    ├── crafting.json         ← 20 recipes
    ├── achievements.json     ← 20 achievements
    ├── events.json           ← 8 random events
    └── lore.json             ← 15 lore entries
```

---

## Setup Instructions

### Step 1: Prerequisites

**Python 3.7 or higher** is required. Check your version:

```bash
python3 --version
```

If you don't have Python 3.7+, download it from [python.org](https://www.python.org/downloads/)

**No external dependencies needed!** The game uses only Python standard library.

---

### Step 2: Download the Game

**Option A: Clone the Repository**
```bash
git clone https://github.com/Sanic9exe/WoodsRevamp.git
cd WoodsRevamp/Whispering_Woods_Main
```

**Option B: Download ZIP**
1. Go to the repository page
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Navigate to the `Whispering_Woods_Main` folder

---

### Step 3: Verify Files

Make sure you have all required files:

```bash
cd Whispering_Woods_Main
ls -la
```

You should see:
- `game.py`
- `run_game.sh`
- `src/` folder
- `data/` folder

Check that data files exist:
```bash
ls data/
```

You should see 10 JSON files.

---

### Step 4: Launch the Game

**Method 1: Direct Python (Recommended)**

```bash
cd Whispering_Woods_Main
python3 game.py
```

**Method 2: Launch Script (Linux/Mac)**

First, make the script executable:
```bash
chmod +x run_game.sh
```

Then run it:
```bash
./run_game.sh
```

**Method 3: Windows**

```cmd
cd Whispering_Woods_Main
python game.py
```

---

## First Launch

When you run the game, you'll see:

1. **Loading Screen** - Game data loads (26 NPCs, 48 items, etc.)
2. **Main Menu** with options:
   - New Game
   - Load Game
   - Instructions
   - Credits
   - Exit

Select "New Game" to start your adventure!

---

## Game Controls

### Basic Commands

Type these commands during gameplay:

**Navigation:**
- `explore` - Move to different locations
- `look` - Search current area
- `map` - View discovered locations

**Character:**
- `inventory` or `i` - View your items
- `stats` - View character stats
- `equipment` - Manage equipped items

**Interaction:**
- `talk` - Speak with NPCs
- `companions` - Manage party members
- `quests` or `q` - View active quests

**Actions:**
- `rest` - Restore health and stamina
- `craft` - Create items
- `save` - Save your progress
- `help` - Show all commands
- `quit` - Exit game

---

## Quick Tips

1. **Save Often** - Use the `save` command to preserve progress
2. **Talk to Everyone** - NPCs give quests and valuable information
3. **Explore Thoroughly** - Many locations have hidden items
4. **Rest in Safe Areas** - Look for inns and safe zones
5. **Read the Lore** - Discover the forest's secrets

---

## Troubleshooting

### "Command not found: python3"

Try `python` instead of `python3`:
```bash
python game.py
```

### "No module named 'src'"

Make sure you're in the `Whispering_Woods_Main` directory:
```bash
cd Whispering_Woods_Main
python3 game.py
```

### "FileNotFoundError" for JSON files

Verify the `data/` folder exists and contains JSON files:
```bash
ls data/
```

All 10 JSON files should be present.

### Game crashes on startup

Check Python version (must be 3.7+):
```bash
python3 --version
```

### Colors don't display correctly (Windows)

Windows Command Prompt may not support ANSI colors. Try:
- Windows Terminal (recommended)
- PowerShell
- Git Bash

---

## Save Files

Save files are stored as:
- `whispering_woods_save.json` (in the game directory)

**To backup your save:**
```bash
cp whispering_woods_save.json whispering_woods_save_backup.json
```

**To restore a save:**
```bash
cp whispering_woods_save_backup.json whispering_woods_save.json
```

---

## Uninstalling

Simply delete the `Whispering_Woods_Main` folder:

```bash
rm -rf Whispering_Woods_Main
```

Or on Windows:
```cmd
rmdir /s Whispering_Woods_Main
```

---

## Additional Resources

- **Game README**: `Whispering_Woods_Main/README.md` - Detailed game info
- **Completion Summary**: `COMPLETION_SUMMARY.md` - Development details
- **Main README**: `README.md` - Project overview

---

## File Links (for reference)

**Core Game Files:**
- [`Whispering_Woods_Main/game.py`](Whispering_Woods_Main/game.py) - Main executable
- [`Whispering_Woods_Main/run_game.sh`](Whispering_Woods_Main/run_game.sh) - Launch script

**Python Modules:**
- [`Whispering_Woods_Main/src/__init__.py`](Whispering_Woods_Main/src/__init__.py)
- [`Whispering_Woods_Main/src/colors.py`](Whispering_Woods_Main/src/colors.py)
- [`Whispering_Woods_Main/src/data_loader.py`](Whispering_Woods_Main/src/data_loader.py)
- [`Whispering_Woods_Main/src/player.py`](Whispering_Woods_Main/src/player.py)
- [`Whispering_Woods_Main/src/utils.py`](Whispering_Woods_Main/src/utils.py)

**Game Data (JSON):**
- [`Whispering_Woods_Main/data/npcs.json`](Whispering_Woods_Main/data/npcs.json)
- [`Whispering_Woods_Main/data/items.json`](Whispering_Woods_Main/data/items.json)
- [`Whispering_Woods_Main/data/creatures.json`](Whispering_Woods_Main/data/creatures.json)
- [`Whispering_Woods_Main/data/locations.json`](Whispering_Woods_Main/data/locations.json)
- [`Whispering_Woods_Main/data/companions.json`](Whispering_Woods_Main/data/companions.json)
- [`Whispering_Woods_Main/data/quests.json`](Whispering_Woods_Main/data/quests.json)
- [`Whispering_Woods_Main/data/crafting.json`](Whispering_Woods_Main/data/crafting.json)
- [`Whispering_Woods_Main/data/achievements.json`](Whispering_Woods_Main/data/achievements.json)
- [`Whispering_Woods_Main/data/events.json`](Whispering_Woods_Main/data/events.json)
- [`Whispering_Woods_Main/data/lore.json`](Whispering_Woods_Main/data/lore.json)

**Documentation:**
- [`Whispering_Woods_Main/README.md`](Whispering_Woods_Main/README.md) - Game documentation
- [`README.md`](README.md) - Project README
- [`COMPLETION_SUMMARY.md`](COMPLETION_SUMMARY.md) - Full project details

---

## Support

If you encounter issues:

1. Check this guide's **Troubleshooting** section
2. Verify all files are present (see file list above)
3. Ensure Python 3.7+ is installed
4. Create an issue on the repository

---

## Quick Command Reference

```bash
# Navigate to game directory
cd Whispering_Woods_Main

# Launch game
python3 game.py

# Or using launch script
./run_game.sh

# Check files
ls -la

# View data files
ls data/

# Backup save file
cp whispering_woods_save.json backup.json
```

---

**Ready to play?** Run `python3 game.py` and begin your adventure! 🌲✨
