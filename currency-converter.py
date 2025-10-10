
import os
from requests import get
from pprint import PrettyPrinter


BASE_URL = "https://free.currconv.com/"
API_KEY = os.getenv("CURRENCY_API_KEY")

printer = PrettyPrinter()


def get_currencies():
    """Recupera la lista delle valute disponibili dall'API."""
    if not API_KEY:
        print("Errore: la variabile d'ambiente CURRENCY_API_KEY non è impostata.")
        return []

    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json().get('results', {})

    data = list(data.items())
    data.sort()

    return data


def print_currencies(currencies):
    """Stampa le valute in formato leggibile."""
    for _, currency in currencies:
        name = currency['currencyName']
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")
        print(f"{_id} - {name} - {symbol}")


def exchange_rate(currency1, currency2):
    """Ottiene il tasso di cambio tra due valute."""
    if not API_KEY:
        print("Errore: chiave API mancante.")
        return None

    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()

    if len(data) == 0:
        print('Valute non valide.')
        return None

    rate = list(data.values())[0]
    print(f"{currency1} -> {currency2} = {rate}")

    return rate


def convert(currency1, currency2, amount):
    """Converte un importo da una valuta a un'altra."""
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return

    try:
        amount = float(amount)
    except ValueError:
        print("Importo non valido.")
        return

    converted_amount = rate * amount
    print(f"{amount} {currency1} = {converted_amount} {currency2}")
    return converted_amount


def main():
    """Interfaccia principale del programma."""
    currencies = get_currencies()

    print("💱 Benvenuto nel Currency Converter!")
    print("Comandi disponibili:")
    print("  list     → mostra le valute disponibili")
    print("  convert  → converte un importo tra due valute")
    print("  rate     → mostra il tasso di cambio")
    print("  q        → esce dal programma")
    print()

    while True:
        command = input("Inserisci un comando: ").lower().strip()

        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Valuta di partenza (es. USD): ").upper()
            amount = input(f"Importo in {currency1}: ")
            currency2 = input("Valuta di destinazione (es. EUR): ").upper()
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Valuta di partenza: ").upper()
            currency2 = input("Valuta di destinazione: ").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Comando non riconosciuto.")


if __name__ == "__main__":
    main()
