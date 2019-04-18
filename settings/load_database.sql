DROP DATABASE IF EXISTS bot;
CREATE DATABASE bot ENCODING 'UTF8' TEMPLATE template0;
\c bot;

DROP ROLE IF EXISTS bot_account;

CREATE ROLE bot_account WITH PASSWORD 'password' LOGIN;

CREATE EXTENSION pgcrypto;

--------------------------------------------------------

CREATE TABLE gw2_api_keys (
    id serial,
    discord_id text,
    gw2_api_key text
);

GRANT SELECT, INSERT, UPDATE ON gw2_api_keys TO bot_account;

CREATE TABLE builds (
    id serial,
    discord_server text,
    profession text,
    description text,
    link text
);

GRANT SELECT, INSERT, UPDATE ON builds TO bot_account;

CREATE TABLE gw2_account_activity (
    id serial NOT NULL PRIMARY KEY,
    last_active_time text,
    current_active_time text
)