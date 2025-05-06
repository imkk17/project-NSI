import pandas as pd
import os
import msvcrt
import webbrowser

def load_pokemon_data() -> pd.DataFrame:
    """Charge les données des Pokémon depuis les fichiers CSV."""
    pokemon_df = pd.read_csv('pokedex_francais_complet.csv')
    images_df = pd.read_csv('pokemon_images.csv')
    return pokemon_df.merge(images_df, on='Numéro', how='left')

def search_pokemon(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Recherche des Pokémon correspondant à la requête."""
    if not query:
        return pd.DataFrame
    
    # Essayer d'abord la recherche par numéro
    try:
        num = int(query)
        return df[df['Numéro'] == num]
    except ValueError:
        # Si ce n'est pas un numéro, chercher dans le nom et les types
        mask = (
            df['Nom'].str.contains(query, case=False, na=False) |
            df['Type 1'].str.contains(query, case=False, na=False) |
            df['Type 2'].str.contains(query, case=False, na=False)
        )
        return df[mask]

def display_pokemon_details(pokemon: pd.Series):
    """Affiche les détails d'un Pokémon."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"=== {pokemon['Nom']} (N°{pokemon['Numéro']:03d}) ===")
    print("-" * 40)
    
    # Types
    types = f"{pokemon['Type 1']}/{pokemon['Type 2']}" if pd.notna(pokemon['Type 2']) else pokemon['Type 1']
    print(f"Types: {types}")
    
    # Statistiques
    print("\nStatistiques:")
    print(f"PV: {pokemon['PV']}")
    print(f"Attaque: {pokemon['Attaque']}")
    print(f"Défense: {pokemon['Défense']}")
    print(f"Attaque Spéciale: {pokemon['Attaque Spéciale']}")
    print(f"Défense Spéciale: {pokemon['Défense Spéciale']}")
    print(f"Vitesse: {pokemon['Vitesse']}")
    
    # Génération et région
    print(f"\nGénération: {pokemon['Génération']}")
    print(f"Région: {pokemon['Région']}")
    
    # Évolution
    if pd.notna(pokemon['Évolution']):
        print(f"\nÉvolue de: {pokemon['Évolution']}")
    
    # Image
    if pd.notna(pokemon['URL Image']):
        print("\nAppuyez sur 'i' pour voir l'image du Pokémon...")
    
    print("\nAppuyez sur une touche pour revenir à la recherche...")
    key = msvcrt.getch()
    
    # Si l'utilisateur appuie sur 'i' et qu'il y a une image
    if ord(key) == 105 and pd.notna(pokemon['URL Image']):  # 'i'
        webbrowser.open(pokemon['URL Image'])

def display_results(results: pd.DataFrame, query: str, selected_idx: int = 0, max_lines: int = 15):
    """Affiche les résultats de la recherche."""
    # Effacer l'écran
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Afficher l'en-tête
    print("=== Recherche de Pokémon ===")
    print("Appuyez sur ÉCHAP pour quitter")
    print("Utilisez les flèches ↑↓ pour sélectionner et Entrée pour voir les détails")
    print("Appuyez sur 'i' dans les détails pour voir l'image")
    print(f"\nRecherche: {query}")
    print("-" * 40)
    
    if results.empty:
        print("\nAucun résultat trouvé")
        return
    
    start_idx = max(0, selected_idx - max_lines + 1)
    end_idx = min(len(results), start_idx + max_lines)
    
    for i, (_, row) in enumerate(results.iloc[start_idx:end_idx].iterrows()):
        prefix = ">" if i + start_idx == selected_idx else " "
        types = f"{row['Type 1']}/{row['Type 2']}" if pd.notna(row['Type 2']) else row['Type 1']
        print(f"{prefix} {row['Numéro']:03d} - {row['Nom']} ({types})")
    
    if end_idx < len(results):
        print(f"\n... et {len(results) - end_idx} autres résultats")
    print("-" * 40)

def main():
    # Chargement des données
    print("Chargement des données...")
    df = load_pokemon_data()
    print("Données chargées !")
    
    query = ""
    results = pd.DataFrame()
    selected_idx = 0
    
    # Afficher l'écran initial
    display_results(results, query, selected_idx)
    
    while True:
        # Attendre qu'une touche soit pressée
        if msvcrt.kbhit():
            key = msvcrt.getch()
            
            # Échap pour quitter
            if ord(key) == 27:  # ESC
                break
            # Retour arrière pour effacer
            elif ord(key) == 8:  # BACKSPACE
                query = query[:-1]
                results = search_pokemon(df, query)
                selected_idx = 0
                display_results(results, query, selected_idx)
            # Entrée pour afficher les détails
            elif ord(key) == 13:  # ENTER
                if not results.empty and selected_idx < len(results):
                    display_pokemon_details(results.iloc[selected_idx])
                    display_results(results, query, selected_idx)
            # Flèche haut
            elif ord(key) == 72:  # UP
                if not results.empty:
                    selected_idx = max(0, selected_idx - 1)
                    display_results(results, query, selected_idx)
            # Flèche bas
            elif ord(key) == 80:  # DOWN
                if not results.empty:
                    selected_idx = min(len(results) - 1, selected_idx + 1)
                    display_results(results, query, selected_idx)
            # Caractères normaux
            elif 32 <= ord(key) <= 126:  # Caractères ASCII imprimables
                query += key.decode('ascii')
                results = search_pokemon(df, query)
                selected_idx = 0
                display_results(results, query, selected_idx)

if __name__ == "__main__":
    main() 