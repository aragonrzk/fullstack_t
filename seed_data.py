#!/usr/bin/env python3
"""
Seed data script for PT XYZ Vehicle Inventory System.
Inserts dummy data into fs_produk table using SQLAlchemy ORM.
"""

import sys
sys.path.insert(0, '/home/santoso/Documents/fullstack')

from flask import Flask
from config import DATABASE_URL
from models import db, Produk

# Create minimal Flask app for database context
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def seed_data():
    """Insert dummy data into fs_produk table using ORM."""
    dummy_products = [
        ("Toyota", "MPV", 5, 185000000, "Toyota Avanza 2019, mulus terawat, pajak hidup"),
        ("Toyota", "SUV", 3, 285000000, "Toyota Fortuner 2018, diesel, KM rendah"),
        ("Toyota", "Sedan", 2, 145000000, "Toyota Vios 2020, automatic, silver metalik"),
        ("Daihatsu", "MPV", 7, 165000000, "Daihatsu Xenia 2019, R Deluxe, irit BBM"),
        ("Daihatsu", "SUV", 4, 195000000, "Daihatsu Terios 2019, R Adventure, 4x2"),
        ("Daihatsu", "Hatchback", 3, 125000000, "Daihatsu Ayla 2021, R Deluxe, low KM"),
        ("Honda", "MPV", 4, 205000000, "Honda Mobilio 2020, RS, automatic"),
        ("Honda", "Sedan", 2, 175000000, "Honda City 2019, RS, merah marun"),
        ("Honda", "SUV", 3, 255000000, "Honda CR-V 2018, turbo, sunroof"),
        ("Suzuki", "MPV", 6, 155000000, "Suzuki Ertiga 2020, GX, automatic"),
        ("Suzuki", "SUV", 2, 225000000, "Suzuki Grand Vitara 2017, 4x4, offroad ready"),
        ("Suzuki", "Hatchback", 5, 115000000, "Suzuki Baleno 2019, hatchback, putih"),
        ("Mitsubishi", "SUV", 3, 265000000, "Mitsubishi Pajero Sport 2018, Dakar, diesel"),
        ("Mitsubishi", "MPV", 4, 175000000, "Mitsubishi Xpander 2020, Ultimate, automatic"),
        ("Nissan", "SUV", 2, 195000000, "Nissan X-Trail 2017, 2.0, panoramic roof"),
    ]

    with app.app_context():
        try:
            # Clear existing data using ORM
            Produk.query.delete()
            db.session.commit()
            
            print("Cleared existing data.")

            # Insert dummy data using ORM
            for merek, jenis, stok, harga, keterangan in dummy_products:
                Produk.create(
                    merek=merek,
                    jenis=jenis,
                    stok=stok,
                    harga=harga,
                    keterangan=keterangan
                )

            print(f"Successfully inserted {len(dummy_products)} products into fs_produk table.")

        except Exception as e:
            db.session.rollback()
            print(f"Error seeding data: {e}")
            raise


if __name__ == "__main__":
    seed_data()
