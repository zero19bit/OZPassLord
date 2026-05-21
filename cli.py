
from datetime import datetime
import os
import json
import click
import pyperclip
from threading import Timer
from vault import save_vault, load_vault
from generator import passGenerator
from config import make_config_file, load_config, save_config
from io_handler import detect_format, export_to_csv, export_to_json, import_from_csv, import_from_json


def get_vault_path():
    try:
        config = load_config()
        return config["vault_path"]
    except FileNotFoundError:
        return None

def get_clipboard_timeout():
    try:
        config = load_config()
        return config.get("clipboard_timeout", 30)
    except FileNotFoundError:
        return 30

def clear_clipboard():
    pyperclip.copy("")
    click.echo("Clipboard cleared.")

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """A simple password manager CLI."""
    pass

@cli.command()
def init():
    """Initialize the storage file."""
    click.echo("""
    Hello
    wellcome to OZ PassLord
    Enter Master Password to start""")

    while True:
        masterPassword1 = click.prompt("password", hide_input=True)
        masterPassword2 = click.prompt("Retype password", hide_input=True)

        if masterPassword1 == masterPassword2:
            masterPassword = masterPassword1
            break

        click.echo("❌ Passwords do not match. Try again.\n")

    mode = click.prompt(
        "Choose storage mode:\n"
        " [P]ortable - config & vault alongside program\n"
        " [S]ystem   - config & vault in user directory\n"
        "Enter choice (P/S)",
        type=click.Choice(['p', 's'], case_sensitive=False),
        show_choices=False
    ).lower()

    defaults = make_config_file(mode)
    if defaults is None:
        click.echo("❌ Failed to create configuration.")
        return

    vault_path = get_vault_path()
    if vault_path is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    if os.path.exists(vault_path):
        click.echo("⚠️  A vault already exists at this location.")
        click.echo("   If you continue, all existing passwords will be PERMANENTLY DELETED.")
        if not click.confirm("Are you sure you want to overwrite the existing vault?"):
            click.echo("❌ Initialization cancelled.")
            return

    try:
        save_vault([], masterPassword, vault_path)
        click.echo(f"\n✅ Vault created successfully at `{vault_path}`.")
        click.echo("⚠️  Remember your master password! It cannot be recovered.")
    except Exception as e:
        click.echo(f"\n❌ Failed to create vault: {e}")
        raise SystemExit(1)



@cli.command()
@click.option("--title", required=True, help="Title of the entry")
@click.option("--username", required=True, help="Username for this entry")
@click.option("--password", default=None, help="Password for this entry")
@click.option("--url", default=None , help="url for this entry")
@click.option("--note", default = None, help="note for this entry")
def add(title, username, password, url, note):
    """Add a new password entry."""

    vault_path = get_vault_path()
    if vault_path is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    masterPassword = click.prompt("password", hide_input=True, confirmation_prompt=False)

    try:
        passwords = load_vault(masterPassword, vault_path)
    except Exception:
        click.echo("❌ Wrong master password or vault corrupted.")
        return

    for entry in passwords:
        if entry["title"] == title:
            click.echo(f"❌ An entry with title '{title}' already exists.")
            return

    if password is None:
        choice = click.prompt("No password provided. Do you want to generate a random password or you want to enter it manually(r or m)?", type=click.Choice(['r', 'm'], case_sensitive=False), show_choices=False)
        if choice == 'r':
            password = passGenerator(load_config().get("default_password_length", 20))
            click.echo(f"Generated password: {password}")
        elif choice == 'm':
            password = click.prompt("Enter password", hide_input=True, confirmation_prompt=True)
    newEntry = {
        "title" : title,
        "username" : username,
        "password" : password,
        "url": url,
        "notes": note
    }

    passwords.append(newEntry)

    try:
        save_vault(passwords, masterPassword, vault_path)
        click.echo(f"✅ Entry '{title}' added successfully.")
    except Exception as e:
        click.echo(f"\n❌ Failed to update vault: {e}")
        return

@cli.command(name="list")
def list_items():
    """List all saved entries."""

    vault_path = get_vault_path()
    if vault_path is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    masterPassword = click.prompt("password", hide_input=True, confirmation_prompt=False)

    try:
        passwords = load_vault(masterPassword, vault_path)
    except Exception:
        click.echo("❌ Wrong master password or vault corrupted.")
        return


    if passwords:
        for entry in passwords:
            click.echo(entry["title"])
    else:
        click.echo("Your vault is empty!!!!")


