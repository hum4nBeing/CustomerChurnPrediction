import streamlit as st
from utils import load_data
from components.sidebar import filter_data
from components.metrics import display_summary_metrics, download_filtered_data
from components.plots import (
    plot_churn_distribution, plot_tenure_boxplot, plot_monthly_charges_histogram,
    plot_tenure_vs_charges, plot_payment_method_breakdown, plot_contract_churn,
    plot_sunburst_chart, plot_internet_service_donut, expander_explanation,
    plot_null_values_heatmap, plot_senior_vs_churn, plot_partner_dependents_vs_churn,
    plot_gender_vs_churn, plot_service_usage_vs_churn, plot_paperlessbilling_vs_churn,
    plot_totalcharges_boxplot, plot_scatter_matrix, plot_kmeans_clusters
)
from components.insights import insights_tab
from components.prediction import prediction_form
from components.about import about_tab

# Configure the main page layout and settings
st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Apply custom CSS styling for UI enhancements
    st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        color: #4A90E2;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #555555;
        text-align: center;
        margin-bottom: 2rem;
    }
    div[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">🔮 Customer Churn Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Explore key insights and predict customer churn with interactive visualizations</div>', unsafe_allow_html=True)
    st.divider()

    # Fetch dataset and apply global filters only once
    data = load_data()
    filtered_data = filter_data(data)

    # Initialize application tabs with descriptive icons
    tabs = st.tabs(["🏠 Overview", "📊 Insights", "🔮 Prediction", "ℹ️ About"])

    # --- Section: Dashboard Overview ---
    with tabs[0]:
        st.header("🏠 Overview")
        display_summary_metrics(filtered_data)
        download_filtered_data(filtered_data)
        
        st.subheader("General Visualizations")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_churn_distribution(filtered_data), use_container_width=True, key="plot_churn_distribution")
            with st.expander("About Churn Distribution"):
                st.markdown(expander_explanation("churn_distribution"))
            st.plotly_chart(plot_tenure_boxplot(filtered_data), use_container_width=True, key="plot_tenure_boxplot")
            with st.expander("About Tenure Distribution"):
                st.markdown(expander_explanation("tenure_boxplot"))
        with col2:
            st.plotly_chart(plot_monthly_charges_histogram(filtered_data), use_container_width=True, key="plot_monthly_charges_histogram")
            with st.expander("About Monthly Charges Distribution"):
                st.markdown(expander_explanation("monthly_charges"))
            st.plotly_chart(plot_tenure_vs_charges(filtered_data), use_container_width=True, key="plot_tenure_vs_charges")
            with st.expander("About Tenure vs. Monthly Charges"):
                st.markdown(expander_explanation("tenure_vs_charges"))
        
        st.markdown("### Additional Visualizations")
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(plot_payment_method_breakdown(filtered_data), use_container_width=True, key="plot_payment_method_breakdown")
            with st.expander("About Payment Method Breakdown"):
                st.markdown(expander_explanation("payment_method"))
        with col4:
            st.plotly_chart(plot_contract_churn(filtered_data), use_container_width=True, key="plot_contract_churn")
            with st.expander("About Churn by Contract"):
                st.markdown(expander_explanation("contract_churn"))
        
        st.plotly_chart(plot_sunburst_chart(filtered_data), use_container_width=True, key="plot_sunburst_chart_1")
        with st.expander("About Customer Segmentation"):
            st.markdown(expander_explanation("sunburst"))
        
        st.plotly_chart(plot_internet_service_donut(filtered_data), use_container_width=True, key="plot_internet_service_donut")
        with st.expander("About Internet Service Usage"):
            st.markdown(expander_explanation("internet_service"))
        
        st.subheader("Data Preview")
        st.dataframe(filtered_data.head(20))
        
        st.markdown("## Category-Based Analysis")
        # 1. Initial Data Inspection and Understanding
        with st.expander("🧩 Dataset Understanding and Initial Exploration"):
            st.info("Checking for missing values:")
            null_fig = plot_null_values_heatmap(filtered_data)
            if null_fig:
                st.plotly_chart(null_fig, use_container_width=True, key="plot_null_values_heatmap")
            else:
                st.info("No missing values detected.")
        
        # 2. Demographics Overview
        with st.expander("🔍 Demographic Analysis"):
            st.plotly_chart(plot_gender_vs_churn(filtered_data), use_container_width=True, key="plot_gender_vs_churn")
            st.plotly_chart(plot_senior_vs_churn(filtered_data), use_container_width=True, key="plot_senior_vs_churn")
            st.plotly_chart(plot_partner_dependents_vs_churn(filtered_data), use_container_width=True, key="plot_partner_dependents_vs_churn")
        
        # 3. Customer Services and Subscription Options
        with st.expander("📶 Service Usage and Subscription Type"):
            st.plotly_chart(plot_service_usage_vs_churn(filtered_data), use_container_width=True, key="plot_service_usage_vs_churn")
        
        # 4. Analysis of Tenure and Billing Patterns
        with st.expander("💰 Tenure and Payment Patterns"):
            fig_pb = plot_paperlessbilling_vs_churn(filtered_data)
            if fig_pb:
                st.plotly_chart(fig_pb, use_container_width=True, key="plot_paperlessbilling_vs_churn")
            else:
                st.info("No 'PaperlessBilling' column found.")
            fig_total = plot_totalcharges_boxplot(filtered_data)
            if fig_total:
                st.plotly_chart(fig_total, use_container_width=True, key="plot_totalcharges_boxplot")
            else:
                st.info("No 'TotalCharges' data available.")
            st.plotly_chart(plot_scatter_matrix(filtered_data), use_container_width=True, key="plot_scatter_matrix")
        
        # 5. Feature Importance and Correlation Measures
        with st.expander("📈 Correlations and Feature Importance"):
            # Scatter matrix provided here (correlation heatmap is in Insights tab).
            st.plotly_chart(plot_scatter_matrix(filtered_data), use_container_width=True, key="plot_scatter_matrix_2")
        
        # 6. Customer Clustering and Segmentation
        with st.expander("🧠 Segment-Based Analysis"):
            st.plotly_chart(plot_kmeans_clusters(filtered_data), use_container_width=True, key="plot_kmeans_clusters")
    
    # --- Section: Deep Insights ---
    with tabs[1]:
        insights_tab(filtered_data)

    # --- Section: Real-time Prediction ---
    with tabs[2]:
        st.header("🔮 Prediction")
        st.markdown("Enter customer details below to predict churn using our trained model.")
        prediction_form()

    # --- Section: About the App ---
    with tabs[3]:
        about_tab()
if __name__ == "__main__":
    main()