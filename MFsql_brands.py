#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  27 20:30:29 2018

@author: diablo
"""
from flask import flash
from wtforms import Form, StringField
from mysql.connector.errors import Error
import mysql.connector as mariadb

def sql_brands(config, option, key):

    cnx = mariadb.connect(**config)
    cur = cnx.cursor()

    if option == 'cursor':

        query = "SELECT * FROM MFbrands"
        cur.execute(query)
        cursor_brands = cur.fetchall()
        cur.close()
        cnx.close()
        return cursor_brands

    elif option == 'ins':
        sql = "INSERT INTO MFbrands( brand, totalproducts, totalsales, totalpurchases, usercreate, datecreate, userlastupdate, datelastupdate ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (key, 0,0,0,'admin','2017-01-01 00:00:01','admin','2017-01-01 00:00:01')
        #print (sql, data)
        result = 0
        try:
            try:
                cur.execute(sql,data)
            except (mariadb.Error, mariadb.Warning) as err:
                if Error(errno=2006):
                    print("Bran exist: {}".format(err))
                    flash('Brand name Exist', 'success')
                else:
                    print("Oops! There was an error: {}".format(err))
                    flash('Oops! There was an error', 'success')
                result = 1
        finally:
            cnx.commit()
            cur.close()
            cnx.close()
        return result

    elif option == 'get':
        sql = "SELECT * FROM MFbrands WHERE brand = %s"
        cur.execute(sql,[key])
        register = cur.fetchone()
        cur.close()
        cnx.close()
        return register

    elif option == 'upd':
        sql = "UPDATE MFbrands SET userlastupdate=%s WHERE brand = %s"
        data = ('admin',key)
        #print (sql, data)

        try:
            try:
                cur.execute(sql,data)
            except (mariadb.Error, mariadb.Warning) as err:
                if Error(errno=2006):
                    print("Bran exist: {}".format(err))

                else:
                    print("Oops! There was an error: {}".format(err))
                    flash('Oops! There was an error', 'success')
                result =  1
            result = 0

        finally:
            cnx.commit()
            cur.close()
            cnx.close()
        return result

    elif option == 'del':
        sql = "DELETE FROM MFbrands WHERE brand = %s"
        data = (key)
        #print (sql, data)
        result = 0
        try:
            try:
                cur.execute("DELETE FROM MFbrands WHERE brand = %s",[key])
            except (mariadb.Error, mariadb.Warning) as err:
                    print("Oops! There was an error: {}".format(err))
                    result = 1
            flash('delete completed', 'success')

        finally:
            print("finally")
            cnx.commit()
            cur.close()
            cnx.close()
        return result
