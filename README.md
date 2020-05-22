API for Irish whisky bar ordering system.

xxx/api:

token/  	- Used for logging in- username password	[POST]
token/refresh/ 		- Used to refresh token			[POST]

These require the access token from jwt in the Authorization header:

orders/ 	- Bartenders can view orders 			[GET]
orders/pk/	- Bartenders can change paid/completed state	[PATCH]
orders/		- Customers can make an order			[POST]

items/		- User can view items 				[GET]
items/pk	- Bartender can mark item as out of stock	[PATCH]
