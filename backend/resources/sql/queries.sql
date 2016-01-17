-- name: create-user!
-- creates a new user record
INSERT INTO users
(id, first_name, last_name, email, pass)
VALUES (:id, :first_name, :last_name, :email, :pass)

-- name: update-user!
-- update an existing user record
UPDATE users
SET first_name = :first_name, last_name = :last_name, email = :email
WHERE id = :id

-- name: get-user
-- retrieve a user given the id.
SELECT * FROM users
WHERE id = :id

-- name: delete-user!
-- delete a user given the id
DELETE FROM users
WHERE id = :id

-- name: list-actor
-- list all existing actors
select name from Actor;

-- name: get-actor
-- Get information for a specificed actor
select information from Actor where name = :name;

-- name: create-actor!
-- create a new actor
insert into actor (Name, Avatar, Information) values (:name, :avatar, :information);

-- name: get-config
-- query configuration
select value from config where name = :name;

-- name: clear-db!
-- Clear database
delete from actor;

-- name: set-config!
-- set configuration
merge into config values (:name, :value);
