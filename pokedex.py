from flask import Flask, request, jsonify, send_from_directory
import pandas as pd

app = Flask(__name__, static_folder='.', static_url_path='')

# Charger les données une seule fois au démarrage
pokemon_df = pd.read_csv('pokedex_francais_complet.csv')
images_df = pd.read_csv('pokemon_images.csv')
df = pokemon_df.merge(images_df, on='Numéro', how='left')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    if not query:
        results = df
    else:
        mask = (
            df['Nom'].str.lower().str.contains(query) |
            df['Type 1'].str.lower().str.contains(query) |
            df['Type 2'].str.lower().str.contains(query) |
            df['Numéro'].astype(str).str.contains(query)
        )
        results = df[mask]
    return jsonify(results.fillna('').to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)