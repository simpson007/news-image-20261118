# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/simpson007/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/simpson007/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A program that writes one image summing up the world's news of Wednesday 18 November 2026 — Iranian drones over Bahrain and Kuwait, the Kerch bridge span falling, the Shenzhen APEC summit, and a market slide — to /output/entry.png.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## What's in the picture

A one-page newspaper front page for Wednesday 18 November 2026:

- **Lead — The Gulf:** Iranian drones struck at Bahrain and Kuwait before dawn, aimed at US Patriot systems at Ali Al-Salem air base; Bahrain said its defences shot several down. The US confirmed its jets hit a missile site on Qeshm Island, and a third carrier group is sailing in.
- **Ukraine:** Kyiv hit the Crimea bridge for a second day; part of its road span fell into the strait. Russia struck two bridges in Kyiv in reply.
- **Shenzhen:** Putin flew in for the APEC summit, a day before the first three-way meeting with Xi and Trump. Trump was in Manila for the Quad first.
- **Markets:** Dow −1.6%, S&P −1.0% (lowest since July), Nasdaq −0.7%, Brent −0.7%, gold −1.4% to a one-year low; Nvidia beat earnings after the bell, up 4%.
- **Also:** Ebola in DR Congo (11,000 cases, 5,400 dead), Peltola flipping Alaska's Senate seat as Democrats take 56, Category 5 Cyclone Xavier over the Cook Islands, four nations urging Israel to open Gaza aid crossings, Dhoni retiring from the IPL, a Russian plane crash killing 19, and the US losing its measles-free status.

## How it was made

`render.py` draws the front page with Pillow (deterministic: fixed text and geometry, no network, no randomness) and writes `entry.png` (1024×1024, about 140 KiB). `main.ts` (Node 22, standard library only) copies it to `/output/entry.png`, so two runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ngqr1ydj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
