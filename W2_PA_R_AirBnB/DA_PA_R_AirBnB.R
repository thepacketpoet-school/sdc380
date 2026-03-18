# ============================================================
# PA: Data Cleaning and Visualization Using R
# Student: Haley Archer | Student ID: halarc1407
# Dataset: AirBnB 2022 Listings (v2) - AirBnBSummary_v2.xlsx
# ============================================================

# ── Markdown Cell (put this in a Markdown cell in Jupyter) ──
# # PA: Data Cleaning and Visualization Using R
# **Name:** Haley Archer  |  **Student ID:** halarc1407
# **Date:** 2026-03-15
# **Dataset:** AirBnB 2022 Listings (v2) | File: AirBnBSummary_v2.xlsx

# ── Cell 1: Load Libraries & Read Data ─────────────────────
library(readxl)
library(dplyr)
library(writexl)
library(ggplot2)
library(corrplot)
library(IRdisplay)

todays_date  <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
student_id   <- "halarc1407"
student_name <- "Haley Archer"

file_path <- "AirBnBSummary_v2.xlsx"

# Read Excel file (columns A-I only)
df <- read_excel(file_path, col_types = c(
  "numeric", "numeric", "text", "text", "text",
  "numeric", "numeric", "numeric", "numeric"
))
colnames(df) <- c(
  "id", "host_id", "host_name", "neighbourhood", "room_type",
  "price", "minimum_nights", "number_of_reviews", "availability_365"
)

# Add StudentID column
df$StudentID <- student_id

display_markdown(paste("###", student_name, "(", student_id, ") –", todays_date))


# ── Cell 2: Step 1 – Remove Duplicates ─────────────────────
display_markdown(paste("###", student_id, "-", todays_date))

# Find duplicates before cleaning
duplicate_rows_before <- df[duplicated(df), ]
display_markdown("### Duplicate Rows before cleaning")
display(duplicate_rows_before)

# Remove duplicates
df_cleaned <- df %>% distinct()

# Confirm no duplicates remain
duplicate_rows_after <- df_cleaned[duplicated(df_cleaned), ]
display_markdown("### Duplicate Rows after cleaning")
display(duplicate_rows_after)


# ── Cell 3: Step 2 – Fill Missing Values (MEDIAN) & Fix Capitalization ──
display_markdown(paste("###", student_id, "-", todays_date))

# Count missing values before
missing_before <- sapply(df_cleaned, function(x) sum(is.na(x)))
display_markdown("### Number of missing values in each column")
display(missing_before)

# Fix capitalization inconsistencies in room_type
display_markdown("### Capitalization inconsistencies corrected (str_to_title())")
cat("Before:", paste(unique(df_cleaned$room_type), collapse = ", "), "\n")
df_cleaned$room_type <- tools::toTitleCase(tolower(df_cleaned$room_type))
cat("After: ", paste(unique(df_cleaned$room_type), collapse = ", "), "\n")

# Fill missing numeric values with column MEDIAN
df_cleaned <- df_cleaned %>%
  mutate(across(
    where(is.numeric),
    ~ ifelse(is.na(.), median(., na.rm = TRUE), .)
  ))

# Confirm no missing values remain
missing_after <- sapply(df_cleaned, function(x) sum(is.na(x)))
display_markdown("### Number of missing values after filling with MEDIAN")
display(missing_after)


# ── Cell 4: Step 3 – Remove Outliers (3 × IQR) & Save ──────
display_markdown(paste("###", student_id, "-", todays_date))
display_markdown("### Outliers — price column (3 × IQR method)")

Q1  <- quantile(df_cleaned$price, 0.25, na.rm = TRUE)
Q3  <- quantile(df_cleaned$price, 0.75, na.rm = TRUE)
IQR_val <- Q3 - Q1
lower <- Q1 - 3 * IQR_val
upper <- Q3 + 3 * IQR_val

cat(sprintf("Q1 = %g   Q3 = %g   IQR = %g\n", Q1, Q3, IQR_val))
cat(sprintf("Lower bound: %g   Upper bound: %g\n", lower, upper))

outliers <- df_cleaned[df_cleaned$price < lower | df_cleaned$price > upper, ]
print(paste(nrow(outliers), "outlier rows found (price >", upper, ")"))
print(paste("Outlier price range: $", min(outliers$price), "–$", max(outliers$price)))

