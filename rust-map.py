import obspython as S
import time

class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_settings = obs_settings
        self.hotkey_id = S.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id
        self.load()

    def load(self):
        self.hotkey_saved_key = S.obs_data_get_array(self.obs_settings,  str(self._id))
        S.obs_data_array_release(self.hotkey_saved_key)
        self.hotkey_id = S.obs_hotkey_register_frontend(str(self._id), str(self._id), self.callback)
        S.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)
        self.save()

    def save(self):
        self.hotkey_saved_key = S.obs_hotkey_save(self.hotkey_id)
        S.obs_data_set_array(self.obs_settings, str(self._id), self.hotkey_saved_key)
        S.obs_data_array_release(self.hotkey_saved_key)

def mapkey_callback(pressed):
    obs_source = S.obs_frontend_get_current_scene()
    if data.scene != "" and data.scene != S.obs_source_get_name(obs_source):
        S.obs_source_release(obs_source)
        return
    S.obs_source_release(obs_source)
    #needs a semaphore / lock for spamming
    if pressed:
        toggle(True)
    else:  
        time.sleep(data.delay)
        toggle(False)

def toggle(boolean):
    obs_source = S.obs_frontend_get_current_scene()
    current_scene = S.obs_scene_from_source(obs_source)
    scene_item = S.obs_scene_find_source(current_scene, data.image)
    S.obs_sceneitem_set_visible(scene_item, boolean)
    S.obs_source_release(obs_source)

def script_description():
    return "Adds a hotkey for your Rust game map cover.\n\n\nTutorial: \n\n    rust_map_source_name : is the name of the image you have in your scene to cover the rust map with. \n\n    rust_scene_name : is the scene that you want the hotkey to affect. leave blank if irrelevant\n\n    reveal delay : the amount of time before the map cover disapeears before revealing (seconds).\n\n    - Then go into hotkeys and set the RustMap Push to Hide hotkey to your map key + whatever combinations you might use it in (shift + g).\n\n\n wee wee followw mee knaxelbabyy <3"

def script_properties():
    properties = S.obs_properties_create()
    S.obs_properties_add_text(properties, "rust_map_source_name", "rust_map_source_name:", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_text(properties, "rust_scene_name", "rust_scene_name:", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_float_slider(properties, "rust_map_delay", "reveal delay (.11 std) :", 0,1,.01)
    return properties

def script_update(settings):
    data.image = S.obs_data_get_string(settings, "rust_map_source_name")
    data.scene = S.obs_data_get_string(settings, "rust_scene_name")
    data.delay = S.obs_data_get_double(settings, "rust_map_delay")

def script_load(settings):
    data.hotkey = Hotkey(mapkey_callback, settings, "RustMap Push to Hide")
    data.image = S.obs_data_get_string(settings, "rust_map_source_name")
    data.scene = S.obs_data_get_string(settings, "rust_scene_name")
    data.delay = S.obs_data_get_double(settings, "rust_map_delay")

def script_save(settings):
    data.hotkey.save()

class Data:
    image = ""
    scene = ""
    delay = 0.0
    hotkey = None 

data = Data()