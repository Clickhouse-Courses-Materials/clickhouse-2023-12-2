## dbt setup

1. Install dbt using [these instructions](https://docs.getdbt.com/docs/installation).

1. Set up a profile to connect to a data warehouse by following [these instructions](https://docs.getdbt.com/docs/configure-your-profile). 
If you have access to a data warehouse, you can use those credentials – we recommend setting your [target schema](https://docs.getdbt.com/docs/configure-your-profile#section-populating-your-profile) 
to be a new schema (dbt will create the schema for you, as long as you have the right privileges). 
If you don't have access to an existing data warehouse, you can also setup a local postgres database and connect to it in your profile.

1. Ensure your profile is setup correctly from the command line:
```bash
$ dbt debug
```

## Operation DB model:

The raw data consists of customers, orders, and payments, with the following entity-relationship diagram:

![ERD](./shop_erd.png)

```sql
Table orders {
id int PK
user_id int
order_date date
status varchar
}

Table payments {
id int
order_id int
payment_method int
amount int
}

Table customers {
id int PK
first_name varchar
last_name varchar
}
```

Orders can be one of the following statuses:

- **status**	description
- **placed**	The order has been placed but has not yet left the warehouse
- **shipped**	The order has ben shipped to the customer and is currently in transit
- **completed**	The order has been received by the customer
- **return_pending**	The customer has indicated that they would like to return the order, but it has not yet been received at the warehouse
- **returned**	The order has been returned by the customer and received at the warehouse

Load the CSVs with the demo data set. This materializes the CSVs as tables in your target schema.
Note that a typical dbt project does not require this step since dbt assumes your raw data is already in your warehouse.

```shell
dbt seed
```

## Stage area

```sql
Ref: orders.user_id > customers.id

Ref: payments.order_id > orders.id
```

1. Run the models:
```bash
$ dbt run
```

> **NOTE:** If this steps fails, it might mean that you need to make small changes to the SQL in the models folder to adjust for the flavor of SQL of your target database. 
> Definitely consider this if you are using a community-contributed adapter.

1. Test the output of the models:
```bash
$ dbt test
```

## DDS

```text
order_id | creadit_card_amount | gift_card_amount | total
1        |     1000     | 0         | 1000
```
Необходимо реализовать следующие агрегации:
1. Для каждого платежного метода посчитать сумму для каждого заказа (отдельная колонка для каждого платежного метода), 
а также посчитать общую сумму платежей по заказу. Вывести полную информацию о заказе.
2. На основании данных заказов пользователей найти: первый заказ, самый последний заказ, количество заказов пользователя.
На основании платежей найти общую сумму заказов пользователя. Вывести полную информацию о пользователе.

---
For more information on dbt:
- Read the [introduction to dbt](https://docs.getdbt.com/docs/introduction).
- Read the [dbt viewpoint](https://docs.getdbt.com/docs/about/viewpoint).
- Join the [dbt community](http://community.getdbt.com/).
---

1. Generate documentation for the project:
```bash
$ dbt docs generate
```

1. View the documentation for the project:
```bash
$ dbt docs serve
```