@cli.command()
@click.argument("title")
def get(title):
    """Get an entry by title."""

    vault_path = get_vault_path()
    clipboard_timeout = get_clipboard_timeout()
    if vault_path is None or clipboard_timeout is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    masterPassword = click.prompt("password", hide_input=True, confirmation_prompt=False)

    try:
        passwords = load_vault(masterPassword, vault_path)
    except Exception:
        click.echo("❌ Wrong master password or vault corrupted.")
        return


    for entry in passwords:
        if entry["title"] == title:
            try:
                pyperclip.copy(str(entry["password"]))
                click.echo(f"Username : {entry['username']} , Password : '✅copied to clipboard'")
                Timer(clipboard_timeout, clear_clipboard).start()
                break
            except Exception:
                click.echo("⚠️  Could not copy to clipboard (no clipboard tool installed).")
                click.echo("💡 To enable copying, install 'xclip' or 'wl-clipboard' on Linux.")
                click.echo(f"Username : {entry['username']} , Password : {entry['password']}")
                break
    else:
        click.echo(f"❌ No entry found with title '{title}'.")

@cli.command()
@click.argument("title")
@click.option("--username", default=None, help="New username")
@click.option("--password", default=None, help="New password")
@click.option("--url", default=None, help="New url")
@click.option("--note", default=None, help="New note")
def update(title, username, password, url, note):


    vault_path = get_vault_path()
    if vault_path is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    masterPassword = click.prompt("password", hide_input=True, confirmation_prompt=False)

    try:
        passwords = load_vault(masterPassword, vault_path)
    except Exception:
        click.echo("❌ Wrong master password or vault corrupted.")
        return

    for entry in passwords:
        if entry["title"] == title:
            if username is None:
                username = click.prompt("New username", default=entry["username"])
            if password is None:
                pw = click.prompt("New password (empty to keep)", default="", hide_input=True)
                if pw:
                    password = pw
            if url is None:
                url = click.prompt("New url", default=entry["url"])
            if note is None:
                note = click.prompt("New note", default=entry["notes"])

            entry["username"] = username if username else entry["username"]
            entry["password"] = password if password else entry["password"]
            entry["url"] = url if url else entry["url"]
            entry["notes"] = note if note else entry["notes"]
            break
    else:
        click.echo("Title not found.")
        return


    try:
        save_vault(passwords, masterPassword, vault_path)
        click.echo(f"✅ Entry '{title}' updated successfully.")
    except Exception as e:
        click.echo(f"\n❌ Failed to update vault: {e}")
        return


@cli.command()
@click.argument("length", default=20, type = int)
@click.option("--show", is_flag=True, help="Show password in terminal")
def generate(length, show):
    password = passGenerator(length)

    clipboard_timeout = get_clipboard_timeout()
    if clipboard_timeout is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    try:
        pyperclip.copy(password)
        click.echo("✅ Password copied to clipboard.")
        Timer(clipboard_timeout, clear_clipboard).start()
    except Exception:
        click.echo("⚠️  Could not copy to clipboard (no clipboard tool installed).")
        click.echo("💡 To enable copying, install 'xclip' or 'wl-clipboard' on Linux.")
        show = True

    if show:
        click.echo(f"Generated password: {password}")


@cli.command()
@click.argument("title")
def delete(title):

    vault_path = get_vault_path()
    if vault_path is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    masterPassword = click.prompt("password", hide_input=True, confirmation_prompt=False)

    try:
        passwords = load_vault(masterPassword, vault_path)
    except Exception:
        click.echo("❌ Wrong master password or vault corrupted.")
        return

    for entry in passwords:
        if entry["title"] == title:
            while True:
                test = click.prompt(f"⚠️ Are you sure you want to delete '{title}'? (y/n)")
                if test == 'y':
                    passwords.remove(entry)
                    break
                elif test == 'n':
                    click.echo("❌ Deletion cancelled.")
                    return
                else:
                    click.echo("❌ Invalid input. Please enter 'y' or 'n'.")
            break
    else:
        click.echo(f"❌ No entry found with title '{title}'.")
        return


    try:
        save_vault(passwords, masterPassword, vault_path)
        click.echo(f"✅ Entry {title} deleted successfully.")
    except Exception as e:
        click.echo(f"\n❌ Failed to save vault: {e}")
        return


