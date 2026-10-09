import os

from src.settings import MC_DIR, MC_VERSION


def log(message):
    print(f"[Athilia] {message}")


def is_minecraft_install():
    """Проверяет наличие папки Minecraft."""

    log("Проверяем установку Minecraft...")
    log(f"Папка: {MC_DIR}")
    log(f"Версия: {MC_VERSION}")

    if not os.path.isdir(MC_DIR):
        log("✗ Папка Minecraft не существует.")
        return False

    log("✓ Папка Minecraft найдена.")
    return True
