from models.productor_consumidor import iniciar_sistema, detener_sistema
import time

if __name__ == "__main__":
    try:
        iniciar_sistema()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        detener_sistema()
