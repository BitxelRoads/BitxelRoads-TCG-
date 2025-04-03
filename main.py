# MÓDULOS 1–6: Generador de Cartas, Gadgets, Combate, MP, Sinergias y Maniobrabilidad

import random

# ------------------------------
# CONFIGURACIÓN DE PROPIEDADES
# ------------------------------

STAR_DISTRIBUTION = {
    1: (10, 19),
    2: (20, 26),
    3: (27, 32),
}

NITRO_PROBABILITIES = {
    "No Nitro": 0.65,
    "Nitro Orange": 0.15,
    "Nitro Blue": 0.15,
    "Both Nitros": 0.05,
}

MODELS = ["Convertible", "Luxury", "Sport", "Turbo"]
PROTOCOLS = ["PoW", "PoS", "Layer 2", "P2P", "Genesis"]
VARIABLES = ["accel", "speed", "fuel", "brakes"]

# ------------------------------
# FUNCIÓN: Seleccionar Nitro al Azar
# ------------------------------
def select_nitro():
    return random.choices(list(NITRO_PROBABILITIES.keys()), weights=NITRO_PROBABILITIES.values())[0]

# ------------------------------
# FUNCIÓN: Generar una carta de auto
# ------------------------------
def generate_car_card(card_id: int):
    star = random.choices([1, 2, 3], weights=[60, 28, 12])[0]
    suma_min, suma_max = STAR_DISTRIBUTION[star]

    while True:
        stats = [random.randint(1, 10) for _ in range(4)]
        if suma_min <= sum(stats) <= suma_max:
            if star < 3 and (stats.count(1) > 1 or stats.count(10) > 1):
                continue
            break

    acc, spd, fuel, brakes = stats
    nitro = select_nitro()
    model = random.choice(MODELS)
    protocol = random.choice(PROTOCOLS)

    return {
        "id": f"CAR_{card_id}",
        "stars": star,
        "accel": acc,
        "speed": spd,
        "fuel": fuel,
        "brakes": brakes,
        "nitro": nitro,
        "model": model,
        "protocol": protocol,
        "used_vars": [],
        "cooldown": False,
        "alt_defense_used": False,
        "last_var_used": None
    }

# ------------------------------
# MÓDULO 2: Generador de Gadgets
# ------------------------------

GADGETS = [
    {
        "name": "Oil Slick",
        "base_cost": 2,
        "instant": "Enemy skips Accel or Speed next turn (50% backfire).",
        "equipment": "+1 Fuel, -1 Brakes while active.",
        "synergy": "Turbo cars are immune to instant effect."
    },
    {
        "name": "Brake Fluid",
        "base_cost": 1,
        "instant": "Reduce Brakes damage by 50% this turn.",
        "equipment": "+1 FP when using Brakes.",
        "synergy": "PoW: Also +1 Accel when active."
    },
    {
        "name": "Spike Strip",
        "base_cost": 3,
        "instant": "Enemy loses 3 FP if they used Brakes.",
        "equipment": "Enemy Brakes have 30% chance to fail.",
        "synergy": "P2P: Ignores Fuel Economy resistance."
    },
    {
        "name": "Pothole",
        "base_cost": 1,
        "instant": "Reduce enemy Brakes by -2 if their last action was Fuel.",
        "equipment": "Enemy loses 1 FP every time they use Brakes.",
     "synergy": "PoW: Equipment duration +1 round"
    }, 
    {
        "name": "Traffic Police",
        "base_cost": 1,
        "instant": "Cancels opponent’s next variable (random choice).",
        "equipment": "Enemy cannot repeat the same variable twice in a row.",
        "synergy": "PoS: Equipment costs 1 less MP"
    },
    {
        "name": "Speed Radar",
        "base_cost": 1,
        "instant": "Ignore Nitro when comparing Speed; deal +1 FP if you win.",
        "equipment": "+1 Speed if last action was Accel.",
        "synergy": "Layer 2: Instant costs 0 MP next round"
    },
    {
        "name": "Protocol Shift",
        "base_cost": 3,
        "instant": "Copy opponent’s protocol for this round.",
        "equipment": "Your protocol is treated as both yours and opponent’s.",
        "synergy": "Genesis: Immune to protocol effects"
    },
    {
        "name": "GPS Jammer",
        "base_cost": 3,
        "instant": "Guess enemy’s variable; if correct, cancel and deal 2 FP.",
        "equipment": "See opponent’s chosen variable 1 round early.",
        "synergy": "Layer 2: No penalty if your guess is wrong"
    },
    {
        "name": "Spoiler Kit",
        "base_cost": 1,
        "instant": "+2 Speed this round.",
        "equipment": "+1 Speed, -1 Fuel while active.",
        "synergy": "Sport: No penalty on Equipment"
    },
    {
        "name": "Shock Absorber",
        "base_cost": 2,
        "instant": "Negate 2 damage from Accel or Brakes this round.",
        "equipment": "Reduce all incoming damage by 1.",
        "synergy": "Luxury: Equipment cost reduced by 1 MP"
    }

]

