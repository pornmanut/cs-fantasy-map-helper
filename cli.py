#!/usr/bin/env python3
import cmd
import sys
from typing import List, Optional
from main import GameMap, Direction
from colorama import Fore, Style, init as colorama_init

class GameMapCLI(cmd.Cmd):
    intro = f"""
{Fore.CYAN}Welcome to the Card Survival Fantasy Map Helper

Command Categories:
{Fore.GREEN}Navigation Commands:{Style.RESET_ALL}
  goto, look, path, nearest

{Fore.YELLOW}Location Management:{Style.RESET_ALL}
  add_location, add_connection, list_locations

{Fore.GREEN}Resource Management:{Style.RESET_ALL}
  add_resource, find, list_resources

{Fore.YELLOW}Map Management:{Style.RESET_ALL}
  save, load, list_maps

{Fore.GREEN}General:{Style.RESET_ALL}
  help, quit

Type 'help <command>' for detailed information about a command.
{Style.RESET_ALL}"""
    def get_prompt(self) -> str:
        """Generate the prompt string based on current location"""
        if not self.game_map.current_location:
            return f'{Fore.YELLOW}[no location]>{Style.RESET_ALL} '
        return f'{Fore.GREEN}[{self.game_map.current_location}]>{Style.RESET_ALL} '

    def postcmd(self, stop: bool, line: str) -> bool:
        """Update prompt after each command"""
        self.prompt = self.get_prompt()
        return stop

    # Command categories for help
    NAVIGATION_COMMANDS = ["goto", "look", "path", "nearest"]
    LOCATION_COMMANDS = ["add_location", "add_connection", "list_locations"]
    RESOURCE_COMMANDS = ["add_resource", "find", "list_resources"]
    MAP_COMMANDS = ["save", "load", "list_maps"]
    GENERAL_COMMANDS = ["help", "quit"]

    def help_navigation(self):
        """Show help for navigation commands"""
        print(f"\n{Fore.CYAN}Navigation Commands:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}goto <location>{Style.RESET_ALL} - Move to a specific location")
        print(f"{Fore.GREEN}look{Style.RESET_ALL} - Show information about current location")
        print(f"{Fore.GREEN}path <destination>{Style.RESET_ALL} - Find path to target location")
        print(f"{Fore.GREEN}nearest <resource>{Style.RESET_ALL} - Find nearest location with specified resource")

    def help_locations(self):
        """Show help for location management commands"""
        print(f"\n{Fore.CYAN}Location Management Commands:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}add_location <name> [resource1,resource2,...]{Style.RESET_ALL} - Create a new location")
        print(f"{Fore.GREEN}add_connection <from> <to> <direction>{Style.RESET_ALL} - Connect two locations")
        print(f"{Fore.GREEN}list_locations{Style.RESET_ALL} - Show all locations and their details")

    def help_resources(self):
        """Show help for resource management commands"""
        print(f"\n{Fore.CYAN}Resource Management Commands:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}add_resource <location> <resource1,resource2,...>{Style.RESET_ALL} - Add resources to location")
        print(f"{Fore.GREEN}find <resource>{Style.RESET_ALL} - Find all locations with specified resource")
        print(f"{Fore.GREEN}list_resources{Style.RESET_ALL} - Show all resources and their locations")

    def help_maps(self):
        """Show help for map management commands"""
        print(f"\n{Fore.CYAN}Map Management Commands:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}save [filename]{Style.RESET_ALL} - Save current map to file")
        print(f"{Fore.GREEN}load <filename>{Style.RESET_ALL} - Load map from file")
        print(f"{Fore.GREEN}list_maps{Style.RESET_ALL} - Show available map files")

    def help_general(self):
        """Show help for general commands"""
        print(f"\n{Fore.CYAN}General Commands:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}help{Style.RESET_ALL} - Show command categories or help for specific command")
        print(f"{Fore.GREEN}quit{Style.RESET_ALL} - Exit the program")

    def do_help(self, arg: str) -> None:
        """List available commands with "help" or detailed help with "help cmd"."""
        if arg:
            # If help <category> is called, show category help
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
                # Default cmd.Cmd help for specific command
                super().do_help(arg)
        else:
            # Show command categories
            print(f"\n{Fore.CYAN}Command Categories (type 'help <category>' for details):{Style.RESET_ALL}")
            print(f"{Fore.GREEN}navigation{Style.RESET_ALL} - Commands for moving around the map")
            print(f"{Fore.GREEN}locations{Style.RESET_ALL} - Commands for managing locations")
            print(f"{Fore.GREEN}resources{Style.RESET_ALL} - Commands for managing resources")
            print(f"{Fore.GREEN}maps{Style.RESET_ALL} - Commands for saving/loading maps")
            print(f"{Fore.GREEN}general{Style.RESET_ALL} - Basic commands like help and quit")
            print(f"\nOr type 'help <command>' for help on a specific command")

    def __init__(self):
        super().__init__()
        self.game_map = GameMap()
        colorama_init()
        self.prompt = self.get_prompt()
        
        # Show available maps when starting
        self.do_list_maps("")
        print(f"\n{Fore.CYAN}Type 'load <filename>' to load a map, or start creating a new one.{Style.RESET_ALL}\n")

    def do_list_maps(self, arg: str) -> None:
        """List all available map files that can be loaded
        Example: list_maps"""
        import glob
        import os
        
        map_files = glob.glob("*.json")
        if not map_files:
            print(f"{Fore.YELLOW}No map files found in current directory{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}Available map files:{Style.RESET_ALL}")
        for file in map_files:
            # Get file size and last modified time
            stats = os.stat(file)
            size = stats.st_size / 1024  # Convert to KB
            last_modified = stats.st_mtime
            from datetime import datetime
            modified_time = datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{Fore.GREEN}{file}{Style.RESET_ALL} "
                  f"({size:.1f}KB, modified: {modified_time})")

    def do_add_location(self, arg: str) -> None:
        """Add a new location: add_location <name> [resource1,resource2,...]
        Example: add_location Forest wood,berries"""
        args = arg.split()
        if not args:
            print(f"{Fore.RED}Error: Location name required{Style.RESET_ALL}")
            return

        name = args[0]
        resources = args[1].split(',') if len(args) > 1 else []
        
        try:
            self.game_map.add_location(name, resources)
            print(f"{Fore.GREEN}Location '{name}' added successfully{Style.RESET_ALL}")
        except ValueError as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def do_add_connection(self, arg: str) -> None:
        """Add a connection between locations: add_connection <from_loc> <to_loc> <direction>
        Example: add_connection Forest Beach south"""
        args = arg.split()
        if len(args) != 3:
            print(f"{Fore.RED}Error: Required format: add_connection <from_loc> <to_loc> <direction>{Style.RESET_ALL}")
            return

        from_loc, to_loc, direction_str = args
        try:
            direction = Direction(direction_str.lower())
            self.game_map.add_connection(from_loc, to_loc, direction)
            print(f"{Fore.GREEN}Connection added successfully{Style.RESET_ALL}")
        except (ValueError, KeyError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def do_goto(self, arg: str) -> None:
        """Set current location: goto <location_name>
        Example: goto Forest"""
        if not arg:
            print(f"{Fore.RED}Error: Location name required{Style.RESET_ALL}")
            return

        if arg not in self.game_map.locations:
            print(f"{Fore.RED}Error: Location '{arg}' not found{Style.RESET_ALL}")
            return

        self.game_map.current_location = arg
        self.do_look("")

    def do_look(self, arg: str) -> None:
        """Show information about current location
        Example: look"""
        info = self.game_map.get_current_location_info()
        if not info:
            print(f"{Fore.YELLOW}You are not at any location. Use 'goto' to set your location.{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Location: {info['name']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Resources: {', '.join(info['resources']) or 'None'}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Connections:")
        for direction, location in info['connections'].items():
            print(f"  {direction}: {location}{Style.RESET_ALL}")

    def do_find(self, arg: str) -> None:
        """Find all locations containing a specific resource
        Example: find wood"""
        if not arg:
            print(f"{Fore.RED}Error: Resource name required{Style.RESET_ALL}")
            return

        locations = self.game_map.find_resource(arg)
        if not locations:
            print(f"{Fore.YELLOW}Resource '{arg}' not found in any location{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}Found '{arg}' in: {', '.join(locations)}{Style.RESET_ALL}")

    def do_path(self, arg: str) -> None:
        """Find path between current location and target location
        Example: path Mountain"""
        if not arg:
            print(f"{Fore.RED}Error: Target location required{Style.RESET_ALL}")
            return

        if not self.game_map.current_location:
            print(f"{Fore.RED}Error: No current location set. Use 'goto' first.{Style.RESET_ALL}")
            return

        path = self.game_map.find_path(self.game_map.current_location, arg)
        if not path:
            print(f"{Fore.YELLOW}No path found to {arg}{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}Path to {arg}:")
        print(f"Steps: {len(path)}")
        print("Directions: " + " → ".join(d.value for d in path))
        print(Style.RESET_ALL)

    def do_nearest(self, arg: str) -> None:
        """Find nearest location with specified resource and path to it
        Example: nearest wood"""
        if not arg:
            print(f"{Fore.RED}Error: Resource name required{Style.RESET_ALL}")
            return

        if not self.game_map.current_location:
            print(f"{Fore.RED}Error: No current location set. Use 'goto' first.{Style.RESET_ALL}")
            return

        result = self.game_map.find_nearest_resource(arg, self.game_map.current_location)
        if not result:
            print(f"{Fore.YELLOW}No location found containing '{arg}'{Style.RESET_ALL}")
            return

        location, path = result
        print(f"{Fore.GREEN}Nearest location with '{arg}': {location}")
        print(f"Steps: {len(path)}")
        print("Directions: " + " → ".join(d.value for d in path))
        print(Style.RESET_ALL)

    def do_save(self, arg: str) -> None:
        """Save the current map to a file
        Example: save map_data.json"""
        filename = arg or "map_data.json"
        try:
            self.game_map.save_to_file(filename)
            print(f"{Fore.GREEN}Map saved successfully to {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error saving map: {e}{Style.RESET_ALL}")

    def do_load(self, arg: str) -> None:
        """Load a map from a file
        Example: load example_map.json"""
        if not arg:
            print(f"{Fore.RED}Error: Please specify a map file to load{Style.RESET_ALL}")
            self.do_list_maps("")
            return
            
        try:
            self.game_map.load_from_file(arg)
            print(f"{Fore.GREEN}Map loaded successfully from {arg}{Style.RESET_ALL}")
            print("\nCurrent map contents:")
            self.do_list_locations("")
        except Exception as e:
            print(f"{Fore.RED}Error loading map: {e}{Style.RESET_ALL}")
            self.do_list_maps("")

    def do_quit(self, arg: str) -> bool:
        """Quit the program"""
        print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
        return True

    def do_list_locations(self, arg: str) -> None:
        """List all available locations and their resources
        Example: list_locations"""
        if not self.game_map.locations:
            print(f"{Fore.YELLOW}No locations available{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Available Locations:{Style.RESET_ALL}")
        for name, location in self.game_map.locations.items():
            print(f"\n{Fore.GREEN}{name}:")
            print(f"{Fore.YELLOW}Resources: {', '.join(location.resources) or 'None'}")
            print(f"Connections:")
            for direction, target in location.connections.items():
                print(f"  {direction.value}: {target}{Style.RESET_ALL}")

    def do_list_resources(self, arg: str) -> None:
        """List all resources and their locations
        Example: list_resources"""
        if not self.game_map.resource_locations:
            print(f"{Fore.YELLOW}No resources available{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Available Resources:{Style.RESET_ALL}")
        for resource, locations in self.game_map.resource_locations.items():
            print(f"{Fore.GREEN}{resource}: {', '.join(locations)}{Style.RESET_ALL}")

    def do_add_resource(self, arg: str) -> None:
        """Add resources to an existing location: add_resource <location> <resource1,resource2,...>
        Example: add_resource Forest mushrooms,herbs"""
        args = arg.split()
        if len(args) != 2:
            print(f"{Fore.RED}Error: Required format: add_resource <location> <resource1,resource2,...>{Style.RESET_ALL}")
            return

        location_name, resources_str = args
        resources = resources_str.split(',')

        if location_name not in self.game_map.locations:
            print(f"{Fore.RED}Error: Location '{location_name}' not found{Style.RESET_ALL}")
            return

        # Add new resources to the location
        location = self.game_map.locations[location_name]
        for resource in resources:
            if resource not in location.resources:
                location.resources.append(resource)
                self.game_map.resource_locations[resource].append(location_name)

        print(f"{Fore.GREEN}Resources added to '{location_name}' successfully{Style.RESET_ALL}")

    def do_EOF(self, arg: str) -> bool:
        """Exit on Ctrl-D"""
        print()  # For clean newline
        return self.do_quit("")

def main():
    try:
        GameMapCLI().cmdloop()
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt, exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
