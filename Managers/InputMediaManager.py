from obsws_python import ReqClient


class InputMediaManager:
    def __init__(self, client: ReqClient):
        self.client = client

        # change it based on os and obs version
        self.__text_kind = "text_ft2_source_v2"
        self.__video_kind = "ffmpeg_source"
        self.__image_kind = "image_source"

    def create_text_input(self, scene_name: str, item_name: str, text: str) -> None:
        """Create a text input."""
        self.client.create_input(scene_name, item_name, self.__text_kind, {"text": text}, True)

    def set_text_input_text(self, input_name: str, text: str, overlay: bool = True) -> None:
        """Set the text of a text input."""
        text_inputs = self.client.get_input_kind_list(self.__text_kind).input_kinds
        """ check if the input name is in the list of text inputs to prevent errors"""
        for text_input in text_inputs:
            if text_input["inputName"] == input_name:
                self.client.set_input_settings(text_input["inputName"], {"text": text}, overlay)
                return
        raise Exception(f"Input {input_name} not found")

    def change_text_input_text(self, scene_name: str, item_name: str, text: str) -> None:
        try:
            self.set_text_input_text(item_name, text)
        except Exception as e:
            self.create_text_input(scene_name, item_name, text)

    # Image Inputs
    def create_image_input(self, scene_name: str, item_name: str, path: str) -> None:
        """Create an image input."""
        self.client.create_input(scene_name, item_name, self.__image_kind, {"file": path}, True)
   
    def set_image_settings(self, input_name: str, path: str, overlay: bool = True) -> None:
        """Set the settings of an image input."""
        self.client.set_input_settings(input_name, {"file": path}, overlay)

    # Video Inputs
    def create_video_input(self, scene_name: str, item_name: str, path: str) -> None:
        """Create a video input."""
        self.client.create_input(scene_name, item_name, self.__video_kind, {"local_file": path}, True)

    def set_video_input_settings(self, input_name: str, file: str, looping: bool = False, overlay: bool = True) -> None:
        """Set the settings of a video input."""
        video_inputs = self.client.get_input_kind_list(self.__video_kind).input_kinds
        for video_input in video_inputs:
            if video_input["inputName"] == input_name:
                self.client.set_input_settings(video_input["inputName"], {"local_file": file, "looping": looping}, overlay)
                return
        raise Exception(f"Input {input_name} not found")

    def change_video_input_file(self,  scene_name: str, input_name: str, file: str, overlay: bool = True) -> None:
        """Change the file of a video input."""
        try:
            self.set_video_input_settings(input_name, file, overlay)
        except Exception as e:
            self.create_video_input(scene_name, input_name, file)

