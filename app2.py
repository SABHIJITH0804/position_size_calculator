import streamlit as st

st.set_page_config(
    page_title="Professional Position Size Calculator",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Professional Position Size Calculator")

st.markdown("---")

# =====================================================
# Persistent Variables
# =====================================================

if "capital" not in st.session_state:
    st.session_state.capital = 100000.0

if "risk" not in st.session_state:
    st.session_state.risk = 1000.0

if "margin_mode" not in st.session_state:
    st.session_state.margin_mode = "Delivery"

if "custom_margin" not in st.session_state:
    st.session_state.custom_margin = 25.0

# =====================================================
# Account Settings
# =====================================================

st.subheader("💰 Account Settings")

capital = st.number_input(
    "Account Capital (₹)",
    min_value=1000.0,
    step=1000.0,
    key="capital"
)

risk_amount = st.number_input(
    "Maximum Risk Per Trade (₹)",
    min_value=1.0,
    step=100.0,
    key="risk"
)

st.markdown("---")

# =====================================================
# Margin Settings
# =====================================================

st.subheader("📊 Margin Settings")

margin_mode = st.selectbox(
    "Margin Type",
    ["Delivery", "Intraday", "Custom"],
    key="margin_mode"
)

if margin_mode == "Custom":
    custom_margin = st.number_input(
        "Custom Margin (%)",
        min_value=1.0,
        max_value=100.0,
        step=1.0,
        key="custom_margin"
    )

st.markdown("---")

# =====================================================
# Trade Inputs
# =====================================================

st.subheader("📈 Trade Details")

entry = st.number_input(
    "Entry Price",
    min_value=0.0,
    format="%.2f"
)

sl = st.number_input(
    "Stop Loss Price",
    min_value=0.0,
    format="%.2f"
)

# =====================================================
# Calculations
# =====================================================

if entry > 0 and sl > 0:

    sl_points = abs(entry - sl)

    if sl_points == 0:
        st.error("Entry Price and Stop Loss Price cannot be the same.")

    else:

        # --------------------------
        # Margin %
        # --------------------------

        if margin_mode == "Delivery":
            margin_percent = 100

        elif margin_mode == "Intraday":
            margin_percent = 25

        else:
            margin_percent = st.session_state.custom_margin

        margin_per_share = entry * (margin_percent / 100)

        # --------------------------
        # Quantities
        # --------------------------

        qrisk = risk_amount / sl_points

        qcapital = capital / entry

        qmargin = capital / margin_per_share

        tradable_qty = int(min(qrisk, qcapital, qmargin))

        # --------------------------
        # Other Calculations
        # --------------------------

        investment = tradable_qty * entry

        margin_required = tradable_qty * margin_per_share

        actual_risk = tradable_qty * sl_points

        capital_utilization = (investment / capital) * 100

        remaining_capital = capital - investment

        # =====================================================
        # Results
        # =====================================================

        st.markdown("---")

        st.subheader("📊 Position Sizing")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Stop Loss Points", f"{sl_points:.2f}")
            st.metric("Risk Quantity", f"{int(qrisk)}")

        with c2:
            st.metric("Capital Quantity", f"{int(qcapital)}")
            st.metric("Margin Quantity", f"{int(qmargin)}")

        st.markdown("### ✅ Final Tradable Quantity")

        st.success(f"{tradable_qty} Shares")

        st.markdown("---")

        st.subheader("📋 Trade Summary")

        st.write(f"**Entry Price :** ₹ {entry:,.2f}")

        st.write(f"**Stop Loss Price :** ₹ {sl:,.2f}")

        st.write(f"**Margin Type :** {margin_mode}")

        st.write(f"**Margin Percentage :** {margin_percent:.0f}%")

        st.write(f"**Margin Per Share :** ₹ {margin_per_share:,.2f}")

        st.write(f"**Investment Required :** ₹ {investment:,.2f}")

        st.write(f"**Margin Required :** ₹ {margin_required:,.2f}")

        st.write(f"**Actual Risk :** ₹ {actual_risk:,.2f}")

        st.write(f"**Capital Utilized :** {capital_utilization:.2f}%")

        st.write(f"**Remaining Capital :** ₹ {remaining_capital:,.2f}")
