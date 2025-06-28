import obsws_python as obs
import time
import pathlib
from Managers.InputManager import InputManager
from Managers.sceneManager import SceneManager
from Managers.InputMediaManager import InputMediaManager

# OBS API Wrapper
class OBSClient:
    def __init__(self, host='localhost', port=4444, password="password"):
        self.client = obs.ReqClient(host=host, port=port, password=password)
        
        self.screen_width = 1920
        self.screen_height = 1080

        self.scene = SceneManager(self.client)
        self.input = InputManager(self.client)
        self.input_media = InputMediaManager(self.client)

        self.show_loading_screen(5)

    def show_loading_screen(self, loading_time: int = 3, file: str = "thumbnail.png", audio_file: str = "loading.mp3") -> None:
        """Set the loading screen."""
        print("Initializing loading screen...")
        self.client.create_scene("OBS Loading Screen")
        self.input_media.create_image_input("OBS Loading Screen", "Loading Screen", f"{pathlib.Path(__file__).parent}/static/{file}")
        self.input_media.create_video_input("OBS Loading Screen", "Loading Audio", f"{pathlib.Path(__file__).parent}/static/{audio_file}")
        self.client.set_input_audio_monitor_type("Loading Audio", "OBS_MONITORING_TYPE_MONITOR_AND_OUTPUT")
        self.scene.set_current_scene("OBS Loading Screen")
        item_input_id = self.input._get_scene_item_id("OBS Loading Screen", "Loading Screen")
        self.client.set_scene_item_transform("OBS Loading Screen", item_input_id, {"boundsWidth": self.screen_width, "boundsHeight": self.screen_height, "boundsType": "OBS_BOUNDS_STRETCH"})
        self.client.set_scene_item_locked("OBS Loading Screen", item_input_id, True)
        time.sleep(loading_time)
        print("Starting the script...")
        self.client.remove_scene("OBS Loading Screen")


if __name__ == "__main__":
    obs = OBSClient()
    
    