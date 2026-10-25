# About Picload

Picload downloads image collections and albums from the internet. It's good for wallpapers and comics.

At the moment `picload` has some downfalls, and it will be replaced by `imgload` that uses leading zeros in `curl` URL glob ranges for improved efficiency. `Imgload` also adds automatic range detection features. The `anomtool pic` command will remain supporting manual, customized downloads, while `anomtool img` will use automation to its full potential. The `anomtool picload` will remain working til `anomtool pic` will replace it.

# How to run

To Run in environment try:

```bash
make install  # Pulls venv, deps, etc.
uv run anomtool picload
```

Alternatively you can use picload globally.

Note: Since`--from anomlib` says in which pkg the command should be found.

```bash
uv tool run --from anomlib anomtool picload
```

# Picload in work

Example of downloading `Pepper&Carrot` Webcomic which is distributed under `CC-BY` license: Episode `39`: The Tavern with `12` pages:

`pic "https://www.peppercarrot.com/0_sources/ep39_The-Tavern/low-res/en_Pepper-and-Carrot_by-David-Revoy_E39P" -S12`

Note: `--ending='.jpg'` or `-e'.jpg'` is default value thus can be optional.

Result: `https://www.peppercarrot.com/0_sources/ep39_The-Tavern/low-res/en_Pepper-and-Carrot_by-David-Revoy_E39P[01-12].jpg` `-o img-#1.jpg`

# Imgload in work

At the moment imgload automates some processes, meanwhile, commands may seem bigger at beginning.
