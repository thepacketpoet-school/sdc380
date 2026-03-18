# PA: Data Cleaning and Visualization Using Python

**Student:** Haley Archer  
**Student ID:** halarc1407  
**Course:** Data Analytics  
**Assignment:** W3 PA – Data Cleaning and Visualization Using Python

---

## Dataset

`AirBnBSummary_v2.xlsx` — Summarized portion of Inside AirBnB's 2022 Listing dataset for Columbus, OH.

**Columns:** id, host_id, host_name, neighbourhood, room_type, price, minimum_nights, number_of_reviews, availability_365

---

## Files

| File | Description |
|------|-------------|
| `DA_PA_Python_AirBnB.py` | Main Python script — run each cell block in Jupyter |
| `AirBnBSummary_v2.xlsx` | Raw input dataset |
| `AirBnBSummary_v2_Cleaned.xlsx` | Output — cleaned dataset (generated on run) |

---

## How to Run

1. Open **JupyterLab** (via Anaconda Navigator or VCASTLE)
2. Create a new Python 3 notebook: `DA_PA_Python.ipynb`
3. Copy each `# ── Cell N` block from `DA_PA_Python_AirBnB.py` into separate notebook cells
4. Place the first block in a **Markdown** cell, all others as **Code** cells
5. Place `AirBnBSummary_v2.xlsx` in the same directory as the notebook
6. Run all cells — the cleaned file will be saved automatically

---

## What the Code Does

### Data Cleaning
- **Remove duplicates** — `drop_duplicates()` removes 4 duplicate rows
- **Fill missing values** — `fillna(median)` fills 4 missing prices and 5 missing availability values
- **Fix capitalization** — `str.title()` standardizes room_type (`Private room` → `Private Room`)
- **Remove outliers** — 3×IQR method removes 58 high-price outliers (> $444)

### Descriptive Statistics
Total count, min/max/mean price, median reviews, mode minimum nights, std price, price↔availability correlation

### Visualizations
- Histogram of price distribution
- Bar chart of average price by neighbourhood  
- Scatter plot: price vs availability with trendline
- Seaborn correlation heatmap

---

## Requirements

```
pandas
numpy
matplotlib
seaborn
openpyxl
```

Install with:
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```
