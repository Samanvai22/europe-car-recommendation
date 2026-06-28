import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# 1. Page Configuration and Styling
st.set_page_config(page_title="Europe Car Recommendation System", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1e1e24 !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
        color: #ffffff !important;
    }
    div[data-baseweb="select"] * {
        color: #111111 !important;
    }
    input {
        color: #111111 !important;
    }
    .car-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px 10px 0px 0px;
        margin-bottom: 0px;
        border-left: 5px solid #ff4b4b;
        color: #111111;
    }
    .car-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 2px;
    }
    .car-subtitle {
        font-size: 16px;
        color: #555555;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Database Connection Setup
USER = 'admin'
PASSWORD = 'Carproject123!'
ENDPOINT = 'car-database.c5cgsak2a4rq.eu-north-1.rds.amazonaws.com'
DB_NAME = 'car_db'

@st.cache_data
def load_data_from_rds():
    safe_password = urllib.parse.quote_plus(PASSWORD)
    connection_string = f"mysql+pymysql://{USER}:{safe_password}@{ENDPOINT}:3306/{DB_NAME}"
    engine = create_engine(connection_string)
    query = "SELECT * FROM cars"
    df = pd.read_sql(query, con=engine)
    return df

try:
    df = load_data_from_rds()
except Exception as e:
    st.error(f"Database connection failed: {e}")
    df = pd.DataFrame()

# 3. Premium Title Banner with Background
st.markdown("""
    <div style="
        background-image: url('https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=1600&q=80');
        background-size: cover;
        background-position: center;
        padding: 50px 30px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: inset 0 0 0 2000px rgba(0,0,0,0.65);
    ">
        <h1 style="color: white; font-weight: 800; font-size: 3rem; margin: 0;">🚗 Europe Car Recommendation System</h1>
        <p style="color: #e0e0e0; font-size: 1.2rem; margin-top: 10px; font-weight: 400;">Find your perfect brand-new vehicle based on budget, fuel type, transmission, and performance.</p>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # Sidebar Filtering Controls
    st.sidebar.header("Filter Options")
    
    search_query = st.sidebar.text_input("🔍 Search Models (e.g., M3, GT-R, Manual):")
    
    makes = ['All'] + sorted(df['Make'].unique().tolist())
    selected_make = st.sidebar.selectbox("Select Brand", makes)
    
    min_price = int(df['Price'].min())
    max_price = int(df['Price'].max())
    selected_price = st.sidebar.slider("Maximum Price (€)", min_price, max_price, max_price)
    
    fuel_types = ['All'] + sorted(df['Fuel_Type'].unique().tolist())
    selected_fuel = st.sidebar.selectbox("Fuel Type", fuel_types)

    transmissions = ['All'] + sorted(df['Transmission'].unique().tolist())
    selected_transmission = st.sidebar.selectbox("Transmission", transmissions)

    if selected_make == 'All' and not search_query and selected_fuel == 'All' and selected_transmission == 'All' and selected_price == max_price:
        st.info("👋 Welcome! Use the options or search bar in the left sidebar to discover your perfect high-performance or electric match.")
    else:
        filtered_df = df.copy()
        
        if search_query:
            filtered_df = filtered_df[
                filtered_df['Make'].str.contains(search_query, case=False, na=False) |
                filtered_df['Model'].str.contains(search_query, case=False, na=False) | 
                filtered_df['Variant'].str.contains(search_query, case=False, na=False)
            ]
        if selected_make != 'All':
            filtered_df = filtered_df[filtered_df['Make'] == selected_make]
        if selected_fuel != 'All':
            filtered_df = filtered_df[filtered_df['Fuel_Type'] == selected_fuel]
        if selected_transmission != 'All':
            filtered_df = filtered_df[filtered_df['Transmission'] == selected_transmission]
            
        filtered_df = filtered_df[filtered_df['Price'] <= selected_price]

        st.subheader(f"Found {len(filtered_df)} Matching Variants")
        
        if filtered_df.empty:
            st.warning("No vehicles match your specific combination of filters.")
        else:
            # Model-Specific Image Dictionary with exact M-Series images
            model_images = {
                'Mustang': 'https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?w=800',
                'GT-R': 'https://images.unsplash.com/photo-1604064344445-568b2fa41898?w=800',
                'M3': 'https://images.unsplash.com/photo-1607853202273-797f1c22a38e?w=800', # Exact M3
                'M4': 'https://images.unsplash.com/photo-1617531653332-bd46c24f2068?w=800', # Exact M4
                'M5': 'https://images.unsplash.com/photo-1556189250-72ba007cf7da?w=800', # Exact M5
                'Golf': 'https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=800',
                'Civic': 'https://images.unsplash.com/photo-1604164448130-d1df213c64eb?w=800',
                'Corvette': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800',
                '911': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800',
                'Taycan': 'https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=800',
                'RS3': 'https://images.unsplash.com/photo-1542282088-fe8426682b8f?w=800',
                'RS4': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800',
                'RS5': 'https://images.unsplash.com/photo-1612825173281-9a193378527e?w=800',
                'Model 3': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800',
                'Model Y': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800',
                'Model S': 'https://images.unsplash.com/photo-1618013083162-ce28014dd58d?w=800',
                'G-Class': 'https://images.unsplash.com/photo-1520031441872-265e4ff70366?w=800'
            }

            brand_fallback_images = {
                'Audi': 'https://images.unsplash.com/photo-1542282088-fe8426682b8f?w=800',
                'BMW': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800',
                'Tesla': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800',
                'Mercedes-Benz': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800',
                'Porsche': 'https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=800',
                'Toyota': 'https://images.unsplash.com/photo-1629897048514-3dd74142fbce?w=800',
                'Honda': 'https://images.unsplash.com/photo-1604164448130-d1df213c64eb?w=800',
                'Ford': 'https://images.unsplash.com/photo-1551830820-330a71b99659?w=800',
                'Volkswagen': 'https://images.unsplash.com/photo-1622200294736-2ebac8665dd9?w=800',
                'Hyundai': 'https://images.unsplash.com/photo-1671520330663-e381b1dd089d?w=800',
                'Nissan': 'https://images.unsplash.com/photo-1602426328842-12f5a0ce5e97?w=800',
                'Chevrolet': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800',
                'Lucid': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800',
                'Rivian': 'https://images.unsplash.com/photo-1669022634351-4b1ba7d566e5?w=800'
            }
            fallback_img = 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800'

            for index, car in filtered_df.iterrows():
                
                # Render the Car Card WITHOUT the Year
                st.markdown(f"""
                <div class="car-card">
                    <div class="car-title">{car['Make']} {car['Model']}</div>
                    <div class="car-subtitle">{car['Variant']} • {car['Fuel_Type']} • {car['Transmission']}</div>
                    <h3 style='color: #ff4b4b !important; margin-top: 0; margin-bottom: 5px;'>€{car['Price']:,}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                car_make = car['Make']
                car_model = car['Model']
                
                if car_model in model_images:
                    image_url = model_images[car_model]
                else:
                    image_url = brand_fallback_images.get(car_make, fallback_img)
                    
                st.image(image_url, use_container_width=True)

                col1, col2 = st.columns(2)
                
                with col1:
                    kml_val = round(float(car['Fuel_Economy']) * 0.4251, 1)
                    st.write(f"⛽ **Fuel Efficiency:** {kml_val} km/L")
                    st.progress(min(kml_val / 60.0, 1.0))
                    
                with col2:
                    acc_val = float(car['Acceleration_0_100'])
                    st.write(f"⚡ **0-100 km/h Sprint:** {acc_val} seconds")
                    st.progress(max(0.0, min((10.0 - acc_val) / 10.0, 1.0)))
                
                st.markdown("<br><hr style='border-top: 1px dashed #bbb;'>", unsafe_allow_html=True)
else:
    st.warning("No data found. Please check your database connection.")
