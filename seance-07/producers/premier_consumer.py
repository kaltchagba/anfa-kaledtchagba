"""
premier_consumer.py
────────────────────
Lit tous les messages du topic anfa-positions-bus depuis le début.
"""

import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "anfa-positions-bus",
    bootstrap_servers=["localhost:19092", "localhost:19093", "localhost:19094"],
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",     # lire depuis le début du topic
    group_id="mon-premier-groupe",    # identifiant du consumer group
    consumer_timeout_ms=5000,         # s'arrête si rien de nouveau après 5s
)

print("[INFO] Lecture des messages...\n")
for message in consumer:
    print(f"[LU] partition={message.partition} offset={message.offset} -> {message.value}")

print("\n[OK] Fin de la lecture (plus de nouveaux messages).")
