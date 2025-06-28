from obsws_python import ReqClient
from typing import List
import time


class InputManager:
    def __init__(self, client: ReqClient):
        self.client = client

     # protected methods
    def _get_scene_item_id(self, scene_name: str, item_name: str) -> int:
        """Get the ID of a scene item."""
        object = self.client.get_scene_item_id(scene_name, item_name)
        return object.scene_item_id

    def get_input_kind_list(self, unversioned: bool = True) -> List:
        """Get the list of input kinds in OBS."""
        object = self.client.get_input_kind_list(unversioned)
        return object.input_kinds

    def get_sources_with_kind_list(self, kind: str) -> List:
        """Get the list of inputs in OBS."""
        object = self.client.get_input_list(kind)
        return object.inputs
    
    def get_scene_item_enabled(self, scene_name: str, sceneItemId: int) -> bool:
        """Get the enabled state of a scene item."""
        object = self.client.get_scene_item_enabled(scene_name, sceneItemId)
        return object.scene_item_enabled
    
    def set_scene_item_enabled(self, scene_name: str, sceneItemId: int, enabled: bool) -> None:
        """Set the enabled state of a scene item."""
        self.client.set_scene_item_enabled(scene_name, sceneItemId, enabled)
    
    def toggle_source_visibility(self, scene_name: str, item_name: str) -> None:
        """Toggle the visibility of a source."""
        source_id = self._get_scene_item_id(scene_name, item_name)
        enabled = self.get_scene_item_enabled(scene_name, source_id)
        self.set_scene_item_enabled(scene_name, source_id, not enabled)

    def set_scene_source_visibility(self, scene_name: str, item_name: str, enabled: bool) -> None:
        """Set the visibility of a source."""
        source_id = self._get_scene_item_id(scene_name, item_name)
        self.set_scene_item_enabled(scene_name, source_id, enabled)

    def restart_scene_source_visibility(self, scene_name: str, item_name: str) -> None:
        """Restart the visibility of a source by toggling it off and on."""
        source_id = self._get_scene_item_id(scene_name, item_name)
        enabled = self.get_scene_item_enabled(scene_name, source_id)
        if enabled:
            self.set_scene_item_enabled(scene_name, source_id, False)
            time.sleep(0.1)
            self.set_scene_item_enabled(scene_name, source_id, True)
