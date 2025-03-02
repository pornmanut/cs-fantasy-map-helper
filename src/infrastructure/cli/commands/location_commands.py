from typing import Optional, cast
from colorama import Fore, Style
from .base_commands import CommandMixin, BaseCommands
from ....domain.entities.direction import Direction

class LocationCommands(CommandMixin):
    """Commands for managing locations."""

    def do_add_location(self, arg: str) -> None:
        """Add a new location: add_location <name> [resource1,resource2,...]
        Example: add_location Forest wood,berries"""
        parts = self.require_args(arg, 1, "add_location <name> [resource1,resource2,...]")
        if not parts:
            return

        name = parts[0]
        resources = self.parse_resources(arg[len(name):].strip())
        
        try:
            self.game_map.create_location(name, resources)
            self.success(f"Location '{name}' added successfully")
        except ValueError as e:
            self.error(str(e))

    def do_add_connection(self, arg: str) -> None:
        """Add a connection between locations: add_connection <from_loc> <to_loc> <direction>
        Example: add_connection Forest Beach south"""
        parts = self.require_args(arg, 3, "add_connection <from_loc> <to_loc> <direction>")
        if not parts:
            return

        from_loc, to_loc, direction_str = parts
        try:
            self.game_map.add_connection(from_loc, to_loc, direction_str)
            self.success("Connection added successfully")
        except (ValueError, KeyError) as e:
            self.error(str(e))

    def do_goto(self, arg: str) -> None:
        """Set current location: goto <location_name>
        Example: goto Forest"""
        parts = self.require_args(arg, 1, "goto <location_name>")
        if not parts:
            return

        location_name = parts[0]
        try:
            self.game_map.set_current_location(location_name)
            self.do_look("")
        except ValueError as e:
            self.error(str(e))

    def do_look(self, _: str) -> None:
        """Show information about current location
        Example: look"""
        current = cast(str, self.game_map.get_current_location())
        if not current:
            self.warning("You are not at any location. Use 'goto' to set your location.")
            return
        
        self.show_location_info(current)

    def do_list_locations(self, _: str) -> None:
        """List all available locations and their resources
        Example: list_locations"""
        locations = self.game_map.list_locations()
        if not locations:
            self.warning("No locations available")
            return

        self.info("Available Locations:")
        for name, location in locations.items():
            print(f"\n{Fore.GREEN}{name}:")
            print(f"{Fore.YELLOW}Resources: {', '.join(location.resources) or 'None'}")
            print(f"Connections:")
            for direction, target in location.connections.items():
                print(f"  {direction.value}: {target}{Style.RESET_ALL}")

    def do_path(self, arg: str) -> None:
        """Find path between current location and target location
        Example: path Mountain"""
        if not self.require_current_location():
            return

        parts = self.require_args(arg, 1, "path <destination>")
        if not parts:
            return

        current = cast(str, self.game_map.get_current_location())
        destination = parts[0]
        
        try:
            path = self.game_map.resource_management.find_path(current, destination)
            if not path:
                self.warning(f"No path found to {destination}")
                return

            self.info(f"Path to {destination}:")
            self.success(f"Steps: {len(path)}")
            self.info("Directions: " + self.format_directions(path))
        except ValueError as e:
            self.error(str(e))
