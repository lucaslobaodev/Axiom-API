INSERT INTO leads(
    email,
    phone,
    name
)
VALUES(
    %s,
    %s,
    %s
)
RETURNING id, name, email, phone;