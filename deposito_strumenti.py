class Strumento :#oggetto strumento
    def __init__(self,id_strumento,tipo,marca,anno_acquisto,valore):#costruttore
        self.id_strumento = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):#serve per fare un output ben comprensibile
        return f"{self.id_strumento}-{self.tipo}-{self.marca}-{self.anno_acquisto}-{self.valore}"
class Prestito:#oggetto prestito
    def __init__(self,codice_prestito,data, codice_strumento, cognome_allievo):
        self.data = data
        self.codice_prestito = codice_prestito
        self.cognome_allievo = cognome_allievo
        self.codice_strumento = codice_strumento

    def __str__(self):
        return f"{self.codice_prestito}-{self.data}-{self.codice_strumento}-{self.cognome_allievo}"

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            file_strumenti = open(file_path, "r")
            for riga in file_strumenti:
                riga = riga.strip()
                pezzo = riga.split(",")
                s = Strumento(pezzo[0], pezzo[1], pezzo[2], int(pezzo[3]), float(pezzo[4]))
                self.strumenti.append(s)#carico ogni riga del file nella lista strumenti
            file_strumenti.close()
        except FileNotFoundError:
            raise FileNotFoundError#se non trovo il file scateno errore


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        massimo = 0
        for strumento in self.strumenti:
            codice = strumento.id_strumento
            numero = int(codice[1:]) #poiche la variabile codice arriva cosi S1, gli diciamo di saltare la posizione 0 che
                                    #è la S e convertire le cifre dopo la S in numuro cosi da poterle confrontare tra loro
            if numero > massimo:
                massimo = numero
        massimo +=1
        id_strumento=(f"S{massimo}")#creo il nuovo id mettendo S e le cifre massime
        marca = marca.capitalize()#funzione che converte la prima lettera maiuscola e le altre minuscole , perchè senno da problemi nell'ordinamento del file tra lettere minuscole emaiuscole
        s= Strumento(id_strumento, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(s)#aggiungo il nuovo strumento nella lista
        return s


    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        from operator import attrgetter
        strumenti_ordinati = sorted(self.strumenti,key=attrgetter("marca"))#ordino la lista per la marca , gli passo prima la lista iniziale e poi per che coss voglio ordinare con attrgetter
        return strumenti_ordinati


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # guardo se esiste gia  lo strumento
        trovato = False
        for strumento in self.strumenti:
            if strumento.id_strumento == id_strumento:
                trovato = True
        if trovato==False:
            raise Exception("Strumento non presente")

        #guardo se è già in prestito
        for prestito in self.prestiti:
            if prestito.codice_strumento == id_strumento:
                raise Exception("Strumento gia' in prestito")

        # se non si scatena eccezione genera un nuovo prestito
        massimo = 0
        for prestito in self.prestiti:
            numero = int(prestito.id_prestito[1:])#come quello creato nella funzione aggiungi strumento
            if numero > massimo:
                massimo = numero
        massimo += 1
        codice_prestito = f"P{massimo}"

        prenotazione = Prestito(codice_prestito, data, id_strumento, cognome_allievo)
        self.prestiti.append(prenotazione)#aggingo  la prenotazione nella lista prestiti
        return prenotazione




    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        #guardo se il prestito esiste(ritorno True) e no (ritorno false)
        trovato = False
        for prestito in self.prestiti:
            if prestito.codice_prestito == id_prestito:
                trovato =True
        if trovato==False:
            raise Exception("Strumento non trovato")

        #termino il prestito togliendolo dalla lista prestiti
        for i in range(len(self.prestiti)):
            if self.prestiti[i].codice_prestito == id_prestito:
                self.prestiti.pop(i)