# ------------------------------
# FUNCIÓN: Generar un gadget
# ------------------------------
def generate_gadget(player_stars):
    gadget = random.choice(GADGETS)
    use_mode = random.choice(["Instant", "Equipment"])
    base_cost = gadget["base_cost"]
    star_modifier = 0 if player_stars == 1 else 1 if player_stars == 2 else 2
    total_cost = base_cost + (1 if use_mode == "Equipment" else 0) + star_modifier

    return {
        "name": gadget["name"],
        "mode": use_mode,
        "cost": total_cost,
        "effect": gadget[use_mode.lower()],
        "synergy": gadget["synergy"],
        "active": False,
        "revealed": False
    }

# ------------------------------
# MÓDULO 3: Lógica de Combate por Ronda
# ------------------------------

def select_variable(card):
    remaining = [v for v in VARIABLES if v not in card['used_vars']]
    selected = random.choice(remaining)
    card['used_vars'].append(selected)
    card['last_var_used'] = selected
    return selected

def calculate_damage(var1, var2, stat1, stat2):
    if stat1 == stat2:
        return "tie", 0, 0
    elif stat1 > stat2:
        return "p1_wins", 0, stat1 - stat2
    else:
        return "p2_wins", stat2 - stat1, 0

# ------------------------------
# MÓDULO 4: Sistema de MP y Activación de Gadget + Cooldown
# ------------------------------

def can_activate_gadget(gadget, mp):
    return mp >= gadget["cost"] and not gadget["revealed"]

def activate_gadget(gadget):
    gadget["revealed"] = True
    if gadget["mode"] == "Equipment":
        gadget["active"] = True
    return gadget

# ------------------------------
# MÓDULO 5: Aplicación de Sinergias Modelo + Protocolo
# ------------------------------

def apply_synergy(card):
    bonus = 0.0
    if card['model'] == "Convertible" and card['last_var_used'] == "fuel":
        bonus += 1.5
        if card['protocol'] == "P2P":
            bonus += 0.5
    elif card['model'] == "Luxury" and card['last_var_used'] == "accel":
        bonus += 1.5
        if card['protocol'] == "PoS":
            bonus += 0.5
    elif card['model'] == "Sport" and card['last_var_used'] == "speed":
        bonus += 1.5
        if card['protocol'] == "Layer 2":
            bonus += 0.5
    elif card['model'] == "Turbo" and card['last_var_used'] == "brakes":
        bonus += 1.5
        if card['protocol'] == "PoW":
            bonus += 0.5
    return bonus

# ------------------------------
# MÓDULO 6: Maniobrabilidad y Empates
# ------------------------------

def calculate_maneuverability(card):
    avg = (card['accel'] + card['speed'] + card['fuel'] + card['brakes']) / 4
    bonus = 2 if card['stars'] == 1 else 1 if card['stars'] == 2 else 0
    return round(12 - avg + bonus, 2)

def resolve_tie(card1, card2):
    man1 = calculate_maneuverability(card1)
    man2 = calculate_maneuverability(card2)
    if man1 > man2:
        return "player1"
    elif man2 > man1:
        return "player2"
    else:
        # Random dice with star bonus
        d1 = random.randint(1, 6) + (2 if card1['stars'] == 1 else 1 if card1['stars'] == 2 else 0)
        d2 = random.randint(1, 6) + (2 if card2['stars'] == 1 else 1 if card2['stars'] == 2 else 0)
        return "player1" if d1 > d2 else "player2"

# ------------------------------
# DEMO: Generar mazo completo
# ------------------------------
def demo_generate_player_deck():
    deck = []
    star3_used = False

    while len(deck) < 3:
        card = generate_car_card(len(deck)+1)
        if card['stars'] == 3:
            if star3_used:
                continue
            star3_used = True
        deck.append(card)

    avg_stars = round(sum(c['stars'] for c in deck) / 3)
    gadget = generate_gadget(avg_stars)

    return deck, gadget



