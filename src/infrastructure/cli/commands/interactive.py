"""Interactive prompting utilities for CLI commands."""
from typing import Optional, TypeVar, Sequence, Any, Callable
from difflib import get_close_matches
from colorama import Fore, Style

T = TypeVar('T')

class InteractivePrompt:
    """Utility class for interactive command prompts."""

    @staticmethod
    def format_options(items: Sequence[Any], formatter: Optional[Callable[[Any], str]] = None) -> str:
        """Format a list of items with numbers."""
        if not formatter:
            formatter = str
        return "\n".join(f"{i+1}. {formatter(item)}" for i, item in enumerate(items))

    @staticmethod
    def get_close_matches(word: str, possibilities: list[str], n: int = 3, cutoff: float = 0.6) -> list[str]:
        """Get list of close matches for a word."""
        return get_close_matches(word.lower(), [p.lower() for p in possibilities], n=n, cutoff=cutoff)

    @staticmethod
    def prompt_selection(
        items: Sequence[T],
        prompt: str,
        formatter: Optional[Callable[[T], str]] = None,
        error_handler: Optional[Callable[[str], None]] = None
    ) -> Optional[T]:
        """Prompt user to select from a list of items."""
        if not items:
            if error_handler:
                error_handler("No items available")
            return None

        if formatter is None:
            formatter = str

        # Show available options
        print(f"\n{Fore.CYAN}Available options:{Style.RESET_ALL}")
        for i, item in enumerate(items):
            print(f"{Fore.GREEN}{i+1}. {formatter(item)}{Style.RESET_ALL}")

        while True:
            try:
                choice = input(f"\n{prompt} (Enter number, name, or press Enter to cancel): ").strip()
                
                if not choice:  # User pressed Enter without input
                    return None

                # Try as number first
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(items):
                        return items[index]
                    raise ValueError("Invalid number")
                except ValueError:
                    # Try as name
                    lower_choice = choice.lower()
                    lower_names = [formatter(item).lower() for item in items]
                    
                    # Exact match
                    if lower_choice in lower_names:
                        return items[lower_names.index(lower_choice)]
                    
                    # Close matches
                    close_matches = get_close_matches(lower_choice, lower_names, n=3, cutoff=0.6)
                    if close_matches:
                        print(f"\n{Fore.YELLOW}Did you mean:{Style.RESET_ALL}")
                        for i, match in enumerate(close_matches):
                            print(f"{Fore.GREEN}{i+1}. {match}{Style.RESET_ALL}")
                        
                        sub_choice = input("\nEnter number or press Enter to try again: ").strip()
                        if sub_choice.isdigit():
                            index = int(sub_choice) - 1
                            if 0 <= index < len(close_matches):
                                match_index = lower_names.index(close_matches[index])
                                return items[match_index]

                if error_handler:
                    error_handler(f"Invalid selection: {choice}")
                else:
                    print(f"{Fore.RED}Invalid selection: {choice}{Style.RESET_ALL}")

            except KeyboardInterrupt:
                print("\nOperation cancelled")
                return None
            except EOFError:
                return None
