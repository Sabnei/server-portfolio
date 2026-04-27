-- sql/init.sql
-- Corre automáticamente cuando postgres-central arranca por primera vez.
-- Para agregar un proyecto nuevo: agrega un bloque CREATE SCHEMA +
-- CREATE TABLE al final, o créalo directamente desde pgAdmin.

-- ── Schema interno de Airflow ────────────────────────────────────────
CREATE SCHEMA IF NOT EXISTS airflow_metadata;

-- ── Proyecto 1: Crypto ETL ───────────────────────────────────────────
CREATE SCHEMA IF NOT EXISTS crypto;

CREATE TABLE IF NOT EXISTS crypto.crypto_prices (
    id               SERIAL PRIMARY KEY,
    coin_id          VARCHAR(150)   NOT NULL,
    symbol           VARCHAR(50)    NOT NULL,
    name             VARCHAR(150)   NOT NULL,
    price_usd        DECIMAL(20, 8) NOT NULL,
    market_cap_usd   BIGINT,
    volume_24h       BIGINT,
    change_pct_24h   DECIMAL(8, 4),
    last_updated_api TIMESTAMPTZ,
    extracted_at     TIMESTAMPTZ    DEFAULT NOW()
);

-- ── Proyecto 2 (cuando lo hagas, descomenta y adapta) ────────────────
-- CREATE SCHEMA IF NOT EXISTS weather;
-- CREATE TABLE IF NOT EXISTS weather.observations ( ... );
