import random
import time
import os

# Generazione automatica dei livelli standard (0-300)
LIVELLI = {
    i: {
        "nome": f"Level {i}",
        "pericolo": random.randint(1, 10),
        "prob_risorse": random.uniform(0.5, 0.9),
        "descrizione": f"Livello {i} delle Backrooms"
    } for i in range(301)
}

# Aggiunta livelli negativi (-1 to -100)
LIVELLI.update({
    -i: {
        "nome": f"Level -{i}",
        "pericolo": random.randint(3, 10),
        "prob_risorse": random.uniform(0.6, 0.95),
        "descrizione": f"Livello negativo -{i}"
    } for i in range(1, 101)
})

# Sovrascrittura dei livelli speciali con dettagli specifici
LIVELLI_SPECIALI = {
    0: {"nome": "Level 0 - The Lobby", "pericolo": 1, "prob_risorse": 0.7, 
        "descrizione": "Infiniti uffici vuoti con moquette umida e pareti gialle"},
    1: {"nome": "Level 1 - Magazzino", "pericolo": 2, "prob_risorse": 0.8, 
        "descrizione": "Magazzino industriale infinito con casse misteriose"},
    "!": {"nome": "Level ! - Run For Your Life", "pericolo": 10, "prob_risorse": 0.99, 
          "descrizione": "Corri. Non fermarti. Non guardare indietro."},
    "Fun": {"nome": "Level Fun =)", "pericolo": 10, "prob_risorse": 0.95, 
            "descrizione": "Una festa infinita dove nessuno dovrebbe entrare"},
    "Hub": {"nome": "The Hub", "pericolo": 1, "prob_risorse": 0.8, 
            "descrizione": "Centro di scambio e rifugio per esploratori"},
    "Poolrooms": {"nome": "The Poolrooms", "pericolo": 3, "prob_risorse": 0.7, 
                  "descrizione": "Infinite piscine con acqua tiepida e piastrelle bianche"},
    "Endless City": {"nome": "The Endless City", "pericolo": 6, "prob_risorse": 0.85, 
                     "descrizione": "Una metropoli abbandonata che si estende all'infinito"},
    "Blackout": {"nome": "Level Blackout", "pericolo": 8, "prob_risorse": 0.9, 
                 "descrizione": "Oscurità totale e suoni inquietanti"},
    "Death": {"nome": "Level Death", "pericolo": 10, "prob_risorse": 1.0, 
              "descrizione": "Il livello più pericoloso conosciuto"},
    "Crimson Forest": {"nome": "The Crimson Forest", "pericolo": 7, "prob_risorse": 0.8, 
                       "descrizione": "Una foresta infinita di alberi rosso sangue"}
}

# Aggiornamento del dizionario principale con i livelli speciali
LIVELLI.update(LIVELLI_SPECIALI)

# Database esteso delle entità
ENTITA = {
    # Entità comuni
    "bacteria": {"nome": "Bacteria", "danno": 15, "hp": 40, 
                "descrizione": "Masse gelatinose fluttuanti"},
    "hound": {"nome": "Hound", "danno": 20, "hp": 50, 
              "descrizione": "Creature simili a cani deformi"},
    "skin_stealer": {"nome": "Skin Stealer", "danno": 40, "hp": 80, 
                     "descrizione": "Entità che rubano la pelle delle vittime"},
    "smiler": {"nome": "Smiler", "danno": 60, "hp": 100, 
               "descrizione": "Sorrisi luminosi nel buio"},
    "partygoer": {"nome": "Partygoer", "danno": 30, "hp": 70, 
                  "descrizione": "Esseri festosi con facce sorridenti"},
    
    # Entità rare
    "beast_of_level_7": {"nome": "Beast of Level 7", "danno": 80, "hp": 200, 
                         "descrizione": "Mostro leggendario del livello 7"},
    "window_walker": {"nome": "Window Walker", "danno": 45, "hp": 90, 
                     "descrizione": "Creature che attraversano le finestre"},
    "death_moth": {"nome": "Death Moth", "danno": 50, "hp": 70, 
                   "descrizione": "Falene giganti letali"},
    
    # Boss entities
    "master_partygoer": {"nome": "Master Partygoer", "danno": 100, "hp": 300, 
                         "descrizione": "Il re delle feste infinite"},
    "void_walker": {"nome": "Void Walker", "danno": 120, "hp": 400, 
                    "descrizione": "Entità che manipola lo spazio stesso"},
    
    # Entità neutrali
    "trader": {"nome": "Trader", "danno": 0, "hp": 50, 
               "descrizione": "Commerciante misterioso"},
    "wanderer": {"nome": "Wanderer", "danno": 0, "hp": 60, 
                 "descrizione": "Esploratore solitario"},
    
    # Entità specifiche per livello
    "poolrooms_swimmer": {"nome": "Poolrooms Swimmer", "danno": 35, "hp": 80, 
                         "descrizione": "Nuotatore deforme nelle Poolrooms"},
    "city_stalker": {"nome": "City Stalker", "danno": 55, "hp": 120, 
                     "descrizione": "Predatore urbano dell'Endless City"}
}