@cli.command()
def change_master():

    vault_path = get_vault_path()
    if vault_path is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    counter = 0
    while True:
        if counter >= 4:
            click.echo("❌ Too many failed attempts. Master password change cancelled.")
            return
        masterPassword = click.prompt("password", hide_input=True, confirmation_prompt=False)
        try:
            passwords = load_vault(masterPassword, vault_path)
            break
        except Exception:
            click.echo("❌ Wrong master password")
            counter += 1

    while True:
        newMasterPass1 = click.prompt("new password", hide_input=True, confirmation_prompt=False)
        newMasterPass2 = click.prompt("retype new password", hide_input=True, confirmation_prompt=False)


        if newMasterPass1 == newMasterPass2:
            newMasterPass = newMasterPass1
            break

        click.echo("❌ Passwords do not match. Try again.\n")
    try:
        save_vault(passwords, newMasterPass, vault_path)
        click.echo("✅ Master password changed successfully.")
        click.echo("⚠️  Remember your master password! It cannot be recovered.")
    except Exception as e:
        click.echo(f"❌ Failed to save vault with new master password: {e}")
        return


@cli.command()
@click.argument("keyword")
@click.option("--field", default=None, help="Search only in specific field (title, username, url, notes)")
def search(keyword, field):
    keyword = keyword.lower()
    vault_path = get_vault_path()
    if vault_path is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    master_password = click.prompt("Master password", hide_input=True, confirmation_prompt=False)
    try:
        passwords = load_vault(master_password, vault_path)
    except Exception:
        click.echo("❌ Wrong master password or vault corrupted.")
        return

    valid_fields = ["title", "username", "url", "notes"]
    if field is not None and field not in valid_fields:
        click.echo("❌ Invalid field. Valid fields: title, username, url, notes")
        return

    click.echo(f"{'ID':<4} {'Title':<20} {'Username':<30} {'URL':<35} {'Notes':<25}")
    click.echo("-" * 114)

    results = []
    counter = 0

    for entry in passwords:
        title = (entry['title'] or '').lower()
        username = (entry['username'] or '').lower()
        url = (entry['url'] or '').lower()
        notes = (entry['notes'] or '').lower()

        match = False
        if field == "title":
            if keyword in title:
                match = True
        elif field == "username":
            if keyword in username:
                match = True
        elif field == "url":
            if keyword in url:
                match = True
        elif field == "notes":
            if keyword in notes:
                match = True
        else:
            if keyword in title or keyword in username or keyword in url or keyword in notes:
                match = True

        if match:
            counter += 1
            disp_title = (entry['title'] or '-')[:20]
            disp_user = (entry['username'] or '-')[:30]
            disp_url = (entry['url'] or '-')[:35]
            disp_notes = (entry['notes'] or '-')[:25]
            click.echo(f"{counter:<4} {disp_title:<20} {disp_user:<30} {disp_url:<35} {disp_notes:<25}")
            results.append(entry['title'])

    if counter == 0:
        click.echo(f"❌ No entries matching '{keyword}' found.")
        return

    selected = click.prompt("Enter ID to view details (or press Enter to skip)", default="", show_default=False)
    if selected:
        try:
            idx = int(selected) - 1
            if 0 <= idx < len(results):
                target_title = results[idx]
                for entry in passwords:
                    if entry['title'] == target_title:
                        try:
                            pyperclip.copy(entry['password'])
                            click.echo(f"Username: {entry['username']}, Password: ✅ copied to clipboard")
                            Timer(get_clipboard_timeout(), clear_clipboard).start()
                        except Exception:
                            click.echo("⚠️  Could not copy to clipboard.")
                            click.echo(f"Username: {entry['username']}, Password: {entry['password']}")
                        break
            else:
                click.echo("❌ Invalid ID.")
        except ValueError:
            click.echo("❌ Please enter a valid number.")

