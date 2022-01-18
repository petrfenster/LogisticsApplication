# Logistics Inventory Management Application

This application allows user to track the inventory, in particular:
create, delete, edit, and view products from inventory. 
Additionally, the user can create shipments and assign items from inventory
to them.

This application is specifically designed for companies that sell different
types of vehicles.

The parametrs of an inventory item include:
- id (cannot be changed, assigned automatically)
- name
- description
- type (one of 5 types: car, truck, aircraft, watercraft, train)
- price

The application has already 11 added products in its database.

This repo has been updated to work with `Python v3.8` and up.

### Instructions on how to run
1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv venv
```

3. Then run the command:
```
$ .\venv\Scripts\activate
```

4. Then install the dependencies:
```
$ (venv) pip install -r requirements.txt
```

5. Finally start the web server:
```
$ (venv) python app.py
```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)