# Generazione automatica di altre entità per raggiungere almeno 50
for i in range(30):
    nome_entita = f"entity_{i}"
    ENTITA[nome_entita] = {
        "nome": f"Entità {i}",
        "danno": random.randint(20, 100),
        "hp": random.randint(50, 200),
        "descrizione": f"Misteriosa entità scoperta nelle Backrooms"
    }

class Agente:
    def __init__(self, tipo):
        self.tipo = tipo
        self.hp = 100
        self.esperienza = 0
        self.specializzazione = random.choice([
            "Combattente", "Esploratore", "Medico", 
            "Ricercatore", "Sopravvissuto", "Cartografo",
            "Negoziatore", "Cacciatore di Entità"
        ])
        self.livelli_esplorati = set()
        self.entita_sconfitte = {}
        self.oggetti = []
        self.abilita_speciali = []

class MEGManager:
    def __init__(self):
        self.supplies = 100
        self.agenti = [Agente("Veterano") for _ in range(5)]
        self.almond_water = 50
        self.giorno = 1
        self.sicurezza_base = 100
        self.livelli_scoperti = [0]
        self.conoscenza_accumulata = 0
        self.reputazione = 50
        self.alleanze = set()
        self.tecnologie = set()
        self.base_upgrades = set()
        self.missioni_attive = []
        self.log_esplorazioni = []
        self.mappa_generata = set()
    
    scelta = input("\nScegli un agente da addestrare (0 per tornare): ")
    if scelta.isdigit() and 0 < int(scelta) <= len(self.agenti):
        agente = self.agenti[int(scelta)-1]
        costo = 10
        if self.supplies >= costo:
            self.supplies -= costo
            exp_guadagnata = random.randint(5, 15)
            agente.esperienza += exp_guadagnata
            print(f"\nAddestramento completato! +{exp_guadagnata} EXP")
        else:
            print("\nRisorse insufficienti per l'addestramento!")

    def genera_evento_casuale(self):
        eventi = [
            ("anomalia_spaziale", "Una distorsione spaziale ha creato un nuovo passaggio"),
            ("invasione_entita", "Un gruppo di entità sta attaccando la base"),
            ("sopravvissuti", "Trovato un gruppo di sopravvissuti"),
            ("tecnologia", "Scoperta una nuova tecnologia delle Backrooms"),
            ("portale", "Apparso un portale misterioso"),
            ("commerciante", "Un commerciante misterioso è arrivato alla base")
        ]
        return random.choice(eventi)

    def gestisci_combattimento_avanzato(self, entita_nome):
        entita = ENTITA[entita_nome].copy()
        squadra_combattimento = [a for a in self.agenti if a.specializzazione in ["Combattente", "Cacciatore di Entità"]]
        
        print(f"\nSCONTRO CON {entita['nome'].upper()}!")
        print(f"Descrizione: {entita['descrizione']}")
        
        bonus_squadra = len(squadra_combattimento) * 5
        while entita['hp'] > 0:
            # Sistema di combattimento a turni
            for agente in squadra_combattimento:
                danno_base = random.randint(15, 25)
                danno_bonus = bonus_squadra + (agente.esperienza // 10)
                danno_totale = danno_base + danno_bonus
                
                entita['hp'] -= danno_totale
                print(f"{agente.specializzazione} infligge {danno_totale} danni!")
                
                if entita['hp'] <= 0:
                    break
                
                # Contrattacco dell'entità
                danno_subito = random.randint(entita['danno'] // 2, entita['danno'])
                agente.hp -= danno_subito
                print(f"{agente.specializzazione} subisce {danno_subito} danni!")
                
                if agente.hp <= 0:
                    print(f"Un {agente.specializzazione} è caduto in combattimento!")
                    self.agenti.remove(agente)
                    if not squadra_combattimento:
                        return False
            
            time.sleep(0.5)
        
        print(f"\nVITTORIA! {entita['nome']} è stato sconfitto!")
        self.gestisci_ricompense(entita_nome)
        return True

    def gestisci_ricompense(self, entita_nome):
        ricompense = {
            "supplies": random.randint(20, 100),
            "almond_water": random.randint(5, 25),
            "esperienza": random.randint(10, 30)
        }
        
        print("\nRicompense ottenute:")
        for risorsa, quantita in ricompense.items():
            if risorsa == "supplies":
                self.supplies += quantita
                print(f"+ {quantita} supplies")
            elif risorsa == "almond_water":
                self.almond_water += quantita
                print(f"+ {quantita} almond water")
            elif risorsa == "esperienza":
                for agente in self.agenti:
                    agente.esperienza += quantita
                print(f"+ {quantita} esperienza per ogni agente")

    def esplora_livello_avanzato(self, livello_id):
        livello = LIVELLI[livello_id]
        print(f"\nESPLORAZIONE DI {livello['nome'].upper()}")
        print(f"Descrizione: {livello['descrizione']}")
        
        # Probabilità di eventi basata sul pericolo del livello
        prob_evento = livello['pericolo'] / 10
        
        # Eventi possibili durante l'esplorazione
        eventi_esplorazione = [
            self.trova_risorse,
            self.incontra_entita,
            self.scopri_segreto,
            self.trova_tecnologia,
            self.incontra_sopravvissuti
        ]
        
        for _ in range(3):  # 3 eventi per esplorazione
            if random.random() < prob_evento:
                evento = random.choice(eventi_esplorazione)
                evento(livello)
            
            time.sleep(1)
        
        # Aggiornamento della mappa
        self.mappa_generata.add(livello_id)
        
        # Possibilità di scoprire nuovi livelli collegati
        self.scopri_livelli_collegati(livello_id)

    def gioca_turno(self):
        self.mostra_stato()
        
        print("\nAZIONI DISPONIBILI:")
        print("1. Esplora livello")
        print("2. Gestisci base")
        print("3. Addestra agenti")
        print("4. Ricerca tecnologie")
        print("5. Diplomazia")
        print("6. Termina giorno")
        
        scelta = input("\nScegli un'azione (1-6): ")
        
        if scelta == "1":
            self.menu_esplorazione()
        elif scelta == "2":
            self.menu_gestione_base()
        elif scelta == "3":
            self.menu_addestramento()
        elif scelta == "4":
            self.menu_ricerca()
        elif scelta == "5":
            self.menu_diplomazia()
        elif scelta == "6":
            self.concludi_giorno()

    def menu_esplorazione(self):
        print("\nLIVELLI DISPONIBILI:")
        for i, livello_id in enumerate(sorted(self.livelli_scoperti)):
            print(f"{i+1}. {LIVELLI[livello_id]['nome']} - Pericolo: {LIVELLI[livello_id]['pericolo']}")
        
        scelta = input("\nScegli un livello (numero) o 0 per tornare: ")
        if scelta.isdigit() and 0 < int(scelta) <= len(self.livelli_scoperti):
            self.esplora_livello_avanzato(self.livelli_scoperti[int(scelta)-1])

    def menu_gestione_base(self):
        print("\nGESTIONE BASE:")
        print("1. Potenzia difese")
        print("2. Costruisci strutture")
        print("3. Gestisci risorse")
        print("4. Cura agenti")
        
        scelta = input("\nScegli azione: ")
        if scelta == "1":
            self.potenzia_difese()
        elif scelta == "2":
            self.costruisci_strutture()
        elif scelta == "3":
            self.gestisci_risorse()
        elif scelta == "4":
            self.cura_agenti()

    def menu_addestramento(self):
        print("\nADDESTRAMENTO AGENTI:")
        print("\nAgenti disponibili:")
        for i, agente in enumerate(self.agenti, 1):
            print(f"{i}. {agente.specializzazione} - HP: {agente.hp} - EXP: {agente.esperienza}")
        
        scelta = input("\nScegli un agente da addestrare (0 per tornare): ")
        if scelta.isdigit() and 0 < int(scelta) <= len(self.agenti):
            agente = self.agenti[int(scelta)-1]
            costo = 10
            if self.supplies >= costo:
                self.supplies -= costo
                exp_guadagnata = random.randint(5, 15)
                agente.esperienza += exp_guadagnata
                print(f"\nAddestramento completato! +{exp_guadagnata} EXP")
            else:
                print("\nRisorse insufficienti per l'addestramento!")

    def trova_risorse(self, livello):
        quantita = random.randint(10, 50) * livello['prob_risorse']
        tipo_risorsa = random.choice(['supplies', 'almond_water', 'tecnologia'])
        if tipo_risorsa == 'supplies':
            self.supplies += quantita
            print(f"\nTrovati {int(quantita)} supplies!")
        elif tipo_risorsa == 'almond_water':
            self.almond_water += quantita
            print(f"\nTrovati {int(quantita)} Almond Water!")
        else:
            self.tecnologie.add(f"Tech_{len(self.tecnologie)+1}")
            print("\nScoperta nuova tecnologia!")

    def incontra_entita(self, livello):
        prob_incontro = livello['pericolo'] / 10
        if random.random() < prob_incontro:
            entita = random.choice(list(ENTITA.keys()))
            self.gestisci_combattimento_avanzato(entita)

    def scopri_segreto(self, livello):
        segreti = [
            "Antichi simboli sulle pareti",
            "Documenti classificati",
            "Registrazioni misteriose",
            "Oggetti anomali",
            "Tracce di esperimenti"
        ]
        scoperta = random.choice(segreti)
        self.conoscenza_accumulata += 1
        print(f"\nSCOPERTA: {scoperta}")

    def trova_tecnologia(self, livello):
        if random.random() < 0.3:
            tech = f"Tecnologia_{len(self.tecnologie)+1}"
            self.tecnologie.add(tech)
            print(f"\nScoperta nuova tecnologia: {tech}")

    def incontra_sopravvissuti(self, livello):
        if random.random() < 0.2:
            nuovi_agenti = random.randint(1, 3)
            for _ in range(nuovi_agenti):
                self.agenti.append(Agente("Sopravvissuto"))
            print(f"\nTrovati {nuovi_agenti} sopravvissuti! Si uniscono al team.")

    def scopri_livelli_collegati(self, livello_attuale):
        livelli_possibili = [l for l in LIVELLI.keys() if l not in self.livelli_scoperti]
        if livelli_possibili and random.random() < 0.3:
            nuovo_livello = random.choice(livelli_possibili)
            self.livelli_scoperti.append(nuovo_livello)
            print(f"\nScoperto nuovo livello: {LIVELLI[nuovo_livello]['nome']}!")

    def check_game_over(self):
        if len(self.agenti) <= 0:
            print("\nTutti gli agenti sono stati persi. Game Over.")
            return True
        if self.supplies <= 0 and self.almond_water <= 0:
            print("\nRisorse esaurite. Game Over.")
            return True
        if self.sicurezza_base <= 0:
            print("\nLa base è stata distrutta. Game Over.")
            return True
        return False

    def concludi_giorno(self):
        self.giorno += 1
        self.consuma_risorse()
        evento, descrizione = self.genera_evento_casuale()
        print(f"\nEVENTO GIORNALIERO: {descrizione}")
        self.gestisci_evento(evento)
        
        # Recupero agenti
        for agente in self.agenti:
            agente.hp = min(100, agente.hp + 10)

    def consuma_risorse(self):
        consumo_base = len(self.agenti) * 2
        self.supplies = max(0, self.supplies - consumo_base)
        self.almond_water = max(0, self.almond_water - len(self.agenti))

    def gestisci_evento(self, evento):
        if evento == "anomalia_spaziale":
            if random.random() < 0.5:
                self.scopri_livelli_collegati(random.choice(self.livelli_scoperti))
        elif evento == "invasione_entita":
            self.sicurezza_base -= random.randint(10, 30)
            print(f"La sicurezza della base è scesa a {self.sicurezza_base}%")
        elif evento == "sopravvissuti":
            self.incontra_sopravvissuti({"pericolo": 1})
        elif evento == "tecnologia":
            self.trova_tecnologia({"pericolo": 1})
        elif evento == "commerciante":
            self.commercia()

    def commercia(self):
        print("\nCOMMERCIANTE MISTERIOSO")
        offerte = [
            ("20 supplies", "10 almond water", 1),
            ("Tecnologia misteriosa", "50 supplies", 2),
            ("Nuovo agente", "30 supplies + 20 almond water", 3)
        ]
        
        print("Offerte disponibili:")
        for i, (ottieni, costo, _) in enumerate(offerte, 1):
            print(f"{i}. Ottieni: {ottieni} - Costa: {costo}")
        
        scelta = input("\nScegli un'offerta (0 per rifiutare): ")
        if scelta.isdigit() and 0 < int(scelta) <= len(offerte):
            self.processa_commercio(offerte[int(scelta)-1])

    def processa_commercio(self, offerta):
        ottieni, costo, tipo = offerta
        if tipo == 1 and self.almond_water >= 10:
            self.almond_water -= 10
            self.supplies += 20
            print("Scambio completato!")
        elif tipo == 2 and self.supplies >= 50:
            self.supplies -= 50
            self.tecnologie.add(f"Tech_commerciante_{len(self.tecnologie)}")
            print("Tecnologia acquisita!")
        elif tipo == 3 and self.supplies >= 30 and self.almond_water >= 20:
            self.supplies -= 30
            self.almond_water -= 20
            self.agenti.append(Agente("Mercenario"))
            print("Nuovo agente reclutato!")
        else:
            print("Risorse insufficienti per lo scambio!")

    def mostra_stato(self):
        self.clear_screen()
        print(f"\n=== M.E.G. Base - Giorno {self.giorno} ===")
        print(f"Agenti: {len(self.agenti)}")
        print(f"Supplies: {self.supplies}")
        print(f"Almond Water: {self.almond_water}")
        print(f"Sicurezza Base: {self.sicurezza_base}%")
        print(f"Livelli Scoperti: {len(self.livelli_scoperti)}")
        print(f"Tecnologie: {len(self.tecnologie)}")
        print("=" * 40)

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

def main():
    print("=== M.E.G. Manager v2.0 ===")
    print("Benvenuto nel simulatore di gestione M.E.G.")
    print("Esplora le Backrooms, sopravvivi alle entità, scopri i misteri.")
    input("\nPremi INVIO per iniziare...")
    
    game = MEGManager()
    
    while not game.check_game_over():
        game.gioca_turno()
    
    print("\nGAME OVER")
    print(f"Sei sopravvissuto per {game.giorno} giorni")
    print(f"Livelli scoperti: {len(game.livelli_scoperti)}")
    print(f"Conoscenza accumulata: {game.conoscenza_accumulata}")

if __name__ == "__main__":
    main()
