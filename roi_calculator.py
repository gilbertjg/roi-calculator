
import streamlit as st

# --- Title ---
st.title("🏡 Real Estate Cash-on-Cash ROI Calculator")
st.caption("Compare Long-Term vs Short-Term Rental Performance")

# --- Inputs ---
st.header("🔢 Property Details")
purchase_price = st.number_input("Purchase Price ($)", value=260000)
down_payment_pct = st.slider("Down Payment (%)", 0, 100, 20)
closing_costs = st.number_input("Estimated Closing Costs ($)", value=6000)
loan_term = st.slider("Loan Term (Years)", 5, 40, 30)
interest_rate = st.slider("Interest Rate (%)", 0.0, 15.0, 7.0)

st.header("📈 Monthly Income")
ltr_rent = st.number_input("LTR Rent ($/month)", value=1850)
str_rent = st.number_input("STR Avg Net Income ($/month)", value=3250)

st.header("🧾 Monthly Expenses")
taxes_annual = st.number_input("Property Taxes ($/year)", value=4500)
insurance_annual = st.number_input("Insurance ($/year)", value=1800)
mgmt_pct = st.slider("Property Management Fee (%)", 0, 30, 10)
maintenance = st.number_input("Maintenance ($/month)", value=150)

# --- Calculations ---
down_payment = purchase_price * (down_payment_pct / 100)
loan_amount = purchase_price - down_payment
monthly_interest = (interest_rate / 100) / 12
n_payments = loan_term * 12

monthly_mortgage = loan_amount * (monthly_interest * (1 + monthly_interest)**n_payments) / ((1 + monthly_interest)**n_payments - 1)

monthly_taxes = taxes_annual / 12
monthly_insurance = insurance_annual / 12

def calc_net_income(rent):
    mgmt_fee = rent * (mgmt_pct / 100)
    total_expenses = monthly_mortgage + monthly_taxes + monthly_insurance + maintenance + mgmt_fee
    return rent - total_expenses

ltr_net = calc_net_income(ltr_rent)
str_net = calc_net_income(str_rent)

ltr_annual = ltr_net * 12
str_annual = str_net * 12

total_cash_invested = down_payment + closing_costs

roi_ltr = (ltr_annual / total_cash_invested) * 100
roi_str = (str_annual / total_cash_invested) * 100

# --- Output ---
st.header("📊 Results")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Long-Term Rental")
    st.metric("Net Monthly Income", f"${ltr_net:,.2f}")
    st.metric("Annual Net", f"${ltr_annual:,.2f}")
    st.metric("Cash-on-Cash ROI", f"{roi_ltr:.2f}%" if roi_ltr >= 0 else "Negative")

with col2:
    st.subheader("Short-Term Rental")
    st.metric("Net Monthly Income", f"${str_net:,.2f}")
    st.metric("Annual Net", f"${str_annual:,.2f}")
    st.metric("Cash-on-Cash ROI", f"{roi_str:.2f}%" if roi_str >= 0 else "Negative")

# Footer
st.markdown("---")
st.markdown("---")
st.image("Headshot.jpg", width=160, caption="Created by Gilbert J. Realtor – RE/MAX Elite", use_container_width=False)

st.markdown("📬 **Connect with me:**")
st.markdown(
    """
    🔗 [Properties For You](https://gilbertjrealtor.com)  
    📸 [Instagram](https://instagram.com/gilbertj.realtor)  
    💼 [LinkedIn](https://linkedin.com/in/gilbertjg)  
    """,
    unsafe_allow_html=True
)


