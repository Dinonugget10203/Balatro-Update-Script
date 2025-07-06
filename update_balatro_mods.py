"""
To add more mods:
-Fill in the name of the mod
-give the download URL (Right click on where it says "Download Zip" and copy the link)
-Give the name of the folder in your mods file (ex. "smods-main")
-and the color you want the mod name to be in the cmd prompt
you can copy this format:
    {
        "name": "MOD NAME",
        "url": "URL HERE",
        "folder_name": "FOLDER NAME",
        "color": Fore.CYAN
    },

"""



import os
import shutil
import zipfile
import requests
import tempfile
import filecmp
import msvcrt
from tqdm import tqdm
from colorama import init, Fore, Style

init(autoreset=True)

WHITE = Style.BRIGHT + Fore.WHITE
MODS_DIR = os.path.expandvars(r"%APPDATA%\Balatro\Mods")

MODS = MODS = [
    {
        "name": "smods",
        "url": "https://github.com/Steamodded/smods/archive/refs/heads/main.zip",
        "folder_name": "smods-main",
        "color": Fore.CYAN
    },
  #replace this line with new mods
]


def prefix(mod_name: str, color: str, msg: str) -> None:
    print(f"{WHITE}[{color}{mod_name}{WHITE}] {msg}{Style.RESET_ALL}")


def download_with_progress(mod_name, url, zip_path, color):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))

    # Use raw ANSI color codes in tqdm description
    desc = f"{WHITE}[{color}{mod_name}{WHITE}]"

    with open(zip_path, 'wb') as f, tqdm(
        total=total if total else None,
        unit='B',
        unit_scale=True,
        desc=desc,
        ncols=70,
        bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} {rate_fmt}" if total else "{desc}: Downloading...",
        ascii=True
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))



def download_and_extract(mod_name, url, base_temp_dir, color):
    zip_path = os.path.join(base_temp_dir, f"{mod_name}.zip")
    extract_path = os.path.join(base_temp_dir, f"{mod_name}_extract")

    download_with_progress(mod_name, url, zip_path, color)

    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    extracted_folder = next(
        os.path.join(extract_path, d)
        for d in os.listdir(extract_path)
        if os.path.isdir(os.path.join(extract_path, d))
    )
    return extracted_folder


def compare_dirs(old_dir, new_dir, rel=""):
    diff = filecmp.dircmp(old_dir, new_dir)
    out = {"added": [], "removed": [], "changed": []}

    out["added"].extend(os.path.join(rel, f) for f in diff.right_only)
    out["removed"].extend(os.path.join(rel, f) for f in diff.left_only)
    out["changed"].extend(os.path.join(rel, f) for f in diff.diff_files)

    for sub in diff.common_dirs:
        sub_diffs = compare_dirs(
            os.path.join(old_dir, sub),
            os.path.join(new_dir, sub),
            os.path.join(rel, sub),
        )
        for k in out:
            out[k].extend(sub_diffs[k])
    return out


def install_mod(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main():
    with tempfile.TemporaryDirectory(prefix="balatro_mod_update_") as tmp:
        for mod in MODS:
            name = mod["name"]
            url = mod["url"]
            folder = mod["folder_name"]
            color = mod["color"]
            target = os.path.join(MODS_DIR, folder)
            
            extracted = download_and_extract(name, url, tmp, color)

            prefix(name, color, "Comparing with current version...")
            if os.path.exists(target):
                diffs = compare_dirs(target, extracted)
                if any(diffs.values()):
                    prefix(name, color, "Changes found:")
                    for f in diffs["added"]:
                        print(f"{Fore.BLUE}         Added:   {f}")
                    for f in diffs["removed"]:
                        print(f"{Fore.RED}         Removed: {f}")
                    for f in diffs["changed"]:
                        print(f"{Fore.MAGENTA}         Changed: {f}")
                else:
                    prefix(name, color, f"{Fore.GREEN}No changes found.")
            else:
                prefix(name, color, f"{Fore.GREEN}No previous version found. Will install fresh.")

            prefix(name, color, "Installing new version...\n")
            install_mod(extracted, target)

    print(f"{Style.BRIGHT}{Fore.GREEN}[DONE] All mods updated.")
    print(f"{WHITE}Press any key to exit...", end="", flush=True)
    msvcrt.getch()


if __name__ == "__main__":
    main()
