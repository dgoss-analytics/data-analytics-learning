# PRS — Player Reliability Score

**An original baseball statistic built from scratch in Python.**

## What Is PRS?

PRS (Player Reliability Score) measures the **offensive reliability** of MLB position players — not just how good they are, but how reliably good they will be.

Most fantasy baseball and front office metrics measure peak performance. PRS measures *dependable* performance. A player who posts elite numbers in 90 games is less valuable than one who posts solid numbers in 155 games. PRS quantifies that gap.

## The Core Idea

PRS combines three things:

1. **Offensive Production** — a weighted blend of key hitting metrics
2. **Age Factor** — accounts for the natural aging curve of MLB players
3. **Resilience Modifier** — measures how players perform before and after IL stints

The result is a single score that reflects both offensive value and the probability that a player will actually be available and productive.

## Methodology

### Production Component
A weighted blend of hitting metrics, with weights determined through systematic correlation testing against 2026 WAR data. Every weight was data-driven — nothing was assumed.

### Age Factor
An 8-tier aging system based on established MLB aging curves. Players are penalized progressively as they age, with a floor to reflect that veteran players still have baseline value.

### Resilience Modifier
Built from actual game log data — not injury designations. The model detects gaps in a player's appearance history, then measures their OBP performance in the 15 games before and after each IL stint. Players who bounce back stronger are rewarded. Players who decline are penalized.

## Validation

PRS was validated against 2026 WAR (Wins Above Replacement) data from Baseball Reference.

| Validation | Result |
|------------|--------|
| PRS vs 2026 WAR | Strong positive correlation |
| PRS vs 2025 WAR | Weak correlation |
| PRS vs 2024 WAR | Weak correlation |

**Key finding:** PRS correlates strongly with *current* WAR and weakly with prior-year WAR. This confirms PRS is measuring who a player IS right now — exactly what you need for fantasy decisions and salary negotiations.

## Tech Stack

- **Python 3.14**
- **pandas** — data manipulation and weighted calculations
- **requests** — MLB Stats API calls (no authentication required)
- **fuzzywuzzy** — fuzzy name matching for WAR validation
- **MLB Stats API** — live player data, game logs, season stats

## Sample Output

```
name                prs    obp   hr_rate  availability_factor  war
Nick Kurtz         0.2271  0.410  0.0524        1.00           1.6
Yordan Alvarez     0.2136  0.403  0.0567        0.91           2.0
Bobby Witt Jr.     0.2131  0.375  0.0361        0.97           3.0
Juan Soto          0.2094  0.394  0.0530        0.94           0.8
Aaron Judge        0.2060  0.432  0.0791        0.82           2.6
```

## What's Next

- **PRS-P** — a pitcher version using ERA, strikeout rate, and innings pitched
- **Tableau dashboard** — interactive PRS leaderboard by position
- **Performance Resilience Score** — separate component measuring how players respond to demotion and return from the minors
- **Backtesting** — using prior PRS scores to predict future WAR

## About

Built by Dave Goss as part of a self-directed data analytics learning journey targeting sports analytics roles in the Nashville market. This project applies Python, pandas, API integration, feature engineering, and correlation analysis to an original research question.

Portfolio: [github.com/dgoss-analytics](https://github.com/dgoss-analytics)  
LinkedIn: [linkedin.com/in/davidrgoss](https://linkedin.com/in/davidrgoss)

---

*Note: Full formula weights, tuning methodology, and implementation details are proprietary.*
