#!/usr/bin/env python3
"""
Crossword Construction CLI Tool
Helps with NYT-style crossword theme creation
"""

import argparse
import sys
from typing import List, Tuple


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
    def analyze_theme(entries: List[str]) -> dict:
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
    def suggest_wordplay(base_phrase: str) -> List[str]:
        """Suggest potential wordplay transformations"""
        suggestions = []
        
        # Common wordplay patterns
        suggestions.append(f"Add a pun prefix/suffix (e.g., 'NOT {base_phrase}' or '{base_phrase} TOO')")
        suggestions.append(f"Replace words with homophones")
        suggestions.append(f"Replace words with rhyming words")
        suggestions.append(f"Add/remove a letter for a twist")
        suggestions.append(f"Combine with another phrase for double meaning")
        
        return suggestions


def print_analysis(results: dict):
    """Pretty print the theme analysis results"""
    print("\n" + "="*60)
    print("THEME ANALYSIS")
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
  
  # Get wordplay suggestions
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
        "--wordplay",
        metavar="PHRASE",
        help="Get wordplay suggestions for a phrase"
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
        print("="*60 + "\n")
    
    elif args.analyze:
        results = ThemeHelper.analyze_theme(args.analyze)
        print_analysis(results)
    
    elif args.wordplay:
        suggestions = ThemeHelper.suggest_wordplay(args.wordplay)
        print(f"\nWordplay suggestions for: {args.wordplay}")
        print("-" * 60)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
        print()
    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
