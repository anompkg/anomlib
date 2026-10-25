# About Picload

Picload downloads image collections and albums from the internet. It's good for wallpapers and comics.

At the moment `picload` has some downfalls, and it will be replaced by `imgload` that uses leading zeros in `curl` URL glob ranges for improved efficiency. `Imgload` also adds automatic range detection features. The `anomtool picload` will remain working til `anomtool pic` will replace it. The `anomtool pic` command will remain supporting manual, customized downloads, while `anomtool img` will use automation to its full potential.

## How to run

To Run in environment try:

```bash
make install  # Make venv, Pull deps, etc.
uv run anomtool picload
```

Alternatively you can use picload globally.

Note: Since `--from anomlib` says at which pkg `anomtool` command can be found.

```bash
uv tool run --from anomlib anomtool picload
```

## Picload in work

Example of downloading `Pepper&Carrot` Webcomic which is distributed under `CC-BY` license: Episode `39`: The Tavern with `12` pages:

`pic "https://www.peppercarrot.com/0_sources/ep39_The-Tavern/low-res/en_Pepper-and-Carrot_by-David-Revoy_E39P" -S12`

Note: `--ending='.jpg'` or `-e'.jpg'` is default value thus can be optional.

Result: `https://www.peppercarrot.com/0_sources/ep39_The-Tavern/low-res/en_Pepper-and-Carrot_by-David-Revoy_E39P[01-12].jpg` `-o img-#1.jpg`

## Imgload in work

At the moment imgload automates some processes, meanwhile, commands may seem bigger at beginning of development.

How it works now? Let's compare it with process of downloading same comic:

`img https://www.peppercarrot.com/0_sources/ep39_The-Tavern/low-res/en_Pepper-and-Carrot_by-David-Revoy_E39P01.jpg' 'https://www.peppercarrot.com/0_sources/ep39_The-Tavern/low-res/en_Pepper-and-Carrot_by-David-Revoy_E39P12.jpg'`

By providing 2 links, it will compare them and find out that they differ with range 01-12, thus return:

`https://www.peppercarrot.com/0_sources/ep39_The-Tavern/low-res/en_Pepper-and-Carrot_by-David-Revoy_E39P[01-12].jpg`

`Note`: Also, there is shorter and faster way of doing this. Even tho at this moment next commands will raise an error as both links got 4 numbers `(0, 39, 39, 01)` and `(0, 39, 39, 12)`. It will be adjusted soon!

Just use one link of last `12th` comic, and it should work right away if link has only 1 number:

`img 'https://www.peppercarrot.com/0_sources/ep39_The-Tavern/low-res/en_Pepper-and-Carrot_by-David-Revoy_E39P12.jpg'`

It would return expected result, but since it got `4 numbers`, you will soon be able to specify which number is the `page` number, in our case it is `4th` (`--page=4`), the last number with `12` value:

`img 'https://www.peppercarrot.com/0_sources/ep39_The-Tavern/low-res/en_Pepper-and-Carrot_by-David-Revoy_E39P12.jpg' -p4`

And voilà, behold:

`https://www.peppercarrot.com/0_sources/ep39_The-Tavern/low-res/en_Pepper-and-Carrot_by-David-Revoy_E39P[01-12].jpg`

`Note`: In case of multiple numbers, the default page may be the last one, which can make sense, but pay attention if that is not the case or if URLs got queries.