# MÓDULO 7: Lógica Completa de Ronda y Partida
# ------------------------------

def play_match(deck1, gadget1, deck2, gadget2):
    fp1, fp2 = 12, 12
    mp = 1
    print("\n--- MATCH START ---")
    print(f"Player 1 gadget: {gadget1['name']}")
    print(f"Player 2 gadget: {gadget2['name']}")

    for round_num in range(1, 4):
        print(f"\n>>> ROUND {round_num} (MP = {mp})")

        # Activación opcional del gadget si instantáneo
        if can_activate_gadget(gadget1, mp) and gadget1['mode'] == "Instant":
            print("Player 1 activates gadget as INSTANT")
            activate_gadget(gadget1)
            mp -= gadget1['cost']

        if can_activate_gadget(gadget2, mp) and gadget2['mode'] == "Instant":
            print("Player 2 activates gadget as INSTANT")
            activate_gadget(gadget2)
            mp -= gadget2['cost']

        # Activación como equipo si no ha sido usada
        if can_activate_gadget(gadget1, mp) and gadget1['mode'] == "Equipment":
            print("Player 1 activates gadget as EQUIPMENT")
            activate_gadget(gadget1)
            mp -= gadget1['cost']

        if can_activate_gadget(gadget2, mp) and gadget2['mode'] == "Equipment":
            print("Player 2 activates gadget as EQUIPMENT")
            activate_gadget(gadget2)
            mp -= gadget2['cost']

        # Selección de autos por orden
        car1 = deck1[round_num - 1]
        car2 = deck2[round_num - 1]

        var1 = select_variable(car1)
        var2 = select_variable(car2)

        stat1 = car1[var1] + apply_synergy(car1)
        stat2 = car2[var2] + apply_synergy(car2)

        result, dmg1, dmg2 = calculate_damage(var1, var2, stat1, stat2)

        if result == "tie":
            winner = resolve_tie(car1, car2)
            if winner == "player1":
                dmg2 = 1
            else:
                dmg1 = 1

        fp1 -= dmg1
        fp2 -= dmg2

        print(f"Player 1 uses {car1['id']} ({var1}) | Player 2 uses {car2['id']} ({var2})")
        print(f"-> Player 1 takes {dmg1} damage | Player 2 takes {dmg2} damage")
        print(f"-> FP: Player 1 = {fp1} | Player 2 = {fp2}")

        # Ronda completada, aplicar cooldown
        car1['cooldown'] = True
        car2['cooldown'] = True

        mp = min(mp + 1, 3)  # Escala máximo hasta 3 MP

        if fp1 <= 0 or fp2 <= 0:
            break

    print("\n--- MATCH END ---")
    if fp1 > fp2:
        print("WINNER: Player 1")
    elif fp2 > fp1:
        print("WINNER: Player 2")
    else:
        final_winner = resolve_tie(deck1[-1], deck2[-1])
        print(f"TIEBREAKER WINNER: {final_winner.upper()}")




# ------------------------------
# MÓDULO 8: Nitro System
# ------------------------------

def apply_nitro(card):
    boost = {"accel": 0, "speed": 0, "brakes": 0, "fuel": 0}
    fail = False

    if card['nitro'] == "Nitro Blue":
        fail = random.random() < 0.3
        if not fail:
            boost["speed"] += 1
            boost["brakes"] += 1
        else:
            boost["fuel"] -= 1

    elif card['nitro'] == "Nitro Orange":
        fail = random.random() < 0.3
        if not fail:
            boost["accel"] += 1
            boost["fuel"] += 1
        else:
            boost["brakes"] -= 1

    elif card['nitro'] == "Both Nitros":
        fail = random.random() < 0.5
        if not fail:
            for k in boost:
                boost[k] += 1
        else:
            for k in boost:
                boost[k] -= 1

    return boost, fail

# 🔄 Esta función se integrará dentro de la lógica de combate del módulo 7 (por variable).


# ------------------------------
# MÓDULO 9: MP Individual por Jugador
# ------------------------------

def initialize_players():
    p1_deck, p1_gadget = demo_generate_player_deck()
    p2_deck, p2_gadget = demo_generate_player_deck()

    player1 = {
        "deck": p1_deck,
        "gadget": p1_gadget,
        "fp": 12,
        "mp": 1,
        "name": "Player 1"
    }
    
    player2 = {
        "deck": p2_deck,
        "gadget": p2_gadget,
        "fp": 12,
        "mp": 1,
        "name": "Player 2"
    }

    return player1, player2

