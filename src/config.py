from typing import List

class Settings:
    app_name: str = "Paack Assignment API"
    preload_addresses: List[str] = [
        "Calle Prueba 123 4 3A, Madrid",
        "Avenida Siempre Viva 456 4C, Barcelona",
        "Calle del Naranjo 10 Bajo B, Valencia",
        "Calle de la Zamburiña 124 5A, Galicia"
    ]

settings = Settings()