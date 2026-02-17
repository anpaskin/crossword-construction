#!/usr/bin/env python3
"""
Crossword Construction CLI Tool
Helps with NYT-style crossword theme creation
"""

import argparse
import sys
from typing import List, Tuple, Dict, Any
import urllib.request
import urllib.parse
import urllib.error
import json


class MiniCrosswordHelper:
    """Helper class for mini crossword creation (5x5 grid)"""
    
    # Mini crossword guidelines for 5x5 puzzles
    GRID_SIZE = 5
    MIN_THEME_ENTRIES = 2
    MAX_THEME_ENTRIES = 3
    MIN_ENTRY_LENGTH = 3
    MAX_ENTRY_LENGTH = 5
    TOTAL_WORDS = 10  # Typically 5 across + 5 down
    
    @staticmethod
    def validate_entry_length(entry: str) -> Tuple[bool, str]:
        """Validate if a mini crossword entry has appropriate length"""
        length = len(entry.replace(" ", ""))
        
        if length < MiniCrosswordHelper.MIN_ENTRY_LENGTH:
            return False, f"Entry too short ({length} letters). Mini crossword entries are typically {MiniCrosswordHelper.MIN_ENTRY_LENGTH}-{MiniCrosswordHelper.MAX_ENTRY_LENGTH} letters."
        
        if length > MiniCrosswordHelper.MAX_ENTRY_LENGTH:
            return False, f"Entry too long ({length} letters). Mini crossword entries are typically {MiniCrosswordHelper.MIN_ENTRY_LENGTH}-{MiniCrosswordHelper.MAX_ENTRY_LENGTH} letters."
        
        return True, f"✓ Good length ({length} letters)"
    
    @staticmethod
    def analyze_theme(entries: List[str]) -> Dict[str, Any]:
        """Analyze a set of mini crossword theme entries"""
        results = {
            "entries": [],
            "total_length": 0,
            "entry_count": len(entries),
            "warnings": [],
            "suggestions": []
        }
        
        # Process each entry
        for entry in entries:
            clean_entry = entry.replace(" ", "").upper()
            length = len(clean_entry)
            is_valid, message = MiniCrosswordHelper.validate_entry_length(entry)
            
            results["entries"].append({
                "text": entry,
                "length": length,
                "valid": is_valid,
                "message": message
            })
            results["total_length"] += length
        
        # Check entry count
        if results["entry_count"] < MiniCrosswordHelper.MIN_THEME_ENTRIES:
            results["warnings"].append(
                f"Consider adding more theme entries. Mini crosswords typically have {MiniCrosswordHelper.MIN_THEME_ENTRIES}-{MiniCrosswordHelper.MAX_THEME_ENTRIES} theme entries."
            )
        elif results["entry_count"] > MiniCrosswordHelper.MAX_THEME_ENTRIES:
            results["warnings"].append(
                f"You have many theme entries ({results['entry_count']}). Mini crosswords typically have {MiniCrosswordHelper.MIN_THEME_ENTRIES}-{MiniCrosswordHelper.MAX_THEME_ENTRIES} theme entries."
            )
        
        # Check for paired length symmetry
        lengths = [e["length"] for e in results["entries"]]
        if len(set(lengths)) == 1:
            results["suggestions"].append("✓ All theme entries have the same length - excellent for symmetry!")
        else:
            results["suggestions"].append(
                "⚠️  Note: Theme entries have different lengths. Consider matching lengths for easier symmetric placement."
            )
        
        # Mini-specific suggestions
        results["suggestions"].append(f"💡 Mini crossword grid size: {MiniCrosswordHelper.GRID_SIZE}x{MiniCrosswordHelper.GRID_SIZE}")
        results["suggestions"].append(f"💡 Total words needed: ~{MiniCrosswordHelper.TOTAL_WORDS} (typically 5 across + 5 down)")
        
        return results


