DROP DATABASE IF EXISTS GuildWars2Bot;
CREATE DATABASE GuildWars2Bot ENCODING 'UTF8' TEMPLATE template0;
\c GuildWars2Bot;

DROP ROLE IF EXISTS bot_normal;
DROP ROLE IF EXISTS bot_admin;

CREATE EXTENSION pgcrypto;

--- API TABLE ---
DROP TABLE IF EXISTS Gw2APIKeys;
CREATE TABLE Gw2APIKeys (
    id TEXT NOT NULL UNIQUE,
    api_key TEXT
);

--- ACCOUNT INFORMATION TABLE ---
DROP TABLE IF EXISTS Gw2AccountInfo;
CREATE TABLE Gw2AccountInfo(
    id TEXT NOT NULL UNIQUE,
    account JSONB,
    achievements JSONB,
    skins JSONB,
    titles JSONB,
    minis JSONB,
    outfits JSONB,
    dyes JSONB,
    finishers JSONB,
    wallet JSONB,
    materials JSONB,
    bank JSONB,
    inventory JSONB,
    pvp JSONB,
    characters JSONB,
);
