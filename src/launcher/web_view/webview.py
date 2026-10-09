from pathlib import Path

import pystray
import webview
from PIL import Image


APP_NAME = "Athilia Launcher"
APP_URL = "http://127.0.0.1:8080/?v=2"

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 700
WINDOW_MIN_SIZE = (1000, 650)

ICON_PATH = Path(__file__).parent / "assets" / "athilia.png"

window = None
tray = None

_window_visible = True
_exiting = False


def show_window(icon=None, item=None):
    """Показать окно лаунчера."""
    global _window_visible

    if window is None:
        return

    window.show()
    window.restore()

    _window_visible = True


def hide_window(icon=None, item=None):
    """Скрыть окно лаунчера."""
    global _window_visible

    if window is None:
        return

    window.hide()

    _window_visible = False


def toggle_window(icon=None, item=None):
    """Переключить видимость окна."""
    if _window_visible:
        hide_window()
    else:
        show_window()


def exit_app(icon=None, item=None):
    """Полностью завершить приложение."""
    global _exiting

    _exiting = True

    if window is not None:
        window.destroy()

    if tray is not None:
        tray.stop()


def on_window_closing(*_):
    """
    При закрытии окна просто прячем его в трей.
    Настоящий выход выполняется через пункт 'Выход'.
    """
    if _exiting:
        return True

    hide_window()

    # Отменяем настоящее закрытие окна.
    return False


def create_tray():
    """Создать системную иконку Athilia."""
    global tray

    image = Image.open(ICON_PATH)

    menu = pystray.Menu(
        pystray.MenuItem(
            "Открыть / скрыть",
            toggle_window,
            default=True,
        ),
        pystray.MenuItem(
            "Выход",
            exit_app,
        ),
    )

    tray = pystray.Icon(
        "athilia",
        image,
        APP_NAME,
        menu,
    )

    # ВАЖНО:
    # Не запускаем tray.run() в отдельном потоке.
    # run_detached() интегрирует tray с существующим GUI loop.
    tray.run_detached()


def start_webview(
    url: str = APP_URL,
    width: int = WINDOW_WIDTH,
    height: int = WINDOW_HEIGHT,
):
    global window

    window = webview.create_window(
        title=APP_NAME,
        url=url,
        width=width,
        height=height,
        min_size=WINDOW_MIN_SIZE,
        resizable=False,
        frameless=True,
        easy_drag=True,
    )

    # window.events.closing += on_window_closing

    create_tray()

    webview.start(
        private_mode=False,
        http_server=False,
    )