class ThemeHelper:
    """Helper class for crossword theme creation following NYT guidelines"""
    
    # NYT guidelines for 15x15 daily puzzles
    MIN_THEME_ENTRIES = 4
    MAX_THEME_ENTRIES = 5
    MIN_ENTRY_LENGTH = 8
    MAX_ENTRY_LENGTH = 15
    
    @staticmethod
    def validate_entry_length(entry: str) -> Tuple[bool, str]:
        """Validate if a theme entry has appropriate length"""
        length = len(entry.replace(" ", ""))
        
        if length < ThemeHelper.MIN_ENTRY_LENGTH:
            return False, f"Entry too short ({length} letters). NYT theme entries are typically {ThemeHelper.MIN_ENTRY_LENGTH}-{ThemeHelper.MAX_ENTRY_LENGTH} letters."
        
        if length > ThemeHelper.MAX_ENTRY_LENGTH:
            return False, f"Entry too long ({length} letters). NYT theme entries are typically {ThemeHelper.MIN_ENTRY_LENGTH}-{ThemeHelper.MAX_ENTRY_LENGTH} letters."
        
        return True, f"✓ Good length ({length} letters)"
    
    @staticmethod
    def analyze_theme(entries: List[str]) -> Dict[str, Any]:
        """Analyze a set of theme entries for NYT compliance"""
        results = {
            "entries": [],
            "total_length": 0,
            "entry_count": len(entries),
            "warnings": [],
            "suggestions": []
        }
        
        # Process each entry
        for entry in entries:
            clean_entry = entry.replace(" ", "").upper()
            length = len(clean_entry)
            is_valid, message = ThemeHelper.validate_entry_length(entry)
            
            results["entries"].append({
                "text": entry,
                "length": length,
                "valid": is_valid,
                "message": message
            })
            results["total_length"] += length
        
        # Check entry count
        if results["entry_count"] < ThemeHelper.MIN_THEME_ENTRIES:
            results["warnings"].append(
                f"Consider adding more theme entries. NYT puzzles typically have {ThemeHelper.MIN_THEME_ENTRIES}-{ThemeHelper.MAX_THEME_ENTRIES} theme entries."
            )
        elif results["entry_count"] > ThemeHelper.MAX_THEME_ENTRIES:
            results["warnings"].append(
                f"You have many theme entries ({results['entry_count']}). NYT puzzles typically have {ThemeHelper.MIN_THEME_ENTRIES}-{ThemeHelper.MAX_THEME_ENTRIES} theme entries."
            )
        
        # Check for paired length symmetry
        lengths = [e["length"] for e in results["entries"]]
        if len(set(lengths)) == 1:
            results["suggestions"].append("✓ All theme entries have the same length - excellent for symmetry!")
        else:
            # Check if entries can be paired by length
            from collections import Counter
            length_counts = Counter(lengths)
            unpaired_lengths = [length for length, count in length_counts.items() if count % 2 != 0]
            
            if unpaired_lengths:
                results["warnings"].append(
                    f"⚠️  Theme entries must be in pairs of equal lengths for symmetry. Unpaired lengths: {sorted(unpaired_lengths)}"
                )
            else:
                results["suggestions"].append(
                    "✓ All theme entries are paired by length - good for symmetric placement!"
                )
        
        return results
    
    @staticmethod
    def suggest_wordplay(base_phrase: str) -> Dict[str, Any]:
        """Get synonyms and related words for a phrase using Datamuse API"""
        results = {
            "synonyms": [],
            "related": [],
            "error": None
        }
        
        try:
            # Clean the phrase and prepare for API call
            clean_phrase = base_phrase.strip().lower()
            
            # Get synonyms using Datamuse API (ml = means like)
            encoded_phrase = urllib.parse.quote(clean_phrase)
            synonym_url = f"https://api.datamuse.com/words?ml={encoded_phrase}&max=15"
            
            with urllib.request.urlopen(synonym_url, timeout=5) as response:
                synonym_data = json.loads(response.read().decode())
                results["synonyms"] = [item.get("word", "") for item in synonym_data[:10] if item.get("word")]
            
            # Get related words (triggers, rhymes, etc.) using rel_trg parameter
            related_url = f"https://api.datamuse.com/words?rel_trg={encoded_phrase}&max=15"
            
            with urllib.request.urlopen(related_url, timeout=5) as response:
                related_data = json.loads(response.read().decode())
                results["related"] = [item.get("word", "") for item in related_data[:10] if item.get("word")]
            
        except urllib.error.URLError as e:
            results["error"] = f"Network error: Unable to fetch synonyms. {str(e)}"
        except Exception as e:
            results["error"] = f"Error fetching synonyms: {str(e)}"
        
        return results


