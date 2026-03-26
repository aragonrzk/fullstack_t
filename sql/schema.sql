-- Database Schema for PT XYZ Vehicle Inventory System
-- Table: fs_produk

DROP TABLE IF EXISTS fs_produk;

CREATE TABLE fs_produk (
    id SERIAL PRIMARY KEY,
    merek VARCHAR(100) NOT NULL,
    jenis VARCHAR(100) NOT NULL,
    stok INTEGER NOT NULL DEFAULT 0,
    harga DECIMAL(15, 2) NOT NULL,
    keterangan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster search by merek
CREATE INDEX idx_fs_produk_merek ON fs_produk(merek);
