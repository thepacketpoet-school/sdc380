# ============================================================
# PA: Data Cleaning and Visualization Using Python
# Student: Haley Archer | Student ID: halarc1407
# Dataset: AirBnB 2022 Listings (v2) - AirBnBSummary_v2.xlsx
# ============================================================

# ── Markdown Cell (put this in a Markdown cell in Jupyter) ──
# # PA: Data Cleaning and Visualization Using Python
# **Name:** Haley Archer  |  **Student ID:** halarc1407
# **Date:** 2026-03-15
# **Dataset:** AirBnB 2022 Listings (v2) | File: AirBnBSummary_v2.xlsx

# ── Cell 1: Imports ─────────────────────────────────────────
from IPython.display import display, Markdown
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

todays_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
student_id  = "halarc1407"
student_name = "Haley Archer"

file_path = "AirBnBSummary_v2.xlsx"

# Read the Excel file into a DataFrame (columns A–I only)
df = pd.read_excel(file_path, usecols=range(9))
df.columns = [
    'id', 'host_id', 'host_name', 'neighbourhood',
    'room_type', 'price', 'minimum_nights',
    'number_of_reviews', 'availability_365'
]

# Fill StudentID column
df['StudentID'] = student_id

display(Markdown(f"### {student_name} ({student_id}) – {todays_date}"))


# ── Cell 2: Step 1 – Remove Duplicates ─────────────────────
display(Markdown(f"### {student_id} – {todays_date}"))
display(Markdown("## Duplicate Rows before cleaning"))

duplicate_rows_before = df[df.duplicated()]
display(duplicate_rows_before)

df_cleaned = df.copy()
df_cleaned.drop_duplicates(inplace=True)

duplicate_rows_after = df_cleaned[df_cleaned.duplicated()]
display(Markdown("## Duplicate Rows after cleaning"))
display(duplicate_rows_after)


# ── Cell 3: Step 2 – Fill Missing Values (MEDIAN) & Fix Capitalization ──
display(Markdown(f"### {student_id} – {todays_date}"))
display(Markdown("## Missing Values before filling"))

missing_before = df_cleaned.isnull().sum()
display(missing_before)

# Fix capitalization inconsistencies in room_type
display(Markdown("## Capitalization inconsistencies corrected (str.title())"))
print("Before:", df_cleaned['room_type'].unique().tolist())
df_cleaned['room_type'] = df_cleaned['room_type'].str.title()
print("After: ", df_cleaned['room_type'].unique().tolist())

# Fill missing numeric values with column MEDIAN
for col in df_cleaned.select_dtypes(include=['float64', 'int64']).columns:
    if df_cleaned[col].isnull().sum() > 0:
        median_val = df_cleaned[col].median()
        df_cleaned[col] = df_cleaned[col].fillna(median_val)

missing_after = df_cleaned.isnull().sum()
display(Markdown("## Missing Values after filling with MEDIAN"))
display(missing_after)


# ── Cell 4: Step 3 – Remove Outliers (3 × IQR) & Save ──────
display(Markdown(f"### {student_id} – {todays_date}"))
display(Markdown("## Outliers — price column (3 × IQR method)"))

