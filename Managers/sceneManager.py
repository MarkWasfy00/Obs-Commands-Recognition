from obsws_python import ReqClient
from typing import List

class SceneManager:
    def __init__(self, client: ReqClient):
        self.client = client

    def get_scene_list(self) -> List:
        """Get the list of scenes in OBS."""
        object = self.client.get_scene_list()
        return object.scenes
    
    def set_current_scene(self, scene_name: str) -> None:
        """Set the current scene in OBS."""
        self.client.set_current_program_scene(scene_name)
