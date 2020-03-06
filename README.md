# VUB Restaurant Scraper Edition 123493939

This is the 123493939th edition of the VUB scraper. I hope this one is a bit easier to maintain.

# Run

The script requires 2 parameters. The output folder for the JSON files, and the version number.
In version 1 the evening menus are ignored, and the format for the android app is used.
In version 2 the evening menu is scraped, and the json has a different format. See `generator_vx.py` for detais.

```
python main.py --version 1 --output /path/to/dir --backup /previous/menus
```

# Docker

Obviously.

```
docker build -t vub-resto-v2 .
docker run --rm -it -v /path/to/dir:/data vub-resto-v2 --version 1 --backup
```