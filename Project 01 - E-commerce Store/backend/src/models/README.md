# models/

Put Mongoose models here (for example `User.js`, `Product.js`).
See the project `DATA_MODEL.md` for schemas.

## Seed data

Run these commands from the `backend` directory:

```sh
node seedProducts.js
node seedAdmin.js
```

`seedProducts.js` inserts eight sample products. 
`seedAdmin.js` inserts an administrator account.

## Verify the data in Atlas

1. In Atlas, open **Browse Collections** for the cluster.
2. Select the database named in the path portion of `MONGO_URI` (creating it
   implicitly when the first seed data is inserted).
3. Open the `products` collection and confirm the sample product documents are
   present.
4. Open the `users` collection and confirm an account with the `admin` role is
   present. Do not share or expose its password-related fields.