def print_analysis(results: dict, is_mini: bool = False):
    """Pretty print the theme analysis results"""
    print("\n" + "="*60)
    print("MINI CROSSWORD ANALYSIS" if is_mini else "THEME ANALYSIS")
    print("="*60)
    
    print(f"\nTheme Entry Count: {results['entry_count']}")
    print(f"Total Theme Length: {results['total_length']} letters")
    
    print("\nIndividual Entries:")
    print("-" * 60)
    for i, entry in enumerate(results["entries"], 1):
        print(f"{i}. {entry['text']}")
        print(f"   {entry['message']}")
    
    if results["warnings"]:
        print("\n⚠️  WARNINGS:")
        print("-" * 60)
        for warning in results["warnings"]:
            print(f"  • {warning}")
    
    if results["suggestions"]:
        print("\n💡 SUGGESTIONS:")
        print("-" * 60)
        for suggestion in results["suggestions"]:
            print(f"  • {suggestion}")
    
    print("\n" + "="*60)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Crossword Construction CLI - Aid in NYT-style crossword theme creation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze theme entries
  %(prog)s --analyze "PLAY ON WORDS" "WORD PLAY" "PLAYS WELL"
  
  # Analyze mini crossword entries
  %(prog)s --mini "CAT" "DOG" "BAT"
  
  # Get synonyms and related words
  %(prog)s --wordplay "RUNNING LATE"
        """
    )
    
    parser.add_argument(
        "--analyze",
        nargs="+",
        metavar="ENTRY",
        help="Analyze theme entries for NYT compliance (provide multiple entries)"
    )
    
    parser.add_argument(
        "--mini",
        nargs="+",
        metavar="ENTRY",
        help="Analyze theme entries for mini crossword (5x5 grid) (provide multiple entries)"
    )
    
    parser.add_argument(
        "--wordplay",
        metavar="PHRASE",
        help="Get synonyms and related words for a phrase"
    )
    
    parser.add_argument(
        "--guidelines",
        action="store_true",
        help="Display NYT crossword construction guidelines"
    )
    
    args = parser.parse_args()
    
    # Handle commands
    if args.guidelines:
        print("\n" + "="*60)
        print("NYT CROSSWORD CONSTRUCTION GUIDELINES")
        print("="*60)
        print("\nFor 15x15 Daily Puzzles:")
        print(f"  • Theme entries: {ThemeHelper.MIN_THEME_ENTRIES}-{ThemeHelper.MAX_THEME_ENTRIES} entries")
        print(f"  • Entry length: {ThemeHelper.MIN_ENTRY_LENGTH}-{ThemeHelper.MAX_ENTRY_LENGTH} letters each")
        print("  • All entries should follow the same theme logic")
        print("  • Entries should be symmetrically placed")
        print("  • Prefer equal-length entries for symmetry")
        print("  • Minimum 3 letters per word")
        print("  • Maximum 78 words for themed puzzles")
        print("  • All white squares must be 'checked' (crossed)")
        print("\nFor 21x21 Sunday Puzzles:")
        print("  • Larger grid allows for more theme entries")
        print("  • Similar proportional guidelines apply")
        print("\nFor 5x5 Mini Crosswords:")
        print(f"  • Theme entries: {MiniCrosswordHelper.MIN_THEME_ENTRIES}-{MiniCrosswordHelper.MAX_THEME_ENTRIES} entries")
        print(f"  • Entry length: {MiniCrosswordHelper.MIN_ENTRY_LENGTH}-{MiniCrosswordHelper.MAX_ENTRY_LENGTH} letters each")
        print(f"  • Grid size: {MiniCrosswordHelper.GRID_SIZE}x{MiniCrosswordHelper.GRID_SIZE}")
        print(f"  • Total words: ~{MiniCrosswordHelper.TOTAL_WORDS} (5 across + 5 down)")
        print("  • Quick to solve, perfect for daily practice")
        print("="*60 + "\n")
    
    elif args.mini:
        results = MiniCrosswordHelper.analyze_theme(args.mini)
        print_analysis(results, is_mini=True)
    
    elif args.analyze:
        results = ThemeHelper.analyze_theme(args.analyze)
        print_analysis(results)
    
    elif args.wordplay:
        results = ThemeHelper.suggest_wordplay(args.wordplay)
        
        print(f"\nSynonyms and related words for: {args.wordplay}")
        print("=" * 60)
        
        if results["error"]:
            print(f"\n⚠️  {results['error']}")
            print("\nPlease check your internet connection and try again.")
        else:
            if results["synonyms"]:
                print("\n📚 SYNONYMS (similar meanings):")
                print("-" * 60)
                for i, word in enumerate(results["synonyms"], 1):
                    print(f"  {i:2d}. {word}")
            else:
                print("\n📚 SYNONYMS: No synonyms found.")
            
            if results["related"]:
                print("\n🔗 RELATED WORDS (associated concepts):")
                print("-" * 60)
                for i, word in enumerate(results["related"], 1):
                    print(f"  {i:2d}. {word}")
            else:
                print("\n🔗 RELATED WORDS: No related words found.")
        
        print()

    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
