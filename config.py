
class MetaConfig:
    def _configure(self, d: dict, name: str):
        setattr(self, name, d.get(name, getattr(self, name)))

    def _make_config(self, d: dict, name: str, config_class):
        setattr(self, name, config_class(d.get(name)))


class ScreenConfig(MetaConfig):
    hide_cursor = True
    image_path = r"/media/bildschirm"

    def __init__(self, d=dict()):
        self._configure(d, "hide_cursor")
        self._configure(d, "image_path")


class SlideshowConfig(MetaConfig):
    interval = 30
    enable_history = True
    history_length = 256
    fullscreen = True
    topmost = True

    def __init__(self, d=dict()):
        self._configure(d, "interval")
        self._configure(d, "enable_history")
        self._configure(d, "history_length")
        self._configure(d, "fullscreen")
        self._configure(d, "topmost")


class Config(MetaConfig):
    screen: ScreenConfig
    slideshow: SlideshowConfig

    def __init__(self, d=dict()):
        self._make_config(d, "screen", ScreenConfig)
        self._make_config(d, "slideshow", SlideshowConfig)
