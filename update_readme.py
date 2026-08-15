import os
import json
import shutil
from datetime import datetime


def load_config():
    with open("configuration.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_current_topic(config):
    today = datetime.now().date()

    zeitraeume = config.get("zeitraeume", [])
    for entry in zeitraeume:
        if "from" not in entry or "to" not in entry:
            continue

        start = datetime.strptime(entry["from"], "%Y-%m-%d").date()
        end = datetime.strptime(entry["to"], "%Y-%m-%d").date()

        if start <= today <= end:
            print(f"Passenden Zeitraum gefunden: {entry['title']}")
            return entry

    # Fallback: Default-Hintergrund wählen
    print("Kein aktueller Zeitraum matched. Verwende Fallback (default).")
    return config.get("default")


def update_readme(topic_path, topic_title):
    description_path = os.path.join(topic_path, "description.txt")
    description = ""
    if os.path.exists(description_path):
        with open(description_path, "r", encoding="utf-8") as description_file:
            description = description_file.read()

    # Bilder im Ordner finden (jpg, jpeg, png)
    valid_extensions = (".jpg", ".jpeg", ".png")
    images = sorted([directory_file for directory_file in os.listdir(topic_path) if directory_file.lower().endswith(valid_extensions)])

    # Akzentfarbe lesen
    accent_color_path = os.path.join(topic_path, "accent-color.txt")
    accent_color = None

    if os.path.exists(accent_color_path):
        with open(accent_color_path, "r", encoding="utf-8") as accent_file:
            accent_color = accent_file.read().strip()

    # Neues README generieren
    readme_content = "# Dynamische Hintergründe\n\n"
    if accent_color:
        readme_content += f"## Aktuelles Thema: ![{accent_color}](https://placehold.co/15x15/{accent_color}/{accent_color}.png) {topic_title}\n\n"
    else:
        readme_content += f"## Aktuelles Thema: {topic_title}\n\n"
    if description:
        readme_content += f"> {description}\n\n"

    readme_content += "### Bilder in dieser Periode:\n"
    for img in images:
        img_markdown_path = os.path.join(topic_path, img).replace("\\", "/")
        readme_content += f"![{img}]({img_markdown_path})\n"

    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(readme_content)
    print("README.md erfolgreich aktualisiert.")


def prepare_assets_for_configs(topic_path):
    target_temp_dir = "temp_assets_export"
    if os.path.exists(target_temp_dir):
        shutil.rmtree(target_temp_dir)

    shutil.copytree(topic_path, target_temp_dir)
    print(f"Assets aus '{topic_path}' für den Export vorbereitet.")


def main():
    config = load_config()
    current_topic = get_current_topic(config)

    if not current_topic:
        print("Kein passendes Thema für das aktuelle Datum gefunden.")
        return

    print(f"Aktuelles Thema erkannt: {current_topic['title']} ({current_topic['path']})")

    update_readme(current_topic["path"], current_topic["title"])

    prepare_assets_for_configs(current_topic["path"])


if __name__ == "__main__":
    main()