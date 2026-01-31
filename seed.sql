INSERT INTO Users(userID, username, password, employee) 
VALUES(NULL, 'c', '$argon2id$v=19$m=65536,t=3,p=4$Ke/TpTYtxBmHNSZwzqC8Rg$u7RHJuIbPOYNu5+ZzyaQzsLV2StzIHn5DDeawlEqRsU', '0'), --Passordet er customer
(NULL, 'e', '$argon2id$v=19$m=65536,t=3,p=4$KQqCQg3RmFkKZlX47KXnxw$K9/J6u2O+hQ9E4m234NI6N+peQmu/+2NCs6TnyQVdsU', '1'); --passordet er employee

INSERT INTO burgers(burgerID, burgName) 
VALUES(NULL, 'Whopper Queen'),
(NULL, 'Triple Cheesy Princess'),
(NULL, 'Kingdom Fries');

INSERT INTO burgIngredients(burgerID, ingredients) 
VALUES
(1, 1),
(1, 2),
(1, 4),
(1, 5);

INSERT INTO burgIngredients(burgerID, ingredients) 
VALUES
(2, 1),
(2, 2),
(2, 3),
(2, 4),
(2, 5);

INSERT INTO burgIngredients(burgerID, ingredients) 
VALUES
(3, 7);
 
INSERT INTO ingredients (ingredID, ingredName, quantityStorage)
VALUES(NULL, "breadTopBottom", 50),
(NULL, "burgerPatty", 75),
(NULL, "cheese", 120),
(NULL, "lettuce", 30),
(NULL, "tomato", 40),
(NULL, "cucumber", 20),
(NULL, "potato", 10);