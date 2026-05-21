import json
import sys
import click
import os


SYSTEM_DIR = click.get_app_dir("ozpasslord")
SYSTEM_CONFIG_FILE = os.path.join(SYSTEM_DIR, "config.json")
SYSTEM_VAULT_FILE = os.path.join(SYSTEM_DIR, "passlord.vault")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PORTABLE_CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
PORTABLE_VAULT_FILE = os.path.join(BASE_DIR, "passlord.vault")


DEFAULTS_SYSTEM = {
    "vault_path": SYSTEM_VAULT_FILE,
    "session_timeout": 300,
    "clipboard_timeout": 30,
    "editor": "vim",
    "default_password_length": 20
}

DEFAULTS_PORTABLE = {
    "vault_path": PORTABLE_VAULT_FILE,
    "session_timeout": 300,
    "clipboard_timeout": 30,
    "editor": "vim",
    "default_password_length": 20
}



def make_config_file(systemOrPortable):
    if systemOrPortable == "p":
        with open(PORTABLE_CONFIG_FILE, 'w') as file:
            json.dump(DEFAULTS_PORTABLE, file, indent=4)
        return DEFAULTS_PORTABLE
    elif systemOrPortable == "s":
        os.makedirs(SYSTEM_DIR, exist_ok=True)
        with open(SYSTEM_CONFIG_FILE, 'w') as file:
            json.dump(DEFAULTS_SYSTEM, file, indent=4)
        return DEFAULTS_SYSTEM
    else:
        return None




def load_config():
    
    if os.path.exists(PORTABLE_CONFIG_FILE):
        with open(PORTABLE_CONFIG_FILE, 'r') as file:
            user_config = json.load(file)
        
        config = {**DEFAULTS_PORTABLE, **user_config}
        return config
    elif os.path.exists(SYSTEM_CONFIG_FILE):
        with open(SYSTEM_CONFIG_FILE, 'r') as file:
            user_config = json.load(file)
        
        config = {**DEFAULTS_SYSTEM, **user_config}
        return config
    else:
        raise FileNotFoundError(
            "Configuration file not found.\n"
            "Please run 'ozpasslord init' to create a new vault."
        )


def save_config(config_dict):
    if os.path.exists(PORTABLE_CONFIG_FILE):
        target_file = PORTABLE_CONFIG_FILE
    else:
        target_file = SYSTEM_CONFIG_FILE
        os.makedirs(SYSTEM_DIR, exist_ok=True)

    with open(target_file, 'w') as f:
        json.dump(config_dict, f, indent=4)