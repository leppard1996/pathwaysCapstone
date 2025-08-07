import pandas as pd 
import matplotlib.pyplot as plt 
import os 
import glob 


def analyze_weather_files():
    """
    Loop through weather files (weather1.py to weather4.py), find unique cities,
    and display temperature data using matplotlib.
    
    This function will:
    1. Find all weather files matching the pattern
    2. Load and combine data from all files
    3. Find unique cities
    4. Extract temperature data (from avg_temp or temperature column)
    5. Create visualizations of the temperature data
    """
    
    # List to store all weather data from different files
    all_weather_data = []
    
    # Define the weather file pattern to search for
    file_pattern = "weather*.csv"  # Changed from .py to .csv since we're working with data files
    
    # Find all files matching the weather pattern
    weather_files = glob.glob(file_pattern)
    
    # If no CSV files found, try looking for Python files (in case they contain data)
    if not weather_files:
        weather_files = ["weather1.py", "weather2.py", "weather3.py", "weather4.py"]
        # Filter to only existing files
        weather_files = [f for f in weather_files if os.path.exists(f)]
    
    # Check if any weather files were found
    if not weather_files:
        print("❌ No weather files found!")
        print("Looking for: weather1.py, weather2.py, weather3.py, weather4.py")
        print("Or CSV files matching pattern: weather*.csv")
        return
    
    # Loop through each weather file
    for file_name in weather_files:
        print(f"📖 Processing file: {file_name}")
        
        try:
            # Try to read as CSV first
            if file_name.endswith('.csv'):
                # Read CSV file
                df = pd.read_csv(file_name)
                print(f"   ✅ Successfully loaded CSV with {len(df)} rows")
            else:
                # If it's a Python file, you might need custom logic here
                # For now, skip Python files unless they're actually CSV data
                print(f"   ⚠️  Skipping Python file: {file_name}")
                print("      (Convert to CSV format for analysis)")
                continue
            
            # Add source file information
            df['source_file'] = file_name
            
            # Add to our combined dataset
            all_weather_data.append(df)
            
        except Exception as e:
            print(f"Error reading {file_name}: {str(e)}")
            continue
    
    # Check if we have any data to work with
    if not all_weather_data:
        print("No valid data found in any files!")
        return
    
    # Combine all data into one DataFrame
    combined_df = pd.concat(all_weather_data, ignore_index=True)
    
    # Find unique cities
    # Try different possible city column names
    city_columns = ['city', 'location']
    city_column = None
    
    for col in city_columns:
        if col in combined_df.columns:
            city_column = col
            break
    
    # Get unique cities
    unique_cities = combined_df[city_column].unique()
    for i, city in enumerate(unique_cities, 1):
        print(f"   {i}. {city}")
    
    # Find temperature column
    temp_columns = ['avg_temp', 'temperature']
    temp_column = None
    
    for col in temp_columns:
        if col in combined_df.columns:
            temp_column = col
            break

    
    # Set up the plot style
    plt.style.use('default')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('Weather Temperature Analysis', fontsize=16, fontweight='bold')
    
    #Average temperature by city (bar chart)
    city_avg_temps = combined_df.groupby(city_column)[temp_column].mean().sort_values(ascending=False)
    
    ax1.bar(range(len(city_avg_temps)), city_avg_temps.values, 
            color='skyblue', edgecolor='navy', alpha=0.7)
    ax1.set_title('Average Temperature by City', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Cities', fontsize=12)
    ax1.set_ylabel('Temperature (°F)', fontsize=12)
    ax1.set_xticks(range(len(city_avg_temps)))
    ax1.set_xticklabels(city_avg_temps.index, rotation=45, ha='right')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, v in enumerate(city_avg_temps.values):
        ax1.text(i, v + 0.5, f'{v:.1f}°F', ha='center', va='bottom', fontweight='bold')
    
    # Plot 2: Temperature distribution (box plot)
    city_temps = [combined_df[combined_df[city_column] == city][temp_column].values 
                  for city in unique_cities]
    
    box_plot = ax2.boxplot(city_temps, labels=unique_cities, patch_artist=True)
    ax2.set_title('Temperature Distribution by City', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Cities', fontsize=12)
    ax2.set_ylabel('Temperature (°F)', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    # Color the box plots
    colors = ['lightcoral', 'lightblue', 'lightgreen', 'lightyellow', 'lightpink', 'lightgray']
    for patch, color in zip(box_plot['boxes'], colors[:len(box_plot['boxes'])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Show the plots
    plt.show()


if __name__ == "__main__":
    analyze_weather_files()