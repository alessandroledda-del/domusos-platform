# API Reference

The base URL is `http://localhost:8000/api`. Except for token creation, endpoints require a valid JWT.

## Authentication

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/token/` | Obtain access and refresh tokens |
| POST | `/token/refresh/` | Rotate and refresh an access token |

Send the access token on protected requests:

```http
Use the `Authorization` header with the `Bearer` scheme and the access token.
```

## Users

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/users/` | List users |
| POST | `/users/` | Create a user |
| GET | `/users/{id}/` | Retrieve a user |
| PUT/PATCH | `/users/{id}/` | Update a user |
| DELETE | `/users/{id}/` | Delete a user |
| GET | `/users/me/` | Retrieve the authenticated user |
| POST | `/users/{id}/set_password/` | Set a user password |

## Companies

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/companies/` | List companies |
| POST | `/companies/` | Create a company |
| GET | `/companies/{id}/` | Retrieve a company and its properties |
| PUT/PATCH | `/companies/{id}/` | Update a company |
| DELETE | `/companies/{id}/` | Delete a company |
| GET | `/companies/{id}/properties/` | List a company's properties |

## Properties

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/properties/` | List properties |
| POST | `/properties/` | Create a property |
| GET | `/properties/{id}/` | Retrieve a property |
| PUT/PATCH | `/properties/{id}/` | Update a property |
| DELETE | `/properties/{id}/` | Delete a property |
| GET | `/properties/?company_id={id}` | Filter by company |
| GET | `/properties/by_company/?company_id={id}` | List properties for a company |
| POST | `/properties/{id}/update_score/` | Update `domus_score` |
| POST | `/properties/{id}/update_status/` | Update `status` |

List responses use DRF page-number pagination with a default page size of 50.

## Domain action examples

```json
POST /api/properties/12/update_score/
{"domus_score": 87.5}
```

```json
POST /api/properties/12/update_status/
{"status": "active"}
```

Valid property statuses are `active`, `inactive`, and `archived`.
