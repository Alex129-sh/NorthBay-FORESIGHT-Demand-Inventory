

# Project FORESIGHT – NorthBay Living

Demand forecasting and inventory risk scoring (Zidio Development Internship).

## Problem
Retail stockouts lose sales; excess stock locks capital. This project builds a weekly SKU-level demand forecast and turns it into clear REORDER / MARKDOWN / HEALTHY actions.

## Key results
- Seasonal-naive baseline WAPE: **31.26%**
- LightGBM WAPE: **19.96%** (beats baseline by **11.29 points**)
- Latest risk snapshot: **5 REORDER**, **2 MARKDOWN**, **193 HEALTHY**
- Approx. sales at risk: ₹99,745 | locked capital: ₹197,699

## Project structure
- `notebooks/` – cleaning, EDA, features, LightGBM, risk scoring
- `reports/` – full project report and stage PDFs
- `data/` – cleaned and modelling outputs
