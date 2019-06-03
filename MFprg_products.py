#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 20:43:29 2018

@author: diablo
"""
import mysql.connector as mariadb

def products_fetchall():
    config = {
        'user': 'admin',
        'password': 'admin',
        'database': 'db_mfox'
    }

    cnx = mariadb.connect(**config)
    cursor = cnx.cursor()

    some_supplier = 'defend'
    query = "SELECT idproduct, nameproduct, sku, priceuni FROM products WHERE idsupplier= %s"
    cursor.execute(query, (some_supplier,))
    cursor_products = cursor.fetchall()

    return cursor_products

    #return render_template ('products.html', cursor_products = cursor_products)
    #for idproduct, nameproduct, sku, priceuni in cursor:
    #    print("{} {} {} {:6.2f}".format (idproduct, nameproduct, sku, priceuni))
