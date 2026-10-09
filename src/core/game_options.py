import os
import subprocess

from src.settings import MC_DIR, MC_VERSION

import minecraft_launcher_lib
from minecraft_launcher_lib.types import MinecraftOptions


def log(message):
    print(f"[Athilia] {message}")


def check_minecraft():
    """Проверка на наличие Minecraft"""

    log("Проверяем установку Minecraft...")
    log(f"Папка: {MC_DIR}")
    log(f"Версия: {MC_VERSION}")

    if not os.path.exists(MC_DIR):
        log("✗ Папка Minecraft не найдено.")
        return False

    versions = minecraft_launcher_lib.utils.get_installed_versions(MC_DIR)

    if not versions:
        log("✗ Установленных версий Minecraft не найдено.")
        return False

    minecraft_found = False
    fabric_found = False

    log("Найденные версии:")

    for version in versions:
        version_id = version["id"]

        if version_id == MC_VERSION:
            minecraft_found = True
            log(f"  ✓ Minecraft {version_id}")

        elif version_id.startswith("fabric-loader-"):
            fabric_found = True
            log(f"  ✓ {version_id}")

        else:
            log(f"  • {version_id}")

    if not minecraft_found:
        log(f"✗ Minecraft {MC_VERSION} не установлен.")
        return False

    if not fabric_found:
        log("✗ Fabric не установлен.")
        return False

    log("✓ Minecraft + Fabric установлены.")
    return True


def install_minecraft():
    """Устанавливает Minecraft и Fabric"""

    os.makedirs(MC_DIR, exist_ok=True)

    log("=" * 50)
    log("УСТАНОВКА MINECRAFT")
    log("=" * 50)

    # Minecraft
    log(f"[1/2] Установка Minecraft {MC_VERSION}...")
    log(f"Каталог: {MC_DIR}")

    minecraft_launcher_lib.install.install_minecraft_version(
        MC_VERSION,
        MC_DIR
    )

    log("✓ Minecraft успешно установлен.")

    # Fabric
    log(f"[2/2] Установка Fabric для Minecraft {MC_VERSION}...")

    minecraft_launcher_lib.fabric.install_fabric(
        MC_VERSION,
        MC_DIR
    )

    log("✓ Fabric успешно установлен.")

    # Показываем итог
    log("")
    log("Проверяем результат установки...")

    if check_minecraft():
        log("✓ Установка завершена успешно.")
    else:
        log("✗ Установка завершилась, но проверка не пройдена.")
        raise RuntimeError("Minecraft/Fabric не найдены после установки.")


def launch_minecraft(player_nickname):
    """Запускает Minecraft с Fabric."""

    log("=" * 50)
    log("ЗАПУСК MINECRAFT")
    log("=" * 50)

    log(f"Игрок: {player_nickname}")
    log(f"Версия Minecraft: {MC_VERSION}")

    # Проверяем установку перед запуском
    if not check_minecraft():
        raise RuntimeError(
            "Minecraft или Fabric не установлены. "
            "Сначала вызови install_minecraft()."
        )

    # Ищем Fabric
    versions = minecraft_launcher_lib.utils.get_installed_versions(MC_DIR)

    fabric_version = None

    for version in versions:
        if version["id"].startswith("fabric-loader-"):
            fabric_version = version["id"]
            break

    if fabric_version is None:
        raise RuntimeError("Fabric не найден!")

    log(f"Fabric: {fabric_version}")

    # Настройки Minecraft
    options: MinecraftOptions = {
        "username": player_nickname,
        "uuid": "00000000-0000-0000-0000-000000000001",
        "token": "0",

        "server": "athilia.duckdns.org",
        "port": "25565",

        "quickPlayMultiplayer": "athilia.duckdns.org:25565",
    }

    log("Формируем команду запуска...")

    command = minecraft_launcher_lib.command.get_minecraft_command(
        fabric_version,
        MC_DIR,
        options
    )

    log("Команда сформирована.")
    log("")
    log("Команда запуска:")
    print(" ".join(command))

    log("")
    log("Запускаем Minecraft...")

    process = subprocess.Popen(
        command,
        cwd=MC_DIR
    )

    log(f"✓ Minecraft запущен. PID: {process.pid}")