# ✅ A partir de aquí se usará player['mp'] en vez de variable global, y podrá escalarse individualmente.

# ------------------------------
# MÓDULO 10: Aplicar efectos reales de gadgets
# ------------------------------

def apply_gadget_effects(player, opponent, current_var):
    gadget = player['gadget']
    if not gadget['active']:
        return 0, 0  # No efecto si no está activo

    # Efectos de equipo (permanentes)
    if gadget['name'] == "Brake Fluid" and current_var == "brakes":
        player['fp'] += 1

    if gadget['name'] == "Oil Slick":
        player_card = player['deck'][0]
        player_card['fuel'] += 1
        player_card['brakes'] -= 1

    if gadget['name'] == "Spike Strip":
        if opponent['deck'][0]['last_var_used'] == "brakes":
            if random.random() < 0.3:
                return 0, 1  # El oponente falla y recibe daño directo

    return 0, 0  # Sin daño directo adicional por defecto

# 🔄 Se usará durante el enfrentamiento para modificar FP, daño, o stats.

# ------------------------------
# MÓDULO 11: Defensa Alternativa (1 vez por carta)
# ------------------------------

def use_alternative_defense(defender_card, incoming_var):
    if defender_card['alt_defense_used']:
        return 0  # No permitido más de una vez

    alt_vars = [v for v in VARIABLES if v != incoming_var and v not in defender_card['used_vars']]
    if not alt_vars:
        return 0  # No hay defensa disponible

    chosen_def = random.choice(alt_vars)
    defender_card['alt_defense_used'] = True
    return defender_card[chosen_def]  # Valor alterno para mitigar daño

# Esta función podrá integrarse en el combate antes de aplicar el daño real.


# ------------------------------
# MÓDULO 12: Rondas completas por rotación de cartas
# ------------------------------

def play_full_rotation(player1, player2):
    print("\n🧪 FULL MATCH START")
    round_index = 0
    for phase in range(3):  # 3 fases, cada carta entra 1 vez por ronda
        for idx in range(3):
            car1 = player1['deck'][idx]
            car2 = player2['deck'][idx]

            print(f"\n🔁 Duel {phase * 3 + idx + 1}: {car1['id']} vs {car2['id']}")

            var1 = select_variable(car1)
            var2 = select_variable(car2)

            boost1, fail1 = apply_nitro(car1)
            boost2, fail2 = apply_nitro(car2)

            stat1 = car1[var1] + apply_synergy(car1) + boost1.get(var1, 0)
            stat2 = car2[var2] + apply_synergy(car2) + boost2.get(var2, 0)

            # Aplicar defensa alternativa si decide usarla
            alt_def2 = use_alternative_defense(car2, var2)
            if alt_def2:
                stat2 = alt_def2

            alt_def1 = use_alternative_defense(car1, var1)
            if alt_def1:
                stat1 = alt_def1

            result, dmg1, dmg2 = calculate_damage(var1, var2, stat1, stat2)

            if result == "tie":
                winner = resolve_tie(car1, car2)
                if winner == "player1":
                    dmg2 = 1
                else:
                    dmg1 = 1

            bonus1, bonus2 = apply_gadget_effects(player1, player2, var1)
            dmg1 += bonus1
            dmg2 += bonus2

            player1['fp'] -= dmg1
            player2['fp'] -= dmg2

            print(f"{player1['name']} uses {car1['id']} ({var1}) → {stat1} (Nitro Fail: {fail1})")
            print(f"{player2['name']} uses {car2['id']} ({var2}) → {stat2} (Nitro Fail: {fail2})")
            print(f"→ {player1['name']} takes {dmg1} | {player2['name']} takes {dmg2}")
            print(f"FP: {player1['fp']} | {player2['fp']}")

            if player1['fp'] <= 0 or player2['fp'] <= 0:
                break

    print("\n🏁 MATCH END")
    if player1['fp'] > player2['fp']:
        print("🏆 WINNER: Player 1")
    elif player2['fp'] > player1['fp']:
        print("🏆 WINNER: Player 2")
    else:
        print("🤝 DRAW! Resolving by maneuverability...")
        winner = resolve_tie(player1['deck'][-1], player2['deck'][-1])
        print(f"🏁 FINAL WINNER: {winner.upper()}")


