[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/iuzuka/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/iuzuka/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Page — Saturday 21 November 2026

One image summing up the world's news of Saturday 21 November 2026, as a
newspaper front page: `main.ts` copies `entry.png` to `/output/entry.png`.

## The day's news (researched 21 Nov 2026)

- **Lead — Poland:** two Russian cruise missiles and a jet-powered drone
  came down in south-east Poland during Russia's massive overnight attack
  on Ukraine. PM Donald Tusk calls it a deliberate provocation; NATO
  chief Mark Rutte is due in Warsaw on Saturday.
- **Summit — Shenzhen:** the first-ever Trump–Xi–Putin trilateral meeting
  at the APEC summit ends with a four-point joint declaration on peace
  and security, but no deal on Ukraine or Iran.
- **Markets:** Wall Street slumps into correction — the S&P 500 falls
  about 3.7% as AI shares sell off.
- **Asia — Indonesia:** nine days after Gibran Rakabuming quit as vice
  president, the VP seat is still vacant; the MPR waits for President
  Prabowo's two names, with the vote to pick his successor set for
  2 December.
- **Also:** Mongolia's president quits, opening the way for an early
  election; the ICJ genocide verdict reverberates; the UK and EU sign
  trade deals; Trump pardons Pete Rose; a tanker is hit in the Strait
  of Hormuz; at least 11 killed in Kyiv strikes.

## How it was built

`draw_news21.py` (PIL) composites two generated press-style illustrations
(`assets/*.webp`) with crisp programmatic typesetting — no AI-generated
text. The illustrations picture the events; they are not the events
themselves. Rebuild with `python3 draw_news21.py`; it writes a
1024x1024 PNG under 1 MiB.
