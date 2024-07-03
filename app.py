from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import pandas as pd
import zipfile
import os
import numpy as np

app = Flask(__name__)

# Function to split on the second to last comma
def split_on_second_last_comma(s):
    s = str(s)
    parts = s.split(', ', 2)
    if len(parts) == 3:
        return parts[1].strip()  # the region part
    else:
        return None  # or handle appropriately if not in expected format

def get_field_values():
    
    available_categories = ['Red', 'White', 'Sparkling', 'Rose', 'Dessert', 'Port/Sherry', 'Fortified']
    available_countries = ['US', 'Chile', 'Spain', 'France', 'Italy', 'Portugal', 'Australia', 'South Africa', 'Argentina', 'Germany', 'Austria', 'Israel', 'New Zealand', 'Greece', 'Romania', 'Hungary']
    zf = zipfile.ZipFile(f'{os.getcwd()}/data/wine_data.zip') 
    df = pd.read_csv(zf.open('wine_first_batch.csv'))
    year = df['year'].dropna().astype(np.int64).unique()
    year = list(map(str, list(year) + [2017,2018,2019,2020,2021,2022,2023,2024]))

    available_years = sorted(year, reverse=True)

    # Apply function to the DataFrame
    available_regions = list(df['appellation'].apply(split_on_second_last_comma).dropna().unique())
    available_regions = sorted([ x for x in available_regions if "\$" not in x ])
    available_grape_varieties = list(df['varietal'].dropna().unique())
    available_grape_varieties = sorted([ y for y in available_grape_varieties if "$" not in y ])

    available_wineries = list(df['winery'].dropna().unique())

    return available_years, available_categories, available_countries, available_regions, available_grape_varieties, available_wineries




@app.route('/', methods=['GET', 'POST'])
def index():
    available_years, available_categories, available_countries, available_regions, available_grape_varieties, available_wineries = get_field_values()

    if request.method == 'POST':
        # Process form data
        selected_url = request.form['model_url']
        selected_year = int(request.form['year'])
        selected_winery = request.form['winery']
        selected_category = request.form['category']
        selected_varietal = request.form['variety']
        selected_alcohol_percentage = float(request.form['alcohol_percentage'])
        selected_country = request.form['country']
        selected_region = request.form['region']
        # You can add logic to process these inputs
        if selected_alcohol_percentage == '':
            selected_alcohol_percentage = 12

        payload = json.dumps({
            "dataframe_split": {
                "columns": [
                "id",
                "year",
                "wine",
                "winery",
                "category",
                "wine_name",
                "designation",
                "grape_variety",
                "appellation",
                "alcohol",
                "rating",
                "reviewer",
                "review",
                "country",
                "region"
                ],
                "data": [
                [
                    None,
                    selected_year,
                    None,
                    selected_winery,
                    selected_category,
                    None,
                    None,
                    selected_varietal,
                    None,
                    selected_alcohol_percentage,
                    85,
                    None,
                    None,
                    selected_country,
                    selected_region
                ]
                ]
            }
            })
        # Headers with the first authorization token
        headers1 = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer dapib5e25919c5f4bca1c20f5e6662d65e58-2"
        }

        # Headers with the second authorization token
        headers2 = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer dapi93a5b514d4fb731e7970d35985f485de-2"
        }

        # Try the first response
        response = requests.request("POST", selected_url, headers=headers1, data=payload)

        # Check if the first request was successful
        if response.status_code != 200:
            # If not successful, try the second response
            response = requests.request("POST", selected_url, headers=headers2, data=payload)
        # Use the json module to load CKAN's response into a dictionary.
        response_dict = json.loads(response.text)
        return redirect(url_for('results', winery=selected_winery, category=selected_category, year=str(selected_year),
                                        varietal=selected_varietal, alcohol_percentage=selected_alcohol_percentage,
                                        country=selected_country, region=selected_region, price=response_dict['predictions']))

    
    return render_template('index.html', years=available_years, categories=available_categories, varieties=available_grape_varieties,
                           countries=available_countries, regions=available_regions, wineries=available_wineries)

@app.route('/results')
def results():
    year = request.args.get('year')
    winery = request.args.get('winery')
    category = request.args.get('category')
    varietal = request.args.get('varietal')
    alcohol_percentage = request.args.get('alcohol_percentage')
    price = request.args.get('price')
    country = request.args.get('country')
    region = request.args.get('region')
    rating = request.args.get('rating')

    
    return render_template('results.html', year=year, winery=winery, category=category,
                           varietal=varietal, alcohol_percentage=alcohol_percentage,
                           price=price, country=country, region=region, rating=rating)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
