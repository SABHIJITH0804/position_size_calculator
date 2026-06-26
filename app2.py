import streamlit as st

st.set_page_config(
    page_title="Position Size Calculator",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Professional Position Size Calculator")

st.markdown("---")

# -------------------------
# Persistent Inputs
# -------------------------

if "capital" not in st.session_state:
    st.session_state.capital = 100000.0

if "risk" not in st.session_state:
    st.session_state.risk = 1000.0

st.subheader("Account Settings")

capital = st.number_input(
    "Account Capital (₹)",
    min_value=1000.0,
    value=st.session_state.capital,
    step=1000.0,
    key="capital"
)

risk_amount = st.number_input(
    "Maximum Risk Per Trade (₹)",
    min_value=1.0,
    value=st.session_state.risk,
    step=100.0,
    key="risk"
)

st.markdown("---")

# -------------------------
# Trade Inputs
# -------------------------

st.subheader("Trade Details")

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

# -------------------------
# Calculations
# -------------------------

if entry > 0 and sl > 0:

    sl_points = abs(entry - sl)

    if sl_points == 0:
        st.error("Entry and Stop Loss cannot be the same.")

    else:

        qrisk = risk_amount / sl_points

        qcapital = capital / entry

        tradable_qty = int(min(qrisk, qcapital))

        investment = tradable_qty * entry

        actual_risk = tradable_qty * sl_points

        utilisation = (investment / capital) * 100

        st.markdown("---")
        st.subheader("Results")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Stop Loss Points", f"{sl_points:.2f}")
            st.metric("Risk Quantity", f"{int(qrisk)}")

        with c2:
            st.metric("Capital Quantity", f"{int(qcapital)}")
            st.metric("Tradable Quantity", f"{tradable_qty}")

        st.markdown("---")

        st.success("Trade Summary")

        st.write(f"**Investment Required :** ₹ {investment:,.2f}")

        st.write(f"**Actual Risk :** ₹ {actual_risk:,.2f}")

        st.write(f"**Capital Utilized :** {utilisation:.2f}%")

        remaining = capital - investment

        st.write(f"**Remaining Capital :** ₹ {remaining:,.2f}")