# ------------------------------
# MÓDULO 13: Visual Enhancements
# ------------------------------

def print_card_stats(card):
    print(f"  🔹 ID: {card['id']} | ⭐{card['stars']} | Model: {card['model']} | Protocol: {card['protocol']}")
    print(f"  📊 Stats → Accel: {card['accel']} | Speed: {card['speed']} | Fuel: {card['fuel']} | Brakes: {card['brakes']}")
    print(f"  💥 Nitro: {card['nitro']}")
    print("  -----------------------------")

# ✅ Estas funciones serán invocadas dentro de las rondas para mejorar el output visual

# ------------------------------
# MÓDULO 14: Testeo Batch Multijugador
# ------------------------------

def batch_test_matches(n_matches=100):
    stats = {"player1_wins": 0, "player2_wins": 0, "draws": 0, "avg_fp1": 0, "avg_fp2": 0}

    for _ in range(n_matches):
        p1, p2 = initialize_players()
        for card in p1['deck'] + p2['deck']:
            card['used_vars'] = []
            card['cooldown'] = False
            card['alt_defense_used'] = False

        play_full_rotation(p1, p2)

        if p1['fp'] > p2['fp']:
            stats['player1_wins'] += 1
        elif p2['fp'] > p1['fp']:
            stats['player2_wins'] += 1
        else:
            stats['draws'] += 1

        stats['avg_fp1'] += p1['fp']
        stats['avg_fp2'] += p2['fp']

    stats['avg_fp1'] /= n_matches
    stats['avg_fp2'] /= n_matches

    print("\n📊 Batch Test Results:")
    print(f"Player 1 Wins: {stats['player1_wins']}")
    print(f"Player 2 Wins: {stats['player2_wins']}")
    print(f"Draws: {stats['draws']}")
    print(f"Avg FP Player 1: {round(stats['avg_fp1'], 2)}")
    print(f"Avg FP Player 2: {round(stats['avg_fp2'], 2)}")


# ------------------------------
# MÓDULO 15: Filtro por Modo de Juego
# ------------------------------

def valid_deck_by_mode(deck, mode):
    star_counts = [card['stars'] for card in deck]
    count_3_star = star_counts.count(3)

    if mode == "common":
        return all(s < 3 for s in star_counts)
    elif mode == "diamond":
        return count_3_star <= 1
    elif mode == "free":
        return count_3_star <= 1
    else:
        return False

# Se usará al inicializar jugadores según el modo elegido.

# ------------------------------
# EJECUCIÓN COMPLETA DEL SISTEMA
# ------------------------------
if __name__ == "__main__":
    print("\n🚀 INICIANDO PARTIDA DE BITXEL ROADS\n")

    # Generar deck para pruebas iniciales
    print("\n🔧 TEST: DEMO DECK GENERATOR")
    deck, gadget = demo_generate_player_deck()
    for car in deck:
        print(f"\nID: {car['id']} | ⭐{car['stars']}")
        print(f"Model: {car['model']} | Protocol: {car['protocol']} | Nitro: {car['nitro']}")
        print(f"Stats → Accel: {car['accel']} | Speed: {car['speed']} | Fuel: {car['fuel']} | Brakes: {car['brakes']}")

    print("\n🧰 Gadget Assigned:")
    print(f"Name: {gadget['name']} | Mode: {gadget['mode']} | MP Cost: {gadget['cost']}")
    print(f"Effect: {gadget['effect']}")
    print(f"Synergy: {gadget['synergy']}")

    # Inicializar jugadores para partida completa
    player1, player2 = initialize_players()

    # Mostrar decks iniciales
    print("\n🧾 DECK DE PLAYER 1:")
    for car in player1['deck']:
        print_card_stats(car)

    print("\n🧾 DECK DE PLAYER 2:")
    for car in player2['deck']:
        print_card_stats(car)

    # Mostrar gadgets
    print("\n🎲 GADGETS ASIGNADOS:")
    print(f"🧰 Player 1: {player1['gadget']['name']} ({player1['gadget']['mode']}) - Cost: {player1['gadget']['cost']}")
    print(f"🧰 Player 2: {player2['gadget']['name']} ({player2['gadget']['mode']}) - Cost: {player2['gadget']['cost']}")
    
    # Ejecutar partida completa
    play_full_rotation(player1, player2)

    print("\n✅ FIN DE LA PARTIDA\n")
