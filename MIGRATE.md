#### `3a274762cecaf81f4fca75d96421243303792cef` (2015-06-30)

```sql
ALTER TABLE wmsclient_connection ADD COLUMN username character varying;
ALTER TABLE wmsclient_connection ADD COLUMN password character varying;
```


#### `cebcff51486370fe3fc164d38b45b7b0b58a61c8` (2015-09-21)

```sql
ALTER TABLE wfsserver_layer ADD COLUMN maxfeatures integer;
```


#### `97ad027f58f4b20453dc1cf3b32897c73a4daa3e` (2015-10-01)

```sql
ALTER TABLE auth_principal ADD COLUMN description character varying;
ALTER TABLE auth_user ADD COLUMN superuser boolean;
ALTER TABLE auth_user ALTER COLUMN superuser SET NOT NULL;
ALTER TABLE auth_user ADD COLUMN disabled boolean;
ALTER TABLE auth_user ALTER COLUMN disabled SET NOT NULL;
```