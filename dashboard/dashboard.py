import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Seller Analysis Dashboard", layout="wide")


# Load data
@st.cache_data
def load_data():
    return pd.read_csv('all_data.csv')


# Load the data
all_data = load_data()

# Display the raw data (optional, if you want to show the dataframe)
if st.checkbox("Show raw data"):
    st.write(all_data)

# Bagian 1: Distribusi penjual dan pesanan di berbagai wilayah
st.title("Seller Distribution and Order Fulfillment Analysis")

# Assuming that 'seller_state' and 'order_id' exist in all_data
# Data distribusi penjual dan pesanan
seller_distribution_df = all_data['seller_state'].value_counts().reset_index()
seller_distribution_df.columns = ['seller_state', 'seller_count']

seller_order_count = all_data.groupby('seller_state')['order_id'].count().reset_index()
seller_order_count.columns = ['seller_state', 'order_count']

# Gabungkan data distribusi penjual dan pesanan
combined_df = pd.merge(seller_distribution_df, seller_order_count, on='seller_state')

# Plot distribusi penjual dan pesanan yang dipenuhi
st.subheader("Distribution of Sellers and Orders Fulfilled by Region")
fig1, ax1 = plt.subplots(figsize=(14, 7))

# Plot distribusi seller
sns.barplot(x=combined_df['seller_state'], y=combined_df['seller_count'], palette='viridis', ax=ax1)
ax1.set_xlabel('State')
ax1.set_ylabel('Number of Sellers', color='blue')

# Tambahkan axis kedua untuk jumlah pesanan yang dipenuhi
ax2 = ax1.twinx()
sns.lineplot(x=combined_df['seller_state'], y=combined_df['order_count'], color='red', marker='o', ax=ax2)
ax2.set_ylabel('Number of Orders Fulfilled', color='red')

plt.title('Distribution of Sellers and Orders Fulfilled by Region')
st.pyplot(fig1)

# Bagian 2: Pengaruh lokasi penjual terhadap waktu pengiriman dan kepuasan pelanggan
st.title("Seller Location Impact on Shipping Time and Customer Satisfaction")

# Assuming 'delivery_time' and 'review_score' exist in all_data
# Data waktu pengiriman dan kepuasan pelanggan
shipping_times = all_data.groupby('seller_state')['delivery_time'].mean().reset_index()
customer_satisfaction = all_data.groupby('seller_state')['review_score_y'].mean().reset_index()

# Gabungkan data waktu pengiriman dan kepuasan pelanggan
combined_df2 = pd.merge(shipping_times, customer_satisfaction, on='seller_state')

# Plot waktu pengiriman dan kepuasan pelanggan
st.subheader("Average Shipping Time and Customer Satisfaction by Seller Location")
fig2, ax1 = plt.subplots(figsize=(14, 7))

# Plot waktu pengiriman
sns.barplot(x=combined_df2['seller_state'], y=combined_df2['delivery_time'], palette='plasma', ax=ax1)
ax1.set_xlabel('State')
ax1.set_ylabel('Average Shipping Time (days)', color='blue')

# Tambahkan axis kedua untuk kepuasan pelanggan
ax2 = ax1.twinx()
sns.lineplot(x=combined_df2['seller_state'], y=combined_df2['review_score_y'], color='red', marker='o', ax=ax2)
ax2.set_ylabel('Average Review Score', color='red')

plt.title('Average Shipping Time and Customer Satisfaction by Seller Location')
st.pyplot(fig2)

# Bagian 3: Kesimpulan
st.title("Conclusions")
st.markdown("""
**Seller Distribution and Order Fulfillment:**
- The distribution of sellers across regions varies significantly.
- Some regions have more sellers and, generally, fulfill more orders. However, certain regions with fewer sellers still manage to fulfill a large number of orders.

**Shipping Time and Customer Satisfaction:**
- Seller location impacts shipping time significantly, and generally, faster shipping times lead to higher customer satisfaction.
- However, there are exceptions where longer shipping times don't necessarily correlate with lower satisfaction, suggesting other factors such as product quality or customer service may also influence reviews.
""")
