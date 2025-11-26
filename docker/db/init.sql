CREATE TABLE carteira (
    id SERIAL PRIMARY KEY,
    endereco_publico VARCHAR(128) UNIQUE NOT NULL,
    hash_chave_privada VARCHAR(256) NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL CHECK (status IN ('ATIVA', 'BLOQUEADA'))
);

CREATE TABLE moeda (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    nome VARCHAR(50) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('CRYPTO', 'FIAT'))
);

CREATE TABLE saldo_carteira (
    id SERIAL PRIMARY KEY,
    carteira_id INTEGER NOT NULL REFERENCES carteira(id),
    moeda_id INTEGER NOT NULL REFERENCES moeda(id),
    saldo NUMERIC(20,8) NOT NULL DEFAULT 0,
    UNIQUE (carteira_id, moeda_id)
);

CREATE TABLE deposito_saque (
    id SERIAL PRIMARY KEY,
    carteira_id INTEGER NOT NULL REFERENCES carteira(id),
    moeda_id INTEGER NOT NULL REFERENCES moeda(id),
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('DEPOSITO', 'SAQUE')),
    valor NUMERIC(20,8) NOT NULL,
    taxa NUMERIC(20,8) NOT NULL DEFAULT 0,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE conversao (
    id SERIAL PRIMARY KEY,
    carteira_id INTEGER NOT NULL REFERENCES carteira(id),
    moeda_origem INTEGER NOT NULL REFERENCES moeda(id),
    moeda_destino INTEGER NOT NULL REFERENCES moeda(id),
    valor_origem NUMERIC(20,8) NOT NULL,
    valor_convertido NUMERIC(20,8) NOT NULL,
    cotacao NUMERIC(20,8) NOT NULL,
    taxa NUMERIC(20,8) NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE transferencia (
    id SERIAL PRIMARY KEY,
    carteira_origem INTEGER NOT NULL REFERENCES carteira(id),
    carteira_destino INTEGER NOT NULL REFERENCES carteira(id),
    moeda_id INTEGER NOT NULL REFERENCES moeda(id),
    valor NUMERIC(20,8) NOT NULL,
    taxa NUMERIC(20,8) NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO moeda (codigo, nome, tipo) VALUES
('BTC', 'Bitcoin', 'CRYPTO'),
('ETH', 'Ethereum', 'CRYPTO'),
('SOL', 'Solana', 'CRYPTO'),
('USD', 'Dólar Americano', 'FIAT'),
('BRL', 'Real Brasileiro', 'FIAT');

CREATE USER wallet_api_homolog WITH PASSWORD 'api123';

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO wallet_api_homolog;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO wallet_api_homolog;
