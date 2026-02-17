# Crossword Construction CLI

A simple command-line tool to aid in crossword construction, following New York Times crossword construction guidelines. This tool helps with theme creation, validation, and wordplay suggestions.

## About

- **Author**: anpaskin
- **Date of Birth**: 3/14/1998
- **Favorite Color**: green

## Features

- **Theme Analysis**: Validate theme entries against NYT guidelines (letter counts)
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

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
