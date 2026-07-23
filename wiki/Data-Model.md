# Data Model

## User

The custom `User` model uses email as its login identifier and removes the default username field.

| Field | Description |
| --- | --- |
| `email` | Unique login email |
| `nome`, `cognome` | First and last name |
| `telefono` | Optional phone number |
| `ruolo` | `admin`, `user`, or `guest` |
| `stato` | `active`, `inactive`, or `suspended` |
| `created_at`, `updated_at` | Audit timestamps |

## Company

Companies own properties through a foreign-key relationship.

| Field | Description |
| --- | --- |
| `ragione_sociale` | Unique legal name |
| `partita_iva` | Unique VAT number |
| `tipo_cliente` | `enterprise`, `pme`, `freelance`, or `other` |
| `email` | Contact email |
| `telefono` | Optional phone number |

## Property

Each property belongs to one company.

| Field | Description |
| --- | --- |
| `company` | Owning company |
| `indirizzo`, `comune`, `provincia` | Location |
| `foglio`, `particella`, `subalterno` | Land-registry identifiers |
| `categoria_catastale` | Cadastral category |
| `domus_score` | Optional decimal score |
| `status` | `active`, `inactive`, or `archived` |

Deleting a company cascades to its properties.
