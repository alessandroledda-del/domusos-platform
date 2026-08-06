# Ciclo di vita ordine

## Stati

1. `DRAFT`
2. `AWAITING_PAYMENT`
3. `PAID`
4. `IN_PROGRESS`
5. `WAITING_CUSTOMER`
6. `COMPLETED`

Stati terminali alternativi:

- `CANCELLED`
- `REFUNDED`

## SLA

Lo SLA viene calcolato al pagamento usando il valore più alto
tra gli SLA dei servizi presenti nell'ordine.

## Generazione pratica

Quando l'ordine passa a `PAID` e contiene un immobile:

- viene creata una pratica;
- viene creata un'attività per ogni servizio;
- la scadenza è allineata allo SLA dell'ordine.

## Transizioni

Le transizioni sono validate dal servizio applicativo
`apps.orders.services.transition_order`.
