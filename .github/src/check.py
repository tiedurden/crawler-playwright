from playwright.sync_api import sync_playwright

import requests

BOT_TOKEN = "8621775074:AAEpUuWpowryMO244Kjxq8bA7QjkVEyYIPk"
CHAT_ID = "6246159494"

URL = "https://www.baederland-shop.de/kurse"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

   

    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message + "/n " + URL
        }
    )    

    print(response.status_code) 
    print(response.text)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)

        page = browser.new_page()

        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1000)
        page.get_by_test_id("actionButton-accept").click()
        #
        # Debug: Select-Felder anzeigen
        #
        for select in page.locator("select").all():
            print(
                "SELECT:",
                select.get_attribute("id"),
                select.input_value()
            )

        #
        # Filter auswählen
        #

        # Eltern & Babys
        page.locator("#kurskategorie_id").select_option("7")

        # TODO: IDs/Werte aus Debug-Ausgabe einsetzen
        # Beispiel:
        # page.locator("#kursart_id").select_option("123")
        # page.locator("#ort_id").select_option("456")

        #
        # Suche starten
        #

        page.get_by_role("button", name="Suche starten").click()

        page.wait_for_load_state("networkidle")

        #
        # Ergebnisse prüfen
        #

        cards = page.locator("div.teaser")

        available = []

        for i in range(cards.count()):
            card = cards.nth(i)

            try:
                text = card.inner_text(timeout=500)

                if (
                    "Aqua Baby 1" in text
                    and "Festland" in text
                    and "AUSGEBUCHT" not in text
                ):
                    available.append(text)

            except:
                pass

        if available:
            print("Kurs gefunden")
            
            send_telegram(
                "🏊 Kurs verfügbar!\n\n"
                )

        else:
            send_telegram(
                "KEIN 🏊 Kurs verfügbar!\n\n"
                )
            print("Keine Plätze")
            

        browser.close()


if __name__ == "__main__":
    main()
