from typing import Optional
from colorama import Fore, Style
from .base_commands import CommandMixin, BaseCommands

class MapCommands(CommandMixin):
    """Commands for managing map files."""

    # Required placeholder methods that will be provided by GameCLI
    def do_list_locations(self, _: str) -> None:
        """Placeholder for list_locations command"""
        raise NotImplementedError

    def cmdloop(self) -> bool:
        """Placeholder for cmd.Cmd's cmdloop"""
        raise NotImplementedError
    """Commands for managing map files."""

    def do_save(self, arg: str) -> None:
        """Save the current map to a file
        Example: save map_data.json"""
        filename = arg or "map_data.json"
        try:
            self.game_map.save_map_to_file(filename)
            self.success(f"Map saved successfully to {filename}")
        except Exception as e:
            self.error(f"Failed to save map: {str(e)}")

    def do_load(self, arg: str) -> None:
        """Load a map from a file
        Example: load example_map.json"""
        if not arg:
            self.error("Please specify a map file to load")
            self.do_list_maps("")
            return
            
        try:
            self.game_map.load_map_from_file(arg)
            self.success(f"Map loaded successfully from {arg}")
            print("\nCurrent map contents:")
            self.do_list_locations("")
        except Exception as e:
            self.error(f"Failed to load map: {str(e)}")
            self.do_list_maps("")

    def do_list_maps(self, _: str) -> None:
        """List all available map files that can be loaded
        Example: list_maps"""
        try:
            map_files = self.game_map.get_available_maps()
            if not map_files:
                self.warning("No map files found in current directory")
                return
                
            self.info("Available map files:")
            for filename, size_kb, modified_time in map_files:
                self.success(f"{filename} ({size_kb:.1f}KB, modified: {modified_time})")
        except Exception as e:
            self.error(f"Failed to list maps: {str(e)}")

    def do_quit(self, _: str) -> bool:
        """Quit the program"""
        self.info("Goodbye!")
        return True

    def do_EOF(self, _: str) -> bool:
        """Exit on Ctrl-D"""
        print()  # For clean newline
        return self.do_quit("")

    def do_help(self, arg: str) -> None:
        """Show help about commands"""
        if not arg:
            print(f"\n{Fore.CYAN}Command Categories (type 'help <category>' for details):{Style.RESET_ALL}")
            print(f"{Fore.GREEN}navigation{Style.RESET_ALL} - Commands for moving around the map")
            print(f"{Fore.GREEN}locations{Style.RESET_ALL} - Commands for managing locations")
            print(f"{Fore.GREEN}resources{Style.RESET_ALL} - Commands for managing resources")
            print(f"{Fore.GREEN}maps{Style.RESET_ALL} - Commands for saving/loading maps")
            print(f"{Fore.GREEN}general{Style.RESET_ALL} - Basic commands like help and quit")
            print(f"\nOr type 'help <command>' for help on a specific command")
            return

        if arg == "navigation":
            self.help_navigation()
        elif arg == "locations":
            self.help_locations()
        elif arg == "resources":
            self.help_resources()
        elif arg == "maps":
            self.help_maps()
        elif arg == "general":
            self.help_general()
        else:
            # Command-specific help
            if hasattr(self, f'help_{arg}'):
                getattr(self, f'help_{arg}')()
            elif hasattr(self, f'do_{arg}'):
                doc = getattr(self, f'do_{arg}').__doc__ or ''
                self.info(doc)
            else:
                self.error(f"No help available for '{arg}'")

    def help_navigation(self) -> None:
        self.info("\nNavigation Commands:")
        self.success("goto <location> - Move to a specific location")
        self.success("look          - Show information about current location")
        self.success("path <dest>   - Find path to target location")
        self.success("nearest <res> - Find nearest location with specified resource")

    def help_locations(self) -> None:
        self.info("\nLocation Management Commands:")
        self.success("add_location <name> [res1,res2,...] - Create a new location")
        self.success("add_connection <from> <to> <dir>    - Connect two locations")
        self.success("list_locations                      - Show all locations")

    def help_resources(self) -> None:
        self.info("\nResource Management Commands:")
        self.success("add_resource <loc> <res1,res2,...> - Add resources to location")
        self.success("find <resource>                    - Find resource locations")
        self.success("list_resources                     - Show all resources")

    def help_maps(self) -> None:
        self.info("\nMap Management Commands:")
        self.success("save [filename] - Save current map to file")
        self.success("load <filename> - Load map from file")
        self.success("list_maps       - Show available map files")

    def help_general(self) -> None:
        self.info("\nGeneral Commands:")
        self.success("help        - Show command categories or help for specific command")
        self.success("quit        - Exit the program")
