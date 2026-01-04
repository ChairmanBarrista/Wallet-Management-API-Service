# The read me file specifies the various endpoints used to create,view,list, and delete wallets created

## Wallet Management API

Django REST API for managing user payment wallets (Mobile Money and Cards).

## Features

- Create, Read, Delete wallets
- Support for Mobile Money (MTN, Telecel, AT)
- Support for Cards (Visa, Mastercard)
- Business Rules: Max 5 wallets per user, no duplicates
- Token-based authentication

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `http://127.0.0.1:8000/api/token/` | Get auth token |
| POST | `/http://localhost:8000/api/wallets/create/` | Create wallet |
| GET | `/http://127.0.0.1:8000/api/wallets/` | List all wallets |
| GET | `http://127.0.0.1:8000/api/wallets/{id}/` | List single wallet |
| DELETE | `http://127.0.0.1:8000/api/wallets/{id}` | Delete wallet |

## Business Rules

1. Maximum 5 wallets per user
2. No duplicate wallets (same account number)
3. Wallet type must match scheme
