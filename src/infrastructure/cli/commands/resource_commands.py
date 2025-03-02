from typing import Optional, cast, List
from colorama import Fore, Style
from .base_commands import CommandMixin, BaseCommands
from .interactive import InteractivePrompt
from ....domain.entities.direction import Direction

class ResourceCommands(CommandMixin):
    """Commands for managing and finding resources."""

    def _get_all_resources(self) -> list[str]:
        """Get all unique resources from all locations."""
        return sorted(set(
            resource
            for location in self.game_map.list_locations().values()
            for resource in location.resources
        ))

    def do_add_resource(self, arg: str) -> None:
        """Add resources to an existing location: add_resource <location> <resource1,resource2,...>
        Example: add_resource Forest mushrooms,herbs"""
        parts = self.require_args(arg, 2, "add_resource <location> <resource1,resource2,...>")
        if not parts:
            return

        location_name = parts[0]
        resources_str = parts[1]
        resources = self.parse_resources(resources_str)
        
        if not resources:
            self.error("No valid resources specified")
            return

        try:
            for resource in resources:
                self.game_map.add_resource_to_location(location_name, resource)
            self.success(f"Resources added to '{location_name}' successfully")
        except ValueError as e:
            self.error(str(e))

    def do_find(self, arg: str) -> None:
        """Find all locations containing a specific resource
        Example: find wood"""
        if not arg:
            resources = self._get_all_resources()
            resource = InteractivePrompt.prompt_selection(
                resources,
                "Find resource",
                error_handler=self.error
            )
            if not resource:
                return
        else:
            resource = arg
            
        locations = self.game_map.resource_management.find_resource(resource)
        if not locations:
            self.warning(f"Resource '{resource}' not found in any location")
            return

        self.success(f"Found '{resource}' in: {', '.join(locations)}")

    def do_nearest(self, arg: str) -> None:
        """Find nearest location with specified resource and path to it
        Example: nearest wood"""
        if not self.require_current_location():
            return

        if not arg:
            resources = self._get_all_resources()
            resource = InteractivePrompt.prompt_selection(
                resources,
                "Find nearest resource",
                error_handler=self.error
            )
            if not resource:
                return
        else:
            resource = arg

        try:
            result = self.game_map.find_path_to_resource(resource)
            if not result:
                self.warning(f"No location found containing '{resource}'")
                return

            location, path = result
            if not path:  # Resource is in current location
                self.success(f"Resource '{resource}' is available at your current location")
                return

            self.info(f"Nearest location with '{resource}': {location}")
            self.success(f"Steps: {len(path)}")
            if path:
                self.info("Directions: " + self.format_directions(path))
        except ValueError as e:
            self.error(str(e))

    def do_list_resources(self, _: str) -> None:
        """List all resources and their locations
        Example: list_resources"""
        resource_locations = {}
        for location in self.game_map.list_locations().values():
            for resource in location.resources:
                if resource not in resource_locations:
                    resource_locations[resource] = []
                resource_locations[resource].append(location.name)

        if not resource_locations:
            self.warning("No resources available")
            return

        self.info("Available Resources:")
        for resource, locations in sorted(resource_locations.items()):
            self.success(f"{resource}: {', '.join(locations)}")
