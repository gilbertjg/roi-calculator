import smtplib
from email.mime.text import MIMEText
import streamlit as st

# --- Initialize session state ---
query_params = st.experimental_get_query_params()

# Always initialize first
if "show_calculator" not in st.session_state:
    st.session_state["show_calculator"] = False

if "user_info" not in st.session_state:
    st.session_state["user_info"] = {}

# Load from query params if present
if not st.session_state["user_info"] and query_params.get("name") and query_params.get("email"):
    st.session_state["user_info"] = {
        "name": query_params.get("name", [""])[0],
        "email": query_params.get("email", [""])[0],
        "phone": query_params.get("phone", [""])[0],
    }

# Access flag override
if query_params.get("access", [""])[0] == "true":
    st.session_state["show_calculator"] = True

# --- Contact Form ---
if not st.session_state["show_calculator"]:
    st.header("📬 Contact Info to Access the Calculator")

    with st.form("contact_form"):
        name = st.text_input("Name", value=st.session_state["user_info"].get("name", ""))
        email = st.text_input("Email", value=st.session_state["user_info"].get("email", ""))
        phone = st.text_input("Phone Number (optional)", value=st.session_state["user_info"].get("phone", ""))
        submitted = st.form_submit_button("Enter")

    def send_email_to_zapier(name, email, phone):
        try:
            parts = name.strip().split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

            message = (
                f"New ROI Calculator Lead\n"
                f"Name: {first_name} {last_name}\n"
                f"Email: {email}\n"
                f"Phone: {phone or 'N/A'}"
            )

            msg = MIMEText(message)
            msg["Subject"] = "New ROI Calculator Lead"
            msg["From"] = "gilbertjrealtor@gmail.com"
            msg["To"] = "r3vxhw4r@robot.zapier.com"

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login("gilbertjrealtor@gmail.com", "hlaxsolttsziezyk")
                server.send_message(msg)
            return True
        except Exception as e:
            st.error(f"⚠️ Error sending lead to CRM: {e}")
            return False

    if submitted:
        if name and email:
            success = send_email_to_zapier(name, email, phone)
            if success:
                st.session_state["user_info"] = {"name": name, "email": email, "phone": phone}
                st.session_state["show_calculator"] = True
                st.experimental_set_query_params(
                    access="true",
                    name=name,
                    email=email,
                    phone=phone
                )
                st.success("✅ Thanks! Launching the calculator now...")
                st.rerun()
        else:
            st.warning("Please enter both name & email to proceed.")
            st.stop()


# --- Main Calculator ---
if st.session_state["show_calculator"] or st.session_state["user_info"]:
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

    # --- Footer ---
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

    # Optional: Reset button to clear session
    if st.button("🔄 Reset Contact Info"):
        st.session_state.user_info = {}
        st.session_state.show_calculator = False
        st.rerun()
