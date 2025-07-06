# 🎴 Balatro Mod Updater

A Python script that automatically downloads and installs the latest versions of several Balatro mods directly from GitHub. It compares your local mod files with the latest available versions and replaces only when changes are detected.

---

## 📦 Supported Mods

This script currently supports updating the following mod as an example:

- 🔹 [smods](https://github.com/Steamodded/smods)

To add more mods:

- Fill in the name of the mod
- give the download URL (Right click on where it says "Download Zip" and copy the link)
- Give the name of the folder in your mods file (ex. "smods-main")
- and the color you want the mod name to be in the cmd prompt using colorama
  
you can copy this format:
<pre>
  { 
  "name": "MOD NAME",
  "url": "URL HERE",
  "folder_name": "FOLDER NAME",
  "color": Fore.CYAN 
  },
</pre>
---

## 🚀 Features

- ✅ Downloads mods directly from GitHub (or wherever)
- 🔄 Compares local files to tell you if they have changed
- 📂 Installs updates cleanly, overwriting outdated versions
- 📊 Displays progress bars and color-coded output
- 🧪 Uses a temporary folder to avoid polluting your mod directory
- 🎨 Fully customizable to your liking
---

## 🛠 Requirements

Make sure you have Python 3.8 or later installed.

MAKE SURE THAT YOU HAVE THESE PACKAGES INSTALLED:
- requests
- tqdm
- colorama
  
Run this command in the terminal to download them:
<pre>pip install requests tqdm colorama</pre>
---
