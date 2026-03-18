# PA: Data Cleaning and Visualization Using R

**Student:** Haley Archer  
**Student ID:** halarc1407  
**Course:** Data Analytics  
**Assignment:** W3 PA 2.5 – Data Cleaning and Visualization Using R

---

## Dataset

`AirBnBSummary_v2.xlsx` — Summarized portion of Inside AirBnB's 2022 Listing dataset for Columbus, OH.

**Columns:** id, host_id, host_name, neighbourhood, room_type, price, minimum_nights, number_of_reviews, availability_365

---

## Files

| File | Description |
|------|-------------|
| `DA_PA_R_AirBnB.R` | Main R script — run each cell block in Jupyter (R kernel) |
| `AirBnBSummary_v2.xlsx` | Raw input dataset |
| `AirBnBSummary_v2_Cleaned_R.xlsx` | Output — cleaned dataset (generated on run) |

---

## How to Run

1. Open **JupyterLab** (via Anaconda Navigator or VCASTLE)
2. Create a new **R** notebook: `DA_PA_R.ipynb`
3. Copy each `# ── Cell N` block from `DA_PA_R_AirBnB.R` into separate notebook cells
4. Place the first block in a **Markdown** cell, all others as **Code** cells
5. Place `AirBnBSummary_v2.xlsx` in the same directory as the notebook
6. Run all cells — the cleaned file will be saved automatically

---

## What the Code Does

### Data Cleaning
- **Remove duplicates** — `distinct()` removes 4 duplicate rows (1,779 → 1,775)
- **Fill missing values** — `mutate(across())` fills 4 missing prices and 5 missing availability values with column MEDIAN
- **Fix capitalization** — `tools::toTitleCase()` standardizes room_type (`Private room` → `Private Room`)
- **Remove outliers** — 3×IQR method removes 58 high-price outliers (> $444) → 1,717 rows remain

### Descriptive Statistics
Total count, min/max/mean price, median reviews, mode minimum nights, sd price, price↔availability correlation

### Visualizations (ggplot2 + corrplot)
- Histogram of price distribution
- Horizontal bar chart of average price by neighbourhood (coord_flip)
- Scatter plot: price vs availability with lm trendline
- Upper-triangle correlation heatmap (corrplot)

---

## R Package Requirements

```r
install.packages(c("readxl", "dplyr", "writexl", "ggplot2", "corrplot", "IRdisplay"))
```
