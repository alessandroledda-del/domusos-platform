# domusos-platform

**DOMUSOS** è una piattaforma PropTech per la gestione immobiliare e la verifica intelligente degli immobili ("Domus Score"). Espone un'API basata su Django REST Framework e un frontend Next.js 14.

---

## Architettura

```
domusos-platform/
├── manage.py                  # Punto di ingresso della CLI Django
├── core/                      # Pacchetto del progetto Django
│   ├── __init__.py
│   ├── urls.py                # Configurazione principale degli URL
│   ├── wsgi.py                # Applicazione WSGI
│   └── asgi.py                # Applicazione ASGI
├── backend/                   # Applicazione Django
│   ├── __init__.py
│   ├── apps.py
│   ├── settings.py            # Tutte le impostazioni Django
│   ├── models.py              # Utente, azienda, immobile
│   ├── serializers.py         # Serializer DRF
│   ├── views.py               # ViewSet DRF
│   ├── urls.py                # Router dell'API
│   ├── admin.py               # Amministrazione Django
│   ├── migrations/            # Migrazioni del database
│   ├── requirements.txt
│   └── .env.example
└── frontend/                  # App Router di Next.js 14
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx           # Reindirizza a /login o /dashboard
    │   ├── login/page.tsx
    │   ├── dashboard/page.tsx
    │   ├── users/
    │   │   ├── page.tsx       # Elenco utenti
    │   │   └── [id]/page.tsx  # Dettaglio/modifica utente
    │   ├── companies/
    │   │   ├── page.tsx       # Elenco aziende
    │   │   └── [id]/page.tsx  # Dettaglio/modifica azienda
    │   └── properties/
    │       ├── page.tsx       # Elenco immobili
    │       └── [id]/page.tsx  # Dettaglio/modifica/aggiornamento punteggio
    ├── lib/
    │   └── api-client.ts      # Client API Axios con gestione JWT
    ├── package.json
    └── .env.example
```

---

## Stack tecnologico

| Livello  | Tecnologia                                        |
|----------|---------------------------------------------------|
| Backend  | Python 3.11+, Django 4.2, DRF 3.14, Simple JWT   |
| Database | PostgreSQL 15+                                    |
| Cache/Coda | Redis, Celery                                  |
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS   |
| Autenticazione | JWT (accesso: 15 min, aggiornamento: 7 giorni, rotazione) |

---

## Prerequisiti

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis (facoltativo, per i task Celery)

---

## Configurazione del backend

### 1. Crea e attiva un ambiente virtuale

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Installa le dipendenze

```bash
pip install -r backend/requirements.txt
```

### 3. Configura le variabili d'ambiente

```bash
cp backend/.env.example .env
# Modifica .env inserendo i valori reali
```

Variabili principali:

| Variabile | Descrizione |
|---|---|
| `SECRET_KEY` | Chiave segreta Django |
| `DEBUG` | `True` per lo sviluppo |
| `DB_NAME / DB_USER / DB_PASSWORD / DB_HOST / DB_PORT` | Connessione PostgreSQL |
| `JWT_SECRET_KEY` | Chiave di firma JWT (predefinita su `SECRET_KEY`) |
| `CORS_ALLOWED_ORIGINS` | Elenco separato da virgole delle origini frontend consentite |
| `REDIS_HOST / REDIS_PORT` | Connessione Redis (per Celery) |

### 4. Crea il database

```bash
psql -U postgres -c "CREATE DATABASE domusos_db;"
```

### 5. Esegui le migrazioni

```bash
python manage.py migrate
```

### 6. Crea un superutente

```bash
python manage.py createsuperuser
```

### 7. Avvia il server di sviluppo

```bash
python manage.py runserver
```

L'API è disponibile all'indirizzo `http://localhost:8000/api/`
Il pannello di amministrazione è disponibile all'indirizzo `http://localhost:8000/admin/`

---

## Configurazione del frontend

### 1. Installa le dipendenze

```bash
cd frontend
npm install
```

### 2. Configura le variabili d'ambiente

```bash
cp .env.example .env.local
# Modifica .env.local se il backend è eseguito su un URL diverso
```

| Variabile | Descrizione |
|---|---|
| `NEXT_PUBLIC_API_URL` | URL base dell'API backend (predefinito: `http://localhost:8000/api`) |

### 3. Avvia il server di sviluppo

```bash
npm run dev
```

L'applicazione è disponibile all'indirizzo `http://localhost:3000`

---

## Endpoint API

### Autenticazione

