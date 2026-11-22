[![bounty](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Andia86/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Andia86/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

# Sunday 22 November 2026: 40 stories, 5 continents, one page

An entry for the make.fun bounty
[news-image-20261122](https://make.fun/bounty/news-image-20261122) —
one image that sums up the world news of Sunday 22 November 2026.

## What is on the page

- A masthead that names the day: **Sunday 22 November 2026**.
- **11 illustrated cards** for the day's biggest stories — COP31 running
  into overtime in Antalya, tankers hit in Hormuz, the Crimean Bridge
  strikes, the capture of 'El Chapo Isidro', the Jakarta factory fire,
  the FBI database hack, the Seattle airport arrests, two spacecraft
  reaching Mercury, Verstappen's Las Vegas win, Shuri Castle restored,
  and the Nigeria funeral-boat disaster.
- A **dot world map** ("Where it happened") with a numbered pin for every
  terrestrial card; card 8 is at Mercury, off the map.
- **29 more stories as numbered briefs**, so the count reaches 40 across
  five continents: politics, war, courts, science, sport and one lock of
  George Washington's hair.
- Every story happened, or was first reported, on 22 November 2026;
  disputed claims are attributed on the page. The source for each story
  is listed in [NEWS_SOURCES.md](NEWS_SOURCES.md).

## How it is built

- `make_image.py` draws the page with Pillow from the fixed story data in
  the file: masthead, cards, pictograms, dot map, briefs, footer. It is
  deterministic — no clock, no randomness, no network — and writes
  `entry.png` (1024×1024).
- `main.py` is the submitted program (Python 3.13, standard library
  only): it copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`,
  byte for byte, so both grading runs produce identical bytes.

## Run it

```sh
python3 make_image.py                          # redraws entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
