
# QueryWhiz

Chatbot capace di interpretare richieste formulate in linguaggio naturale, migliorando così l’interazione con i dati e facilitando l’accesso a informazioni più dettagliate e personalizzate.

## Come eseguire 
Innanzitutto modificare il `.env` file ed impostare il proprio ambiente di sviluppo Local o Production.

Successivamente, eseguire il seguente comando assicurandosi che Docker Desktop sia in esecuzione.
```sh
docker-compose up --build
```
Oppure, nel caso si volesse eseguire in locale eseguire il seguente comando dalla root directory
```sh
python3 -m app.main
```

Per visualizzare l'interfaccia su browser, recarsi in `/ui` ed eseguire
```sh
python -m http.server -d .
```