@cli.command()
@click.argument("filepath", default=None)
@click.option("--format", "fmt", default=None, type=click.Choice(['csv', 'json']), help="File format (csv or json). If not provided, format is detected from file extension.")
def export(filepath, fmt):
    vault_path = get_vault_path()
    if vault_path is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    masterPassword = click.prompt("password", hide_input=True, confirmation_prompt=False)

    try:
        passwords = load_vault(masterPassword, vault_path)
    except Exception:
        click.echo("❌ Wrong master password or vault corrupted.")
        return

    click.echo("⚠️ WARNING: The exported file will be UNENCRYPTED and readable by anyone.")
    if not click.confirm("Are you sure you want to export?"):
        click.echo("❌ Export cancelled.")
        return


    if fmt is None:
        if filepath:
            try:
                fmt = detect_format(filepath)
            except ValueError as e:
                click.echo(f"❌ {e}")
                return
        else:
            fmt = 'json'

    if filepath is None:
        filepath = f"ozpass_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{fmt}"


    if fmt == "csv":
        try:
            export_to_csv(passwords, filepath)
            click.echo(f"✅ Vault exported successfully to {filepath}.")
        except Exception as e:
            click.echo(f"❌ Failed to export vault: {e}")
    else:
        try:
            export_to_json(passwords, filepath)
            click.echo(f"✅ Vault exported successfully to {filepath}.")
        except Exception as e:
            click.echo(f"❌ Failed to export vault: {e}")

@cli.command(name="import")
@click.argument("filepath")
@click.option("--format", "fmt", default=None, type=click.Choice(['csv', 'json']),help="File format (csv or json). If not provided, format is detected from file extension.")
@click.option("--force", is_flag=True, help="Overwrite existing entries without asking")
def import_cli(filepath, fmt, force):
    vault_path = get_vault_path()
    if vault_path is None:
        click.echo("❌ Vault not initialized. Run 'init' first.")
        return

    master_password = click.prompt("Master password", hide_input=True, confirmation_prompt=False)

    try:
        passwords = load_vault(master_password, vault_path)
    except Exception:
        click.echo("❌ Wrong master password or vault corrupted.")
        return

    if fmt is None:
        try:
            fmt = detect_format(filepath)
        except ValueError as e:
            click.echo(f"❌ {e}")
            return

    try:
        if fmt == "csv":
            imported = import_from_csv(filepath)
        else:
            imported = import_from_json(filepath)
    except Exception as e:
        click.echo(f"❌ Failed to read import file: {e}")
        return

    new_count = 0
    updated_count = 0
    force_all = force

    for imported_entry in imported:
        title = imported_entry.get("title")
        if not title:
            click.echo("⚠️  Skipping entry with no title.")
            continue

        existing_entry = None
        for pw_entry in passwords:
            if pw_entry["title"] == title:
                existing_entry = pw_entry
                break

        if existing_entry is None:
            passwords.append(imported_entry)
            new_count += 1
        else:
            if force_all:
                existing_entry.update(imported_entry)
                updated_count += 1
            else:
                action = click.prompt(
                    f"⚠️  Entry '{title}' already exists. (o)verwrite / (s)kip / (a)ll overwrite / (q)uit?",
                    type=click.Choice(['o', 's', 'a', 'q']),
                    default='s',
                    show_choices=False
                )
                if action == 'o':
                    existing_entry.update(imported_entry)
                    updated_count += 1
                elif action == 'a':
                    existing_entry.update(imported_entry)
                    updated_count += 1
                    force_all = True
                elif action == 'q':
                    click.echo("❌ Import aborted. No changes saved.")
                    return

    try:
        save_vault(passwords, master_password, vault_path)
        if new_count > 0 or updated_count > 0:
            click.echo(f"✅ Imported {new_count} new entries, updated {updated_count} existing.")
        else:
            click.echo("No changes made.")
    except Exception as e:
        click.echo(f"❌ Failed to save vault: {e}")

#*******************************************************************************
@cli.group()
def config():
    """Manage configuration."""
    pass

@config.command()
def show():
    """Display current configuration."""
    try:
        config = load_config()
    except FileNotFoundError:
        click.echo("❌ Configuration file not found. Please run 'init' first.")
        return
    click.echo(json.dumps(config, indent=4))

@config.command()
@click.argument("key")
@click.argument("value")
def set(key, value):
    try:
        configs = load_config()
    except FileNotFoundError:
        click.echo("❌ Configuration file not found. Please run 'init' first.")
        return

    if key in configs:
        if key in ["session_timeout", "clipboard_timeout", "default_password_length"]:
            try:
                value = int(value)
            except ValueError:
                click.echo(f"❌ Value for '{key}' must be an integer.")
                return
        configs[key] = value
        try:
            save_config(configs)
            click.echo(f"✅ Setting '{key}' updated to {value}.")
        except Exception:
            click.echo("❌ Failed to save configuration.")
            return
    else:
        click.echo("❌ Invalid key. Valid keys: vault_path, session_timeout, clipboard_timeout, editor, default_password_length")


if __name__ == "__main__":
    cli()

