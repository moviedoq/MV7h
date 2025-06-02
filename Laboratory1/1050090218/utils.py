# utils.py
import random

def simulate_failure(channel_name: str) -> bool:
    """Simula un fallo de envío. True para éxito, False para fallo."""
    # Hacemos que la consola nunca falle para asegurar un último recurso
    if channel_name == "console":
        return True
    return random.choice([True, False, True]) # Aumentamos la probabilidad de éxito para no fallar siempre