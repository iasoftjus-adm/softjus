from kivy.storage.jsonstore import JsonStore
from datetime import datetime
import os


class FavoritesStore:
    def __init__(self, filename='data/favorites.json'):
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        self.store = JsonStore(filename)

    def add_favorite(self, process_data):
        """Add a process to favorites"""
        # Check if already exists
        for key in self.store:
            fav = self.store.get(key)
            if fav.get('processo') == process_data.get('processo'):
                return False

        key = f"processo_{len(self.store) + 1}"
        self.store.put(key,
                       processo=process_data.get('processo'),
                       classe=process_data.get('classe'),
                       tribunal=process_data.get('tribunal', 'N/A'),
                       data_adicao=datetime.now().isoformat())
        return True

    def remove_favorite(self, process_number):
        """Remove a process from favorites"""
        for key in self.store:
            fav = self.store.get(key)
            if fav.get('processo') == process_number:
                self.store.delete(key)
                return True
        return False

    def get_favorites(self):
        """Get all favorites"""
        favorites = []
        for key in self.store:
            favorites.append(self.store.get(key))
        return favorites

    def is_favorite(self, process_number):
        """Check if a process is already favorited"""
        for key in self.store:
            fav = self.store.get(key)
            if fav.get('processo') == process_number:
                return True
        return False

    def clear_favorites(self):
        """Clear all favorites"""
        keys = list(self.store.keys())
        for key in keys:
            self.store.delete(key)
        return True