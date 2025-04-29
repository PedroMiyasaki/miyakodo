# 🏯 Miyakodo

**Miyakodo** is a project designed to make money on the Brazilian Stock Exchange (B3) by identifying and following the actions of relevant players based on order book (livro de ofertas) behavior.

The idea is not based on privileged access to insider information, but on extracting signals from observable patterns that large, relevant market participants leave through their buying and selling activities.  
In essence: **Miyakodo watches the footprints that important players leave behind.**

---

## 🎯 Project Vision

- **Objective:** Detect significant players operating in the Brazilian stock market by analyzing order book movements, then generate actionable alerts based on these insights.
- **Approach:** 
  - Build a daily ETL pipeline to collect and curate end-of-day order book data.
  - Develop KPIs that track and highlight the behavior of potential "relevant players."
  - Set up an alert system (e.g., Telegram notifications) based on unusual or strategic activity.
  - Weekly, refine identification of the most impactful players based on accumulated behavior.

---

## 🛠️ Architecture (Planned)

The project follows the **Medallion Architecture** (Bronze → Silver → Gold):

- **Landing (Bronze):** Raw end-of-day order book data collected daily.
- **Curated (Silver):** Cleaned and standardized order book data.
- **Specialized (Gold):** KPI-enriched datasets and identified relevant players.

All code follows a **single-package structure** under `src/miyakodo/` to avoid import problems and facilitate scalability.

---

## 🔁 Pipelines

| Pipeline | Frequency | Description |
|:---------|:-----------|:------------|
| **Daily ETL** | Daily | Fetch raw order book data, clean it, compute KPIs, append to history, and send alerts based on predefined rules. |
| **Weekly Analysis** | Weekly | Analyze curated historical data to refine the identification of consistently relevant players and produce an atomic "relevant_players" table. |

---

## 📦 Project Structure

```text
miyakodo/
├── src/
│   ├── miyakodo/
│   │   ├── data/
│   │   │   ├── landing/        # Raw data (Bronze)
│   │   │   ├── curated/        # Cleaned data (Silver)
│   │   │   └── specialized/    # KPI-enriched tables (Gold)
│   │   ├── pipelines/
│   │   │   ├── daily/
│   │   │   └── weekly/
│   │   ├── common/             # Utilities (configs, logging, telegram client)
│   │   └── kpis/               # KPI calculation logic
│   └── main.py                 # Entry point to run pipelines manually
├── tests/                      # Unit and integration tests
├── notebooks/                  # Exploratory data analysis
├── configs/                    # Configuration files and secrets
└── README.md
```

---

## 🚧 Current Status: Data Discovery Phase

Miyakodo is currently in the **early stage** of development:

- **Step 1:** Finding reliable sources of detailed order book data (preferably containing broker or participant-level information).
- **Step 2:** Prototyping the initial ETL to collect and store snapshots.
- **Step 3:** Exploring the data manually to assess whether relevant player behavior can be realistically identified.

No automated pipelines are in production yet.  
The immediate focus is **validating data availability and quality** before proceeding to KPI generation and alerting.

---

## 📅 Next Steps

- Complete order book data extraction.
- Develop basic visualizations to manually inspect participant behaviors.
- Decide whether identified patterns are strong enough to justify full pipeline automation.

---

## ⚠️ Disclaimer

This project is for educational and research purposes only.  
No investment advice or real trading operations are guaranteed by this software.