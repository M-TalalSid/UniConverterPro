import streamlit as st
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="UniConvert Pro",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Updated CSS with enhanced visibility for sidebar sections
def local_css():
    css = """
    <style>
    .stApp {
        background-color: #f8f9fa;
        color: #333333;
    }
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .stButton > button {
        background-color: #6C63FF;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
    }
    .result-display {
        background: linear-gradient(135deg, #6C63FF, #FF6584);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: 700;
        margin: 20px 0;
    }
    .history-item {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid #6C63FF;
    }
    .formula-display {
        background-color: white;
        border-left: 5px solid #4CAF50;
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        margin: 15px 0;
    }
    .logo-text {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(45deg, #6C63FF, #FF6584);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    /* Style for expander labels (Basic, Science, Digital) */
    .st-expander > div > div > button > div > p {
        font-size: 1.5rem !important;  /* Larger font size */
        font-weight: 700 !important;   /* Bolder text */
        color: #ffffff !important;     /* White color for contrast */
        background: linear-gradient(90deg, rgba(108, 99, 255, 0.5), rgba(108, 99, 255, 0.3)); /* Gradient background */
        padding: 8px 12px !important;  /* Add padding */
        border-radius: 8px !important; /* Rounded corners */
        margin: 5px 0 !important;      /* Add spacing */
    }
    /* Style for Recent Conversions subheader */
    .stMarkdown h3 {
        font-size: 1.5rem !important;  /* Larger font size */
        font-weight: 700 !important;   /* Bolder text */
        color: #ffffff !important;     /* White color for contrast */
        background: linear-gradient(90deg, rgba(108, 99, 255, 0.5), rgba(108, 99, 255, 0.3)); /* Gradient background */
        padding: 8px 12px !important;  /* Add padding */
        border-radius: 8px !important; /* Rounded corners */
        margin: 10px 0 !important;     /* Add spacing */
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Conversion functions
def convert_length(value, from_unit, to_unit):
    conversions = {
        'meter': 1, 'kilometer': 0.001, 'centimeter': 100, 'millimeter': 1000,
        'inch': 39.3701, 'foot': 3.28084, 'yard': 1.09361, 'mile': 0.000621371,
        'nautical mile': 0.000539957
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_weight(value, from_unit, to_unit):
    conversions = {
        'kilogram': 1, 'gram': 1000, 'milligram': 1e6, 'pound': 2.20462,
        'ounce': 35.274, 'ton': 0.001, 'stone': 0.157473
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'celsius' and to_unit == 'fahrenheit':
        formula = f"({value} × 9/5) + 32"
        return (value * 9/5) + 32, formula
    elif from_unit == 'fahrenheit' and to_unit == 'celsius':
        formula = f"({value} - 32) × 5/9"
        return (value - 32) * 5/9, formula
    elif from_unit == 'celsius' and to_unit == 'kelvin':
        formula = f"{value} + 273.15"
        return value + 273.15, formula
    elif from_unit == 'kelvin' and to_unit == 'celsius':
        formula = f"{value} - 273.15"
        return value - 273.15, formula
    elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
        formula = f"({value} - 32) × 5/9 + 273.15"
        return (value - 32) * 5/9 + 273.15, formula
    elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
        formula = f"({value} - 273.15) × 9/5 + 32"
        return (value - 273.15) * 9/5 + 32, formula
    else:
        return value, "No conversion needed"

def convert_volume(value, from_unit, to_unit):
    conversions = {
        'liter': 1, 'milliliter': 1000, 'cubic meter': 0.001, 'gallon (US)': 0.264172,
        'quart (US)': 1.05669, 'pint (US)': 2.11338, 'cup (US)': 4.22675,
        'fluid ounce (US)': 33.814, 'tablespoon (US)': 67.628, 'teaspoon (US)': 202.884
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_time(value, from_unit, to_unit):
    conversions = {
        'second': 1, 'millisecond': 1000, 'minute': 1/60, 'hour': 1/3600,
        'day': 1/86400, 'week': 1/604800, 'month (30 days)': 1/2592000,
        'year (365 days)': 1/31536000, 'decade': 1/315360000, 'century': 1/3153600000,
        'millennium': 1/31536000000
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_data(value, from_unit, to_unit):
    conversions = {
        'byte': 1, 'kilobyte': 1/1024, 'megabyte': 1/(1024**2), 'gigabyte': 1/(1024**3),
        'terabyte': 1/(1024**4), 'petabyte': 1/(1024**5), 'bit': 8,
        'kibibyte': 1/1024, 'mebibyte': 1/(1024**2), 'gibibyte': 1/(1024**3),
        'tebibyte': 1/(1024**4), 'pebibyte': 1/(1024**5)
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_area(value, from_unit, to_unit):
    conversions = {
        'square meter': 1, 'square kilometer': 0.000001, 'square centimeter': 10000,
        'square millimeter': 1000000, 'square inch': 1550.0031, 'square foot': 10.76391,
        'square yard': 1.19599, 'acre': 0.000247105, 'hectare': 0.0001
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_speed(value, from_unit, to_unit):
    conversions = {
        'meter per second': 1, 'kilometer per hour': 3.6, 'mile per hour': 2.23694,
        'knot': 1.94384, 'foot per second': 3.28084, 'inch per second': 39.3701
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_energy(value, from_unit, to_unit):
    conversions = {
        'joule': 1, 'kilojoule': 0.001, 'calorie': 0.239006, 'kilocalorie': 0.000239006,
        'watt hour': 0.000277778, 'kilowatt hour': 0.000000277778, 'electron volt': 6.242e+18,
        'british thermal unit': 0.000947817
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_pressure(value, from_unit, to_unit):
    conversions = {
        'pascal': 1, 'kilopascal': 0.001, 'megapascal': 0.000001, 'bar': 0.00001,
        'atmosphere': 0.00000986923, 'torr': 0.00750062, 'psi': 0.000145038,
        'millimeter of mercury': 0.00750062
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_power(value, from_unit, to_unit):
    conversions = {
        'watt': 1, 'kilowatt': 0.001, 'megawatt': 0.000001, 'horsepower': 0.00134102,
        'british thermal unit per hour': 3.41214, 'calorie per second': 0.239006
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_frequency(value, from_unit, to_unit):
    conversions = {
        'hertz': 1, 'kilohertz': 0.001, 'megahertz': 0.000001, 'gigahertz': 0.000000001,
        'cycle per second': 1, 'revolution per minute': 60, 'beat per minute': 60
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

# Utility functions
def init_session_state():
    defaults = {
        'history': [],
        'selected_unit': "Length",
        'current_from_unit': None,  # Separate key for tracking the "from" unit
        'current_to_unit': None,    # Separate key for tracking the "to" unit
        'swap_trigger': False       # Flag to trigger swapping
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Main application
def main():
    init_session_state()
    local_css()

    # Define unit categories and their units
    units_dict = {
        "Length": ['meter', 'kilometer', 'centimeter', 'millimeter', 'inch', 'foot', 'yard', 'mile', 'nautical mile'],
        "Weight": ['kilogram', 'gram', 'milligram', 'pound', 'ounce', 'ton', 'stone'],
        "Temperature": ['celsius', 'fahrenheit', 'kelvin'],
        "Volume": ['liter', 'milliliter', 'cubic meter', 'gallon (US)', 'quart (US)', 'pint (US)', 'cup (US)', 
                  'fluid ounce (US)', 'tablespoon (US)', 'teaspoon (US)'],
        "Time": ['second', 'millisecond', 'minute', 'hour', 'day', 'week', 'month (30 days)', 'year (365 days)',
                'decade', 'century', 'millennium'],
        "Data": ['byte', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte', 'petabyte',
                'bit', 'kibibyte', 'mebibyte', 'gibibyte', 'tebibyte', 'pebibyte'],
        "Area": ['square meter', 'square kilometer', 'square centimeter', 'square millimeter',
                'square inch', 'square foot', 'square yard', 'acre', 'hectare'],
        "Speed": ['meter per second', 'kilometer per hour', 'mile per hour', 'knot',
                 'foot per second', 'inch per second'],
        "Energy": ['joule', 'kilojoule', 'calorie', 'kilocalorie', 'watt hour', 
                  'kilowatt hour', 'electron volt', 'british thermal unit'],
        "Pressure": ['pascal', 'kilopascal', 'megapascal', 'bar', 'atmosphere', 
                    'torr', 'psi', 'millimeter of mercury'],
        "Power": ['watt', 'kilowatt', 'megawatt', 'horsepower', 
                 'british thermal unit per hour', 'calorie per second'],
        "Frequency": ['hertz', 'kilohertz', 'megahertz', 'gigahertz',
                     'cycle per second', 'revolution per minute', 'beat per minute']
    }

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="logo-text">🔄 UniConvert Pro</div>', unsafe_allow_html=True)
        
        unit_categories = {
            "Basic": ["Length", "Weight", "Temperature", "Volume", "Area", "Speed"],
            "Science": ["Time", "Pressure", "Energy", "Power"],
            "Digital": ["Data", "Frequency"]
        }
        
        for category, units in unit_categories.items():
            with st.expander(category, expanded=category == "Basic"):
                cols = st.columns(2)
                for i, unit in enumerate(units):
                    with cols[i % 2]:
                        if st.button(f"{unit}", key=f"unit_{unit}"):
                            st.session_state.selected_unit = unit
                            # Reset unit selections when category changes
                            st.session_state.current_from_unit = None
                            st.session_state.current_to_unit = None
        
        st.subheader("Recent Conversions")
        if st.session_state.history:
            for conv in reversed(st.session_state.history[-5:]):
                st.markdown(f'<div class="history-item">{conv}</div>', unsafe_allow_html=True)
        else:
            st.info("No recent conversions")

    # Main content
    st.title("Unit Converter")
    st.write("Convert between different units with precision and ease")

    selected_unit = st.session_state.selected_unit
    units = units_dict.get(selected_unit, ['meter'])

    # Handle swapping logic
    if st.session_state.swap_trigger:
        # Swap the temporary variables
        temp = st.session_state.current_from_unit
        st.session_state.current_from_unit = st.session_state.current_to_unit
        st.session_state.current_to_unit = temp
        st.session_state.swap_trigger = False  # Reset the trigger

    # Input card
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            # Set default values for the selectboxes
            default_from = st.session_state.current_from_unit if st.session_state.current_from_unit in units else units[0]
            from_unit = st.selectbox("From", units, index=units.index(default_from), key="from_unit_selection")
            st.session_state.current_from_unit = from_unit
            value = st.number_input("Value", value=1.0, step=0.01, format="%.4f")
        
        with col2:
            st.markdown("<div style='height: 100%; display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
            if st.button("↔️ Swap", key="swap"):
                st.session_state.swap_trigger = True  # Trigger the swap
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            default_to = st.session_state.current_to_unit if st.session_state.current_to_unit in units else units[1 if len(units) > 1 else 0]
            to_unit = st.selectbox("To", units, index=units.index(default_to), key="to_unit_selection")
            st.session_state.current_to_unit = to_unit
            convert_button = st.button("Convert", key="convert", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Conversion logic
    if convert_button and value is not None:
        with st.spinner("Converting..."):
            time.sleep(0.3)
            conversion_functions = {
                "Length": convert_length, "Weight": convert_weight, "Temperature": convert_temperature,
                "Volume": convert_volume, "Time": convert_time, "Data": convert_data,
                "Area": convert_area, "Speed": convert_speed, "Energy": convert_energy,
                "Pressure": convert_pressure, "Power": convert_power, "Frequency": convert_frequency
            }
            
            result, formula = conversion_functions[selected_unit](value, from_unit, to_unit)
            
            st.markdown(f'<div class="result-display">{value:.4f} {from_unit} = {result:.4f} {to_unit}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="formula-display">Formula: {formula} = {result:.4f}</div>', unsafe_allow_html=True)
            
            st.session_state.history.append(f"{value:.4f} {from_unit} → {result:.4f} {to_unit}")

    # Quick Reference
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Quick Reference")
        
        reference_data = {
            "Length": {"Unit": ["meter", "kilometer", "inch", "foot", "mile"], 
                      "Equivalent": ["1 m", "1000 m", "0.0254 m", "0.3048 m", "1609.34 m"]},
            "Weight": {"Unit": ["kilogram", "gram", "pound", "ounce", "ton"],
                      "Equivalent": ["1 kg", "0.001 kg", "0.453592 kg", "0.0283495 kg", "1000 kg"]},
            "Temperature": {"Unit": ["celsius", "fahrenheit", "kelvin"],
                           "Freezing Point": ["0°C", "32°F", "273.15K"],
                           "Boiling Point": ["100°C", "212°F", "373.15K"]},
            "Volume": {"Unit": ["liter", "milliliter", "gallon (US)", "cup (US)", "fluid ounce (US)"],
                      "Equivalent": ["1 liter", "0.001 liters", "3.78541 liters", "0.236588 liters", "0.0295735 liters"]},
            "Time": {"Unit": ["second", "minute", "hour", "day", "year"],
                    "Equivalent": ["1 second", "60 seconds", "3600 seconds", "86400 seconds", "31536000 seconds"]},
            "Data": {"Unit": ["byte", "kilobyte", "megabyte", "gigabyte", "terabyte"],
                    "Equivalent": ["1 byte", "1024 bytes", "1048576 bytes", "1073741824 bytes", "1099511627776 bytes"]},
            "Area": {"Unit": ["square meter", "square kilometer", "acre", "hectare"],
                    "Equivalent": ["1 m²", "1,000,000 m²", "4046.86 m²", "10,000 m²"]},
            "Speed": {"Unit": ["meter per second", "kilometer per hour", "mile per hour", "knot"],
                     "Equivalent": ["1 m/s", "3.6 km/h", "2.237 mph", "1.944 knots"]},
            "Energy": {"Unit": ["joule", "kilojoule", "kilocalorie", "watt hour", "kilowatt hour"],
                      "Equivalent": ["1 J", "1000 J", "4184 J", "3600 J", "3.6×10⁶ J"]},
            "Pressure": {"Unit": ["pascal", "kilopascal", "bar", "atmosphere", "psi"],
                        "Equivalent": ["1 Pa", "1000 Pa", "100000 Pa", "101325 Pa", "6894.76 Pa"]},
            "Power": {"Unit": ["watt", "kilowatt", "horsepower", "british thermal unit per hour"],
                     "Equivalent": ["1 W", "1000 W", "745.7 W", "0.293071 W"]},
            "Frequency": {"Unit": ["hertz", "kilohertz", "megahertz", "gigahertz"],
                         "Equivalent": ["1 Hz", "1000 Hz", "1000000 Hz", "1000000000 Hz"]}
        }.get(selected_unit, {"Unit": [], "Equivalent": []})
        
        if reference_data["Unit"]:
            df = pd.DataFrame(reference_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("©2025 Made With Streamlit By Talal Shoaib | UniConvert Pro")

if __name__ == "__main__":
    main()