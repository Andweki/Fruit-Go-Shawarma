import streamlit as st
from datetime import datetime
import requests

# ── Configuration ────────────────────────────────────────────────────────────
st.set_page_config(page_title="Bird House Fast Food", page_icon="🍔", layout="centered")

# STEP 1: Paste your Apps Script Web App URL here after deploying it.
# See the SETUP INSTRUCTIONS comment at the bottom of this file.
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzaQONC37PtylDCjNyXBBQvAWxhazoFqwtEcW7D--ekVFvn74T2x8WMYEHRiO9Ph5IZ/exec"

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #fffdf8; }
    .menu-card {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-left: 4px solid #e8452c;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .menu-item { font-size: 1.05rem; font-weight: 600; color: #1a1a1a; margin: 0; }
    .menu-price { font-size: 1rem; color: #e8452c; font-weight: 700; margin: 4px 0 0 0; }
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a1a;
        border-bottom: 2px solid #e8452c;
        padding-bottom: 6px;
        margin: 24px 0 16px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🍔 Local Bites Fast Food")
st.markdown("**Fresh, fast, and delivered straight to your door!**")
st.markdown("---")

# ── Menu ─────────────────────────────────────────────────────────────────────
menu = {
    "Classic Shawarma ":        300,
    "Hot Dogs":                 150,
    "Loaded Cheese Fries":      200,
    "Kienyeji Chicken":        2000,
    "Beef Sausage pair":        150,
    "Fresh Juices (500ml)":     200,
}

st.markdown('<p class="section-header">📜 Our Menu</p>', unsafe_allow_html=True)

cols = st.columns(2)
for i, (item, price) in enumerate(menu.items()):
    with cols[i % 2]:
        st.markdown(f"""
        <div class="menu-card">
            <p class="menu-item">{item}</p>
            <p class="menu-price">KSh {price:,}</p>
        </div>
        """, unsafe_allow_html=True)

# ── Order Form ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">🛒 Place Your Order</p>', unsafe_allow_html=True)

with st.form("order_form", clear_on_submit=True):
    customer_name    = st.text_input("Full Name *",                   placeholder="John Doe")
    phone_number     = st.text_input("Phone Number *",                placeholder="0712 345 678")
    delivery_address = st.text_area( "Delivery Address / Landmark *", placeholder="Apartment B4, Stage")

    st.markdown("#### Select Items")
    selected_item        = st.selectbox("Choose your main dish *", list(menu.keys()))
    quantity             = st.number_input("Quantity", min_value=1, max_value=10, value=1)
    special_instructions = st.text_input("Special Instructions (e.g., No onions)")

    submit_button = st.form_submit_button("✅ Confirm & Order", use_container_width=True)

# ── Order Processing ──────────────────────────────────────────────────────────
if submit_button:
    if not customer_name or not phone_number or not delivery_address:
        st.error("⚠️ Please fill in all required fields marked with *")
    elif APPS_SCRIPT_URL == "YOUR_APPS_SCRIPT_URL_HERE":
        st.warning("⚙️ **Setup needed:** Paste your Apps Script URL into `APPS_SCRIPT_URL` in the code. See the instructions below.")
    else:
        item_price   = menu[selected_item]
        total_cost   = item_price * quantity
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [
            current_time,
            customer_name,
            phone_number,
            delivery_address,
            selected_item,
            quantity,
            total_cost,
            special_instructions or "None",
        ]

        try:
            response = requests.post(
                APPS_SCRIPT_URL,
                json={"row": row},
                timeout=15,
            )
            if response.status_code == 200 and response.text.strip() == "OK":
                st.success(f"🎉 Order received, {customer_name}!")
                st.markdown(f"""
                ### 📋 Order Summary
                | Detail | Info |
                |---|---|
                | 🍽️ Item | {selected_item} × {quantity} |
                | 💵 Total | **KSh {total_cost:,}** |
                | 📍 Deliver to | {delivery_address} |
                | 📞 We'll call | {phone_number} |
                """)
                st.info("⏰ We'll call you within 5 minutes to confirm your order!")
            else:
                st.error(f"❌ Unexpected response from server: `{response.text}`")

        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Check your Apps Script URL and try again.")
        except Exception as e:
            st.error("❌ Failed to save order.")
            st.caption(f"Error: {e}")

# ── Setup Instructions ────────────────────────────────────────────────────────
with st.expander("⚙️ First-time Setup Instructions (click to expand)"):
    st.markdown("""
    ### How to connect your Google Sheet (one-time setup)

    **Step 1 — Add the Apps Script to your Sheet**
    1. Open your Google Sheet
    2. Click **Extensions → Apps Script**
    3. Delete any existing code and paste this:

    ```javascript
    function doPost(e) {
      const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
      const data = JSON.parse(e.postData.contents);
      sheet.appendRow(data.row);
      return ContentService.createTextOutput("OK");
    }
    ```

    4. Click **Save** (💾)

    **Step 2 — Deploy it as a Web App**
    1. Click **Deploy → New deployment**
    2. Click the gear icon ⚙️ next to "Type" and select **Web app**
    3. Set description to anything (e.g. "Order receiver")
    4. Set **Execute as:** `Me`
    5. Set **Who has access:** `Anyone`
    6. Click **Deploy**
    7. Click **Authorize access** and follow the prompts
    8. Copy the **Web app URL** shown at the end

    **Step 3 — Paste the URL into this file**

    Replace `YOUR_APPS_SCRIPT_URL_HERE` at the top of `app.py` with your copied URL.

    That's it — orders will now write directly to your sheet!
    """)