import mysql.connector as mysql
from contextlib import closing

DB_CONFIG = {
    "host" : "",
    "user" : "root",
    "password" : "Nishant13@",
    "database" : "ecommerce"
}

#=================
#DATABASE CONNECTION
#=================

def get_connection():
     return mysql.connect(**DB_CONFIG)
    
#=================
#DATABASE CONNECTION
#=================

def get_order_status(order_id):
   query = """
            SELECT order_id, customer_name, product_name, order_status
            FROM orders
            WHERE order_id = %s  \
            """

   with closing(get_connection()) as connection:
       with closing(connection.cursor()) as cursor:
           cursor.execute(query,(order_id,))
           order= cursor.fetchone()

           if not order:
               return "Order Not Found"
           
           return {
               "order_id": order[0], 
               "customer_name": order[1],
               "product_name": order[2],
               "status": order[3]
           }


def cancel_order(order_id):

    select_query = """
                    SELECT order_status
                    FROM orders
                    WHERE order_id = %s  \
                    """
    
    update_query = """
                     UPDATE orders
                     SET order_status = 'CANCELLED'   
                     WHERE order_id = %s  \
                   """

    
    with closing(get_connection()) as connection:
           with closing(connection.cursor()) as cursor:

               #get order current status
               cursor.execute(select_query, (order_id,))
               order = cursor.fetchone()

               if not order:
                   return "Order Not Found"

               status = order[0]

               if status == "DELIVERED":
                   return "Order Cannot be cancelled because it is already delivered."

               if status == "CANCELLED":
                   return "Order Cannot be cancelled because it is already Cancelled."


               #CANCEL ORDER
               cursor.execute(update_query, (order_id),)
               connection.commit()

               return "Order Cancelled Successfully"



               

               
    