rows_before <- nrow(df_cleaned)
df_cleaned <- df_cleaned[df_cleaned$price >= lower & df_cleaned$price <= upper, ]
rows_after  <- nrow(df_cleaned)

display_markdown("### After removing outliers")
print(paste("Rows before:", rows_before, "  Rows after:", rows_after, "  Removed:", rows_before - rows_after))
print(paste("Cleaned price range: $", min(df_cleaned$price), "–$", max(df_cleaned$price)))

# Save cleaned data to new Excel file
cleaned_path <- "AirBnBSummary_v2_Cleaned_R.xlsx"
write_xlsx(df_cleaned, cleaned_path)
print(paste("Saved to:", cleaned_path))


# ── Cell 5: Descriptive Statistics ─────────────────────────
display_markdown(paste("###", student_id, "-", todays_date))
display_markdown("### Descriptive Statistics — AirBnB Listings (Cleaned)")

# Mode helper function (R has no built-in mode for numeric)
get_mode <- function(x) {
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}

print(paste("Total count of listings:                ", nrow(df_cleaned)))
print(paste("Minimum price:                          ", min(df_cleaned$price)))
print(paste("Maximum price:                          ", max(df_cleaned$price)))
print(paste("Mean price of listings:                 ", mean(df_cleaned$price)))
print(paste("Median of number_of_reviews:            ", median(df_cleaned$number_of_reviews)))
print(paste("Mode of minimum_nights:                 ", get_mode(df_cleaned$minimum_nights)))
print(paste("Standard Deviation of price:            ", sd(df_cleaned$price)))
print(paste("Correlation (price, availability_365):  ",
            cor(df_cleaned$price, df_cleaned$availability_365, use = "pairwise.complete.obs")))


# ── Cell 6: Histogram – Price Distribution ─────────────────
current_datetime <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")

ggplot(df_cleaned, aes(x = price)) +
  geom_histogram(binwidth = 10, fill = "skyblue", color = "black", linewidth = 0.4) +
  xlab("Price (USD)") +
  ylab("Number of Listings") +
  ggtitle(paste("Histogram of Listing Prices\nStudentID:", student_id, "–", current_datetime)) +
  theme_minimal() +
  theme(panel.grid.major = element_line(colour = "grey90"))


# ── Cell 7: Bar Chart – Avg Price by Neighbourhood ─────────
current_datetime <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")

hood_avg <- df_cleaned %>%
  group_by(neighbourhood) %>%
  summarise(avg_price = mean(price, na.rm = TRUE)) %>%
  arrange(avg_price)

ggplot(hood_avg, aes(x = reorder(neighbourhood, avg_price), y = avg_price)) +
  geom_bar(stat = "identity", fill = "green") +
  xlab("Neighbourhood") +
  ylab("Average Price (USD)") +
  ggtitle(paste("Average Listing Price by Neighbourhood\nStudentID:", student_id, "–", current_datetime)) +
  coord_flip() +
  theme_minimal() +
  theme(panel.grid.major = element_line(colour = "grey90"))


# ── Cell 8: Scatter Plot – Price vs Availability ───────────
current_datetime <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")

ggplot(df_cleaned, aes(x = availability_365, y = price)) +
  geom_point(aes(color = "Listings"), size = 1.5, alpha = 0.4) +
  geom_smooth(method = "lm", se = FALSE, aes(color = "Trendline")) +
  scale_color_manual(values = c("Listings" = "blue", "Trendline" = "red")) +
  xlab("Availability (days/year)") +
  ylab("Price (USD)") +
  ggtitle(paste("Price vs Availability (365 days)\nStudentID:", student_id, "–", current_datetime)) +
  theme_minimal() +
  theme(panel.grid.major = element_line(colour = "grey90"),
        legend.title = element_blank())


# ── Cell 9: Correlation Heatmap (corrplot) ─────────────────
current_datetime <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")

num_cols <- df_cleaned[, c("price", "minimum_nights", "number_of_reviews", "availability_365")]
corr_matrix <- cor(num_cols, use = "pairwise.complete.obs")

corrplot(
  corr_matrix,
  method   = "color",
  type     = "upper",
  addCoef.col = "black",
  tl.col   = "black",
  tl.srt   = 35,
  number.cex = 0.85,
  col      = colorRampPalette(c("white", "#ADD8E6", "#00008B"))(200),
  title    = paste("Correlation Heatmap\nStudentID:", student_id, "–", current_datetime),
  mar      = c(0, 0, 3, 0)
)
