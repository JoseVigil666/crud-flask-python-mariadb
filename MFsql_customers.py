#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 5, 2018

@author: diablo
"""
from flask import flash
from wtforms import Form, StringField
from mysql.connector.errors import Error
import mysql.connector as mariadb

def sql_customers(config, option, key, data):


    cnx = mariadb.connect(**config)
    cur = cnx.cursor()

    print (config, option, key, data)
    if option == 'cursor':
        print ('cursor')
        query = "SELECT * FROM MFcustomers ORDER BY idcustomer DESC LIMIT 20"
        cur.execute(query)
        cursor_customers = cur.fetchall()
        cur.close()
        cnx.close()
        print ('bye cursor')
        return cursor_customers

    elif option == 'ins':

        sql = "INSERT INTO MFcustomers( idcustomer, namecustomer, address , city, state , zipcode, email, phonenumber, usercreate, datecreate , userlastupdate, datelastupdate  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (0,data[1],data[2],data[3],data[4],data[5],data[6],data[7],'admin','2018-01-01 00:00:01','admin','2018-01-01 00:00:01')
        #print (sql,data)
        result = 0
        try:
            try:
                cur.execute(sql,data)
            except (mariadb.Error, mariadb.Warning) as err:
                if Error(errno=2006):
                    print("customer exist: {}".format(err))
                    flash('customer name Exist', 'success')
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
        print ('get')
        sql = "SELECT * FROM MFcustomers WHERE idcustomer = %s"
        cur.execute(sql,[key])
        register = cur.fetchone()
        cur.close()
        cnx.close()
        return register

    elif option == 'upd':
        print ('entro upd')
        sql = "UPDATE MFcustomers SET namecustomer=%s,address=%s,city=%s,state=%s,zipcode=%s,email=%s,phonenumber=%s,usercreate=%s,datecreate=%s,userlastupdate=%s,datelastupdate=%s WHERE customer = %s"
        data = (data[1],data[2],data[3],data[4],data[5],data[6],data[7],'admin','2018-01-01 00:00:01','admin','2018-01-01 00:00:01',key)
        print (sql, data)
        result = 0
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
        finally:
            print("finally")
            cnx.commit()
            cur.close()
            cnx.close()
        print ('cerrando upd')
        print (result)
        return result

    elif option == 'del':
        print ('del')
        sql = "DELETE FROM MFcustomers WHERE customer = %s"
        data = (key)
        print (sql, data)
        result = 0
        try:
            try:
                cur.execute("DELETE FROM MFcustomers WHERE customer = %s",[key])
            except (mariadb.Error, mariadb.Warning) as err:
                    print("Oops! There was an error: {}".format(err))
                    result = 1
            flash('delete completed', 'success')

        finally:
            print("finally")
            cnx.commit()
            cur.close()
            cnx.close()
        print ('bye bye del')
        print (result)
        return result
