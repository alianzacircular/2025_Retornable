import requests
import pandas as pd
import csv
import tempfile
import os

from flask import jsonify, send_file

def calculate_distances(file):
    """
    Calculate the distance and duration between two fixed coordinates using OSRM.
    """
    try:
        # Read .csv
        # file = 'https://docs.google.com/uc?export=download&id=1VYEnH735Tdgqe9cS4ccYV0OUxMqQpsQh'
        print(f"Processing file: {file}")
        df = pd.read_csv(file, usecols=['id', 'latitude', 'longitude', 'type'])
        number = 1

        # Filter by type
        collections = df[df['type'] == 'collection'].drop_duplicates(subset='id')
        clasifications = df[df['type'] == 'clasification'].drop_duplicates(subset='id')
        washings = df[df['type'] == 'washing'].drop_duplicates(subset='id')
        producers = df[df['type'] == 'producer'].drop_duplicates(subset='id')

        results = []
        print('processing distances...')
        # Distances calculation
        # 1. Collection to Clasification
        for _, collection in collections.iterrows():
            for _, clasification in clasifications.iterrows():
                url = f"https://router.project-osrm.org/route/v1/driving/{collection['longitude']},{collection['latitude']};{clasification['longitude']},{clasification['latitude']}?overview=false"
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    distance_km = data["routes"][0]["distance"] / 1000
                    print(f"{number} - {distance_km:.3f}")
                    number += 1
                    results.append({
                        'origin': collection['id'],
                        'type_origin': collection['type'],
                        'destination': clasification['id'],
                        'tipo_destination': clasification['type'],
                        'distance_geo': round(distance_km, 3)
                    })
                except Exception as e:
                    print(f"Error collection to clasification: {collection['id']} - {clasification['id']}: {e}")

        # 2. Clasification to Washing
        for _, clasification in clasifications.iterrows():
            for _, washing in washings.iterrows():
                url = f"https://router.project-osrm.org/route/v1/driving/{clasification['longitude']},{clasification['latitude']};{washing['longitude']},{washing['latitude']}?overview=false"
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    distance_km = data["routes"][0]["distance"] / 1000
                    print(f"{number} - {distance_km:.3f}")
                    number += 1
                    results.append({
                        'origin': clasification['id'],
                        'type_origin': clasification['type'],
                        'destination': washing['id'],
                        'tipo_destination': washing['type'],
                        'distance_geo': round(distance_km, 3)
                    })
                except Exception as e:
                    print(f"Error clasification to washing: {clasification['id']} - {washing['id']}: {e}")

        # 3. Washing to Producer
        for _, washing in washings.iterrows():
            for _, producer in producers.iterrows():
                url = f"https://router.project-osrm.org/route/v1/driving/{washing['longitude']},{washing['latitude']};{producer['longitude']},{producer['latitude']}?overview=false"
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    distance_km = data["routes"][0]["distance"] / 1000
                    print(f"{number} - {distance_km:.3f}")
                    number += 1
                    results.append({
                        'origin': washing['id'],
                        'type_origin': washing['type'],
                        'destination': producer['id'],
                        'tipo_destination': producer['type'],
                        'distance_geo': round(distance_km, 3)
                    })
                except Exception as e:
                    print(f"Error washing to producer: {washing['id']} - {producer['id']}: {e}")

        # Save CSV file
        # filename = 'distances.csv'
        # with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        #     fieldnames = ['origin', 'type_origin', 'destination', 'tipo_destination', 'distance_geo']
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
        #     for row in results:
        #         writer.writerow(row)

        # return send_file(
        #     filename,
        #     as_attachment=True,
        #     download_name=filename,
        #     mimetype='text/csv'
        # )

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', newline='', encoding='utf-8')
        fieldnames = ['origin', 'type_origin', 'destination', 'tipo_destination', 'distance_geo']
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
        temp_file.close()

        # Enviar archivo
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name='distances.csv',
            mimetype='text/csv'
        )


    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500