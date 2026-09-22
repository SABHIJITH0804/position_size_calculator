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
    st.session_state.capital = 50000.0

if "risk" not in st.session_state:
    st.session_state.risk = 200.0

if "margin_mode" not in st.session_state:
    st.session_state.margin_mode = "Intraday"

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

trade_type = st.selectbox(
    "Trade Direction",
    ["Buy", "Sell"]
)

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

atr = st.number_input(
    "ATR",
    min_value=0.0,
    format="%.2f"
)

# =====================================================
# Calculations
# =====================================================

if entry > 0 and sl > 0:

    sl_points = abs(entry - sl)

    sl_50_points = (entry * 0.5)/100

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

        # --------------------------
        # Targets
        # --------------------------
        # ------------------------------------------------
        # ATR Based Percentage
        # ------------------------------------------------

        if margin_mode == "Intraday":
            atr_multiplier = 1.5

        elif margin_mode == "Delivery":
            atr_multiplier = 2.0

        else:
            # Custom margin doesn't imply a trade style, so use the intraday multiplier by default.
            atr_multiplier = 1.5

        atr_percent = ((atr * atr_multiplier) / entry) * 100

        atr_points = (atr_percent / 100) * entry
        
        if trade_type == "Buy":
            t1 = entry + sl_points
            t15 = entry + (sl_points * 1.5)
            t2 = entry + (sl_points * 2)
            t25 = entry + (sl_points * 2.5)
            t3 = entry + (sl_points * 3)
            t35 = entry + (sl_points * 3.5)
            t4 = entry + (sl_points * 4)
            t45 = entry + (sl_points * 4.5)
            t5 = entry + (sl_points * 5)
            t55 = entry + (sl_points * 5.5)
            t6 = entry + (sl_points * 6)
            t65 = entry + (sl_points * 6.5)
            t7 = entry + (sl_points * 7)
            t75 = entry + (sl_points * 7.5)
            t8 = entry + (sl_points * 8)
        else:
            t1 = entry - sl_points
            t15 = entry - (sl_points * 1.5)
            t2 = entry - (sl_points * 2)
            t25 = entry - (sl_points * 2.5)
            t3 = entry - (sl_points * 3)
            t35 = entry - (sl_points * 3.5)
            t4 = entry - (sl_points * 4)
            t45 = entry - (sl_points * 4.5)
            t5 = entry - (sl_points * 5)
            t55 = entry - (sl_points * 5.5)
            t6 = entry - (sl_points * 6)
            t65 = entry - (sl_points * 6.5)
            t7 = entry - (sl_points * 7)
            t75 = entry - (sl_points * 7.5)
            t8 = entry - (sl_points * 8)

        # =====================================================
        # Results
        # =====================================================

        st.markdown("---")

        st.subheader("📊 Position Sizing")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                f"{atr_percent:.2f}% of Entry Price",
                f"₹ {atr_points:.2f}"
                )
            st.metric(
                f"{0.50:.2f}% of Entry Price",
                f"₹ {sl_50_points:.2f}"
                )
            st.metric("Stop Loss Points", f"{sl_points:.2f}")
            st.metric("Risk Quantity", f"{int(qrisk)}")

        with c2:
            st.metric("Capital Quantity", f"{int(qcapital)}")
            st.metric("Margin Quantity", f"{int(qmargin)}")

        st.markdown("---")
        st.subheader("🎯 Trade Targets")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                f"{atr_percent:.2f}% of Entry Price",
                f"₹ {atr_points:.2f}"
                )
            st.metric("SL Points", f"{sl_points:.2f}")

        with c2:
            st.metric("T1 (1R)", f"₹ {t1:.2f}")
            st.metric("T1.5 (1.5R)", f"₹ {t15:.2f}")
            st.metric("T2 (2R)", f"₹ {t2:.2f}")
            st.metric("T2.5 (2.5R)", f"₹ {t25:.2f}")
            st.metric("T3 (3R)", f"₹ {t3:.2f}")
            st.metric("T3.5 (3.5R)", f"₹ {t35:.2f}")
            st.metric("T4 (4R)", f"₹ {t4:.2f}")
            st.metric("T4.5 (4.5R)", f"₹ {t45:.2f}")
            st.metric("T5 (5R)", f"₹ {t5:.2f}")
            st.metric("T5.5 (5.5R)", f"₹ {t55:.2f}")
            st.metric("T6 (6R)", f"₹ {t6:.2f}")
            st.metric("T6.5 (6.5R)", f"₹ {t65:.2f}")
            st.metric("T7 (7R)", f"₹ {t7:.2f}")
            st.metric("T7.5 (7.5R)", f"₹ {t75:.2f}")
            st.metric("T8 (8R)", f"₹ {t8:.2f}")

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
