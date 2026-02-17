# Crossword Construction CLI

A simple command-line tool to aid in crossword construction, following New York Times crossword construction guidelines. This tool helps with theme creation, validation, and wordplay suggestions.

## Features

- **Theme Analysis**: Validate theme entries against NYT guidelines (letter counts)
- **Mini Crossword**: Create and validate entries for 5x5 mini crossword puzzles
- **Synonyms and Related Words**: Get synonyms and related words for phrases
- **Guidelines Reference**: Quick access to NYT construction guidelines

## Installation

### Requirements
- Python 3.6 or higher
- Works on Mac, Linux, and Windows

### Setup

1. Clone this repository:
```bash
git clone https://github.com/anpaskin/crossword-construction.git
cd crossword-construction
```

2. Make the script executable (Mac/Linux):
```bash
chmod +x crossword_cli.py
```

## Usage

### Show Guidelines
```bash
python3 crossword_cli.py --guidelines
```

### Analyze Theme Entries
Provide multiple theme entries to analyze them against NYT guidelines:
```bash
python3 crossword_cli.py --analyze "PLAY ON WORDS" "WORD PLAY" "PLAYING AROUND" "DOUBLE PLAY"
```

### Analyze Mini Crossword Entries
Create and validate entries for 5x5 mini crossword puzzles:
```bash
python3 crossword_cli.py --mini "CAT" "DOG" "BAT"
```

### Get Synonyms and Related Words
Get synonyms and related words for a phrase to help with crossword theme creation:
```bash
python3 crossword_cli.py --wordplay "RUNNING LATE"
```

## NYT Guidelines Summary

For 15x15 daily puzzles:
- **Theme entries**: 4-5 entries
- **Entry length**: 8-15 letters each
- **Symmetry**: Entries should be symmetrically placed
- **Consistency**: All entries should follow the same theme logic
- **Minimum word length**: 3 letters

For 5x5 mini crosswords:
- **Theme entries**: 2-3 entries
- **Entry length**: 3-5 letters each
- **Grid size**: 5x5
- **Total words**: ~10 (typically 5 across + 5 down)
- **Quick to solve**: Perfect for daily practice

## Examples

### Example: Analyzing a theme
```bash
$ python3 crossword_cli.py --analyze "BREAK THE ICE" "BREAK A LEG" "BREAK THE BANK" "BREAK IT DOWN"

============================================================
THEME ANALYSIS
============================================================

Theme Entry Count: 4
Total Theme Length: 43 letters

Individual Entries:
------------------------------------------------------------
1. BREAK THE ICE
   ✓ Good length (11 letters)
2. BREAK A LEG
   ✓ Good length (9 letters)
3. BREAK THE BANK
   ✓ Good length (12 letters)
4. BREAK IT DOWN
   ✓ Good length (11 letters)

💡 SUGGESTIONS:
------------------------------------------------------------
  • Note: Theme entries have different lengths. Consider matching lengths for easier symmetric placement.

============================================================
```

### Example: Analyzing a mini crossword
```bash
$ python3 crossword_cli.py --mini "CAT" "DOG" "BAT"

============================================================
MINI CROSSWORD ANALYSIS
============================================================

Theme Entry Count: 3
Total Theme Length: 9 letters

Individual Entries:
------------------------------------------------------------
1. CAT
   ✓ Good length (3 letters)
2. DOG
   ✓ Good length (3 letters)
3. BAT
   ✓ Good length (3 letters)

💡 SUGGESTIONS:
------------------------------------------------------------
  • ✓ All theme entries have the same length - excellent for symmetry!
  • 💡 Mini crossword grid size: 5x5
  • 💡 Total words needed: ~10 (typically 5 across + 5 down)

============================================================
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
