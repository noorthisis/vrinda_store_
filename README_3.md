# 🛍️ Vrinda Store — Sales Analysis Dashboard

An interactive data analysis dashboard built with **Python**, **Streamlit**, and **Plotly**, based on Vrinda Store's 2022 annual sales data.

🔗 **Live Demo:** [Click to View App](https://your-app-link.streamlit.app) <!-- Replace with your Streamlit Cloud URL -->

---

## 📊 Dashboard Features

- 💰 **KPI Cards** — Total Revenue, Orders, Avg Order Value, Delivery Rate
- 📈 **Monthly Revenue vs Orders** — Dual-axis line + bar chart
- 🎯 **Order Status Breakdown** — Donut chart (Delivered, Returned, Cancelled, Refunded)
- 👥 **Sales by Gender** — Men vs Women comparison
- 🛒 **Channel Contribution** — Amazon, Flipkart, Myntra, Ajio, Meesho, Nalli, Others
- 📍 **Top 10 States by Revenue** — Geographic sales performance
- 🎂 **Age Group & Gender Analysis** — Who buys the most?
- 👗 **Category-wise Revenue** — Kurta, Set, Saree, Top, Western Dress, etc.
- 🔎 **Interactive Filters** — Filter by Month, Channel, Category, Gender

---

## 🗂️ Project Structure

```
vrinda-store-dashboard/
│
├── app.py                          ← Main Streamlit application
├── requirements.txt                ← Python dependencies
├── README.md                       ← Project documentation
└── data/
    └── vrinda_store_cleaned.csv    ← Cleaned dataset (processed from Excel)
```

---

## 🧹 Data Cleaning Steps

The raw Excel file had the following issues which were fixed:

| Issue | Fix |
|-------|-----|
| Gender values `W` and `M` | Replaced with `Women` and `Men` |
| Qty values `One` / `Two` (text) | Converted to numeric `1` / `2` |
| Column name `Channel ` had trailing space | Stripped and renamed |
| `ship-city`, `ship-state` formatting | Renamed to clean snake_case |
| No Month column | Extracted `Month` and `Month_Num` from `Date` |
| No Age Group column | Created bins: Teenager, Young Adult, Adult, Senior |
| Redundant columns (`currency`, `index`, `ship-country`) | Dropped |

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/noorthisis/vrinda-store-dashboard.git
cd vrinda-store-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Pandas | Data cleaning & analysis |
| Streamlit | Web app framework |
| Plotly | Interactive charts |

---

## 📁 Dataset

- **Source:** Kaggle — Vrinda Store Annual Sales Data
- **Year:** 2022
- **Records:** 31,047 orders
- **Channels:** Amazon, Flipkart, Myntra, Ajio, Meesho, Nalli, Others

---

## 👩‍💻 Author

**Noor (Shabnoor)**  
BCA — AI & Data Science | Graphic Era University, Dehradun  
🔗 [GitHub: noorthisis](https://github.com/noorthisis)