Q1  = df_cleaned['price'].quantile(0.25)
Q3  = df_cleaned['price'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 3 * IQR
upper = Q3 + 3 * IQR

print(f"Q1 = ${Q1:.2f}   Q3 = ${Q3:.2f}   IQR = ${IQR:.2f}")
print(f"Lower bound: ${lower:.2f}   Upper bound: ${upper:.2f}")

outliers = df_cleaned[(df_cleaned['price'] < lower) | (df_cleaned['price'] > upper)]
display(Markdown(f"**{len(outliers)} outlier rows found (price > ${upper:.2f})**"))
display(Markdown(f"Outlier price range: ${outliers['price'].min():.0f} – ${outliers['price'].max():.0f}"))

rows_before = len(df_cleaned)
df_cleaned = df_cleaned[
    (df_cleaned['price'] >= lower) & (df_cleaned['price'] <= upper)
].copy()
rows_after = len(df_cleaned)

display(Markdown("## After removing outliers"))
print(f"Rows before: {rows_before}   Rows after: {rows_after}   Removed: {rows_before - rows_after}")
print(f"Cleaned price range: ${df_cleaned['price'].min():.2f} – ${df_cleaned['price'].max():.2f}")

# Save cleaned DataFrame to a new Excel file
cleaned_path = "AirBnBSummary_v2_Cleaned.xlsx"
df_cleaned.to_excel(cleaned_path, index=False)
display(Markdown(f"**Saved to:** `{cleaned_path}`"))


# ── Cell 5: Descriptive Statistics ─────────────────────────
display(Markdown(f"### {student_id} – {todays_date}"))
display(Markdown("## Descriptive Statistics — AirBnB Listings (Cleaned)"))

total_count    = len(df_cleaned)
min_price      = df_cleaned['price'].min()
max_price      = df_cleaned['price'].max()
mean_price     = df_cleaned['price'].mean()
median_reviews = df_cleaned['number_of_reviews'].median()
mode_nights    = df_cleaned['minimum_nights'].mode()[0]
std_price      = df_cleaned['price'].std()
corr_price_avail = df_cleaned['price'].corr(df_cleaned['availability_365'])

print(f"Total count of listings:                 {total_count}")
print(f"Minimum price:                           ${min_price:.2f}")
print(f"Maximum price:                           ${max_price:.2f}")
print(f"Mean price of listings:                  ${mean_price:.2f}")
print(f"Median of number_of_reviews:             {median_reviews}")
print(f"Mode of minimum_nights:                  {mode_nights}")
print(f"Standard Deviation of price:             ${std_price:.2f}")
print(f"Correlation (price, availability_365):   {corr_price_avail:.6f}")


# ── Cell 6: Histogram – Price Distribution ─────────────────
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

plt.figure(figsize=(10, 6))
plt.hist(df_cleaned['price'], bins=30, color='skyblue', edgecolor='black', linewidth=0.6)
plt.xlabel('Price (USD)', fontsize=11)
plt.ylabel('Number of Listings', fontsize=11)
plt.title(f'Histogram of Listing Prices\nStudentID: {student_id} – {current_datetime}', fontsize=10)
plt.grid(True, color='#cccccc', linewidth=0.5)
plt.tight_layout()
plt.show()


# ── Cell 7: Bar Chart – Avg Price by Neighbourhood ─────────
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

hood_avg = df_cleaned.groupby('neighbourhood')['price'].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
bars = plt.bar(hood_avg.index, hood_avg.values, color='#4472C4', edgecolor='white', linewidth=0.8)
for bar, val in zip(bars, hood_avg.values):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
             f'${val:.0f}', ha='center', va='bottom', fontsize=9)
plt.xlabel('Neighbourhood', fontsize=11)
plt.ylabel('Average Price (USD)', fontsize=11)
plt.title(f'Average Listing Price by Neighbourhood\nStudentID: {student_id} – {current_datetime}', fontsize=10)
plt.xticks(rotation=15)
plt.grid(True, axis='y', color='#cccccc', linewidth=0.5)
plt.tight_layout()
plt.show()


# ── Cell 8: Scatter Plot – Price vs Availability ───────────
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

x = df_cleaned['availability_365']
y = df_cleaned['price']
z = np.polyfit(x, y, 1)
p_line = np.poly1d(z)
x_fit = np.linspace(x.min(), x.max(), 200)

plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', s=12, alpha=0.5, label='Listings', zorder=3)
plt.plot(x_fit, p_line(x_fit), color='red', linewidth=2,
         label=f'Trendline: y = {z[0]:.2f}x + {z[1]:.1f}')
plt.xlabel('Availability (days/year)', fontsize=11)
plt.ylabel('Price (USD)', fontsize=11)
plt.title(f'Price vs Availability (365 days)\nStudentID: {student_id} – {current_datetime}', fontsize=10)
plt.legend(fontsize=9)
plt.grid(True, color='#cccccc', linewidth=0.5)
plt.tight_layout()
plt.show()


# ── Cell 9: Correlation Heatmap ────────────────────────────
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

num_cols = df_cleaned[['price', 'minimum_nights', 'number_of_reviews', 'availability_365']]
corr_matrix = num_cols.corr()

plt.figure(figsize=(8, 6.5))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    linewidths=0.5,
    square=True,
    vmin=-1, vmax=1,
    xticklabels=['price', 'min_nights', 'num_reviews', 'avail_365'],
    yticklabels=['price', 'min_nights', 'num_reviews', 'avail_365']
)
plt.title(f'Correlation Heatmap — Numeric Variables\nStudentID: {student_id} – {current_datetime}',
          fontsize=10, pad=12)
plt.tight_layout()
plt.show()
