import obspython as S
import time


class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_data = obs_settings
        self.hotkey_id = S.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id

        self.load_hotkey()
        self.register_hotkey()
        self.save_hotkey()

    def register_hotkey(self):
        description = str(self._id)
        self.hotkey_id = S.obs_hotkey_register_frontend(
             str(self._id), description, self.callback
        )
        S.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)

    def load_hotkey(self):
        self.hotkey_saved_key = S.obs_data_get_array(
            self.obs_data,  str(self._id)
        )
        S.obs_data_array_release(self.hotkey_saved_key)

    def save_hotkey(self):
        self.hotkey_saved_key = S.obs_hotkey_save(self.hotkey_id)
        S.obs_data_set_array(
            self.obs_data, str(self._id), self.hotkey_saved_key
        )
        S.obs_data_array_release(self.hotkey_saved_key)

class h:
    htk_copy = None  # this attribute will hold instance of Hotkey
class text:
	txt = ""
class ffloat:
	f = ""

def toggle():
    current_scene = S.obs_scene_from_source(S.obs_frontend_get_current_scene())
    scene_item = S.obs_scene_find_source(current_scene, text_MapImage.txt)
    boolean = not S.obs_sceneitem_visible(scene_item)
    S.obs_sceneitem_set_visible(scene_item, boolean)




def mapkey_callback(pressed):
    if text_RustScene.txt != "" and text_RustScene .txt!= S.obs_source_get_name(S.obs_frontend_get_current_scene()):

        return;
    if pressed:
        toggle()
    else:
        time.sleep(float_delay.f)	
        toggle()



text_MapImage  = text()
text_RustScene = text()

float_delay = ffloat()

hotkey = h()

def script_description():
    return "Adds a hotkey for your Rust game map cover.\n\n\nTutorial: \n\n    rust_map_source_name : is the name of the image you have in your scene to cover the rust map with. \n\n    rust_scene_name : is the scene that you want the hotkey to affect. leave blank if irrelevant\n\n    reveal delay : the amount of time before the map cover disapeears before revealing (seconds).\n\n    - Then go into hotkeys and set the RustMap Push to Hide hotkey to your map key + whatever combinations you might use it in (shift + g).\n\n\n wee wee followw mee knaxelbabyy <3"

def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_text(props, "rust_map_source_name", "rust_map_source_name:", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_text(props, "rust_scene_name", "rust_scene_name:", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_float_slider(props, "rust_map_delay", "reveal delay (.11 std) :", 0,1,.01)

    return props


def script_update(settings):
    _text1 = S.obs_data_get_string(settings, "rust_map_source_name")
    text_MapImage.txt = _text1
    _text1 = S.obs_data_get_string(settings, "rust_scene_name")
    text_RustScene.txt = _text1
    _f = S.obs_data_get_double(settings, "rust_map_delay")
    float_delay.f = _f


def script_load(settings):
    hotkey.htk_copy = Hotkey(mapkey_callback, settings, "RustMap Push to Hide")

    _text1 = S.obs_data_get_string(settings, "rust_map_source_name")
    text_MapImage.txt = _text1
    _text1 = S.obs_data_get_string(settings, "rust_scene_name")
    text_RustScene.txt = _text1
    _f = S.obs_data_get_double(settings, "rust_map_delay")
    float_delay.f = _f


def script_save(settings):
    hotkey.htk_copy.save_hotkey()