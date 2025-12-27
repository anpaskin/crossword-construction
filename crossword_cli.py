#!/usr/bin/env python3
"""
Crossword Construction CLI Tool
Helps with NYT-style crossword theme creation
"""

import argparse
import sys
from typing import List, Tuple
import urllib.request
import urllib.parse
import urllib.error
import json


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
    def suggest_wordplay(base_phrase: str) -> dict:
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
    
    @staticmethod
    def generate_theme_entries(base_entry: str, max_results: int = 10) -> dict:
        """Generate additional theme entries of equal length using related words and phrases"""
        # Clean the phrase and calculate target length once
        clean_phrase = base_entry.strip().lower()
        clean_no_spaces = clean_phrase.replace(" ", "")
        target_length = len(clean_no_spaces)
        
        results = {
            "base_entry": base_entry.upper(),
            "target_length": target_length,
            "generated_entries": [],
            "error": None
        }
        
        try:
            # Extract key words from the base entry for searching
            words = clean_phrase.split()
            
            all_candidates = []
            
            # For each word in the phrase, find related words and build combinations
            for word in words:
                encoded_word = urllib.parse.quote(word)
                
                # Get synonyms (ml = means like)
                synonym_url = f"https://api.datamuse.com/words?ml={encoded_word}&max=30"
                with urllib.request.urlopen(synonym_url, timeout=5) as response:
                    synonym_data = json.loads(response.read().decode())
                    for item in synonym_data:
                        word_value = item.get("word")
                        if word_value:
                            all_candidates.append(word_value)
                
                # Get related words (rel_trg = triggers)
                related_url = f"https://api.datamuse.com/words?rel_trg={encoded_word}&max=30"
                with urllib.request.urlopen(related_url, timeout=5) as response:
                    related_data = json.loads(response.read().decode())
                    for item in related_data:
                        word_value = item.get("word")
                        if word_value:
                            all_candidates.append(word_value)
            
            # Also try to get phrases that are similar to the full entry
            encoded_phrase = urllib.parse.quote(clean_phrase)
            
            # Try to get topics/related concepts for multi-word phrases
            topic_url = f"https://api.datamuse.com/words?ml={encoded_phrase}&max=50"
            with urllib.request.urlopen(topic_url, timeout=5) as response:
                topic_data = json.loads(response.read().decode())
                for item in topic_data:
                    word_value = item.get("word")
                    if word_value:
                        all_candidates.append(word_value)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_candidates = []
            for candidate in all_candidates:
                if candidate.lower() not in seen:
                    seen.add(candidate.lower())
                    unique_candidates.append(candidate)
            
            # Filter candidates by length and format them
            matching_entries = []
            for candidate in unique_candidates:
                # Check if length matches target (excluding spaces)
                formatted = candidate.upper().replace(" ", "")
                if len(formatted) == target_length:
                    # Preserve original spacing if present, otherwise use no spaces
                    display_candidate = candidate.upper()
                    
                    if display_candidate not in matching_entries:
                        matching_entries.append(display_candidate)
                    
                    if len(matching_entries) >= max_results:
                        break
            
            results["generated_entries"] = matching_entries
            
        except urllib.error.URLError as e:
            results["error"] = f"Network error: Unable to generate theme entries. {str(e)}"
        except Exception as e:
            results["error"] = f"Error generating theme entries: {str(e)}"
        
        return results


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
  
  # Get synonyms and related words
  %(prog)s --wordplay "RUNNING LATE"
  
  # Generate equal-length theme entries
  %(prog)s --generate-theme "BREAK THE ICE"
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
        help="Get synonyms and related words for a phrase"
    )
    
    parser.add_argument(
        "--generate-theme",
        metavar="ENTRY",
        help="Generate additional equal-length theme entries based on related words and phrases"
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
    
    elif args.generate_theme:
        results = ThemeHelper.generate_theme_entries(args.generate_theme)
        
        print(f"\n{'='*60}")
        print("THEME ENTRY GENERATOR")
        print(f"{'='*60}")
        print(f"\nBase Entry: {results['base_entry']}")
        print(f"Target Length: {results['target_length']} letters")
        
        if results["error"]:
            print(f"\n⚠️  {results['error']}")
            print("\nPlease check your internet connection and try again.")
        else:
            if results["generated_entries"]:
                print(f"\n✨ SUGGESTED THEME ENTRIES (equal length - {results['target_length']} letters):")
                print("-" * 60)
                for i, entry in enumerate(results["generated_entries"], 1):
                    # Show the entry with length verification
                    entry_length = len(entry.replace(" ", ""))
                    print(f"  {i:2d}. {entry} ({entry_length} letters)")
                
                print(f"\n💡 TIP: These entries all have {results['target_length']} letters (excluding spaces),")
                print("   making them perfect for symmetric crossword placement!")
            else:
                print(f"\n⚠️  No matching entries found with {results['target_length']} letters.")
                print("   Try a different base entry or length.")
        
        print(f"{'='*60}\n")

    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