| Metodo | Endpoint | Descrizione |
|---|---|---|
| POST | `/api/token/` | Ottiene i token JWT di accesso e aggiornamento |
| POST | `/api/token/refresh/` | Aggiorna un token di accesso |

### Utenti

| Metodo | Endpoint | Descrizione |
|---|---|---|
| GET | `/api/users/` | Elenca tutti gli utenti |
| POST | `/api/users/` | Crea un utente |
| GET | `/api/users/{id}/` | Recupera il dettaglio di un utente |
| PUT/PATCH | `/api/users/{id}/` | Aggiorna un utente |
| DELETE | `/api/users/{id}/` | Elimina un utente |
| GET | `/api/users/me/` | Recupera l'utente autenticato corrente |
| POST | `/api/users/{id}/set_password/` | Imposta una nuova password |

### Aziende

| Metodo | Endpoint | Descrizione |
|---|---|---|
| GET | `/api/companies/` | Elenca tutte le aziende |
| POST | `/api/companies/` | Crea un'azienda |
| GET | `/api/companies/{id}/` | Recupera il dettaglio di un'azienda (include gli immobili) |
| PUT/PATCH | `/api/companies/{id}/` | Aggiorna un'azienda |
| DELETE | `/api/companies/{id}/` | Elimina un'azienda |
| GET | `/api/companies/{id}/properties/` | Elenca gli immobili di un'azienda |

### Immobili

| Metodo | Endpoint | Descrizione |
|---|---|---|
| GET | `/api/properties/` | Elenca tutti gli immobili (`?company_id=` per filtrare) |
| POST | `/api/properties/` | Crea un immobile |
| GET | `/api/properties/{id}/` | Recupera il dettaglio di un immobile |
| PUT/PATCH | `/api/properties/{id}/` | Aggiorna un immobile |
| DELETE | `/api/properties/{id}/` | Elimina un immobile |
| POST | `/api/properties/{id}/update_score/` | Aggiorna il Domus Score |
| POST | `/api/properties/{id}/update_status/` | Aggiorna lo stato |
| GET | `/api/properties/by_company/?company_id=` | Recupera gli immobili di un'azienda |

Tutti gli endpoint (tranne `/api/token/`) richiedono un JWT valido nell'header `Authorization`:

```http
Authorization: JWT
```

---

## Modelli dati

### Utente

| Campo | Tipo | Descrizione |
|---|---|---|
| `email` | EmailField (univoco) | Identificativo di accesso |
| `nome` | CharField | Nome |
| `cognome` | CharField | Cognome |
| `telefono` | CharField (facoltativo) | Numero di telefono |
| `ruolo` | CharField | `admin` / `user` / `guest` |
| `stato` | CharField | `active` / `inactive` / `suspended` |

### Azienda

| Campo | Tipo | Descrizione |
|---|---|---|
| `ragione_sociale` | CharField (univoco) | Denominazione legale |
| `partita_iva` | CharField (univoco) | Partita IVA |
| `tipo_cliente` | CharField | `enterprise` / `pme` / `freelance` / `other` |
| `email` | EmailField | Email di contatto |
| `telefono` | CharField (facoltativo) | Telefono |

### Immobile

| Campo | Tipo | Descrizione |
|---|---|---|
| `company` | ForeignKey → Company | Azienda proprietaria |
| `indirizzo` | CharField | Indirizzo |
| `comune` | CharField | Comune |
| `provincia` | CharField (2 caratteri) | Sigla della provincia |
| `foglio` | CharField | Foglio catastale |
| `particella` | CharField | Particella catastale |
| `subalterno` | CharField (facoltativo) | Subalterno |
| `categoria_catastale` | CharField | Categoria catastale |
| `domus_score` | DecimalField (facoltativo) | Punteggio proprietario dell'immobile |
| `status` | CharField | `active` / `inactive` / `archived` |

---

## Esecuzione dei test

```bash
# Backend
python manage.py test backend

# Verifica dei tipi frontend
cd frontend && npm run type-check

# Lint frontend
cd frontend && npm run lint
```

---

## Deploy in produzione

1. Imposta `DEBUG=False` nel file `.env`.
2. Imposta valori robusti per `SECRET_KEY` e `JWT_SECRET_KEY`.
3. Esegui `python manage.py collectstatic`.
4. Usa **Gunicorn** come server WSGI: `gunicorn core.wsgi:application`.
5. Servi il frontend con `npm run build && npm run start` (oppure esportalo su una CDN).
6. Colloca un reverse proxy (ad esempio nginx) davanti a entrambi i servizi.
