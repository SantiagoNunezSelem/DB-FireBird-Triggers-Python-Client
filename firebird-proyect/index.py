from connection import create_connection_db
from tabulate import tabulate
from firebird.driver import Error
import os


#Importar conexión a la db
con = create_connection_db()
#Definir el cursor
cursor = con.cursor()

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def displayTable(cursor):
    #Recibe los resultados de una query y permite mostrarlos de forma amigable (nombre de columnas, separación entre datos, etc)
    columns =[desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    print("\n")
    print(tabulate(rows, headers=columns))
    print("\n")

def displayMenu():
    print("1. Mostrar Productos")
    print("2. Mostrar Facturas")
    print("3. Mostrar Factura con sus Detalles")
    print("4. Agregar Producto")
    print("5. Agregar Factura")
    print("6. Agregar Detalle")
    print("7. Eliminar Producto")
    print("8. Eliminar Factura")
    print("9. Eliminar Detalle")
    print("c. Limpiar Consola")
    print("0. Salir")

def tableTitle(title):
    title = title.upper()
    print("\n")
    print(f"----- {title}  -----")

def existeFactura(nroFactura):

    query = """
        SELECT * FROM AFACTURA a
        WHERE a.NRO = ?
    """

    #Prevent sql injection
    cursor.execute(query, (nroFactura,))

    if(cursor.fetchall() == []):
        print(f"\nLa factua con NRO {nroFactura} no existe\n")
        return False
    
    return True

def existeProducto(idProduct):
    query = """
        SELECT * FROM APRODUCTO p
        WHERE p.ID = ?
    """

    #Prevent sql injection
    cursor.execute(query, (idProduct,))

    if(cursor.fetchall() == []):
        print(f"\nEl producto con ID {idProduct} no existe\n")
        return False
    
    return True

def mostrarProductos():
    query = """
        SELECT * FROM APRODUCTO
    """
    cursor.execute(query)

    tableTitle("tabla info productos")
    displayTable(cursor)

def mostrarFacturas():
    query = """
        SELECT a.*,a_aux.CI FROM AFACTURA a
        JOIN AFACTURA_AUX a_aux ON a.NRO = a_aux.NRO
    """
    cursor.execute(query)

    tableTitle("tabla info facturas")
    displayTable(cursor)

def mostrarFacturaConDetalles():

    nroFactura = input("Ingrese el NRO de la factura: ")

    if(existeFactura(nroFactura)):

        query = """
            SELECT a.*,a_aux.CI,d.ID,d.CANTIDAD,d.PRECIO FROM AFACTURA a
            JOIN AFACTURA_AUX a_aux ON a.NRO = a_aux.NRO
            JOIN ADETALLE d ON a.NRO = d.NRO
            WHERE a.NRO  = ?
        """
        cursor.execute(query,(nroFactura,))

        tableTitle(f"tabla info factura NRO:{nroFactura} con sus detalles ")
        displayTable(cursor)

def agregarProducto():

    descr = str(input("Ingrese la descripcion del producto: "))
    stock = int(input("Ingrese el stock del producto: "))
    
    query = """
        INSERT INTO APRODUCTO (DESCR,STOCK) VALUES(?,?)
    """

    try:
        #Prevent sql injection
        cursor.execute(query, (descr,stock))
        con.commit()
        print("\nSe ingresaron los datos correctamente\n")
    except Error as e:
        print("Error al ralizar la consulta:",e)

def agregarFactura():
    importe = int(input("Ingrese el importe de la factura: "))

    query = """
        INSERT INTO AFACTURA (IMPORTE) VALUES (?)
    """

    try:
        #Prevent sql injection
        cursor.execute(query, (importe,))
        con.commit()
        print("\nSe ingresaron los datos correctamente\n")
    except Error as e:
        print("Error al ralizar la consulta:",e)

def agregarDetalle():
    #insert INTO ADETALLE (NRO,ID,CANTIDAD,PRECIO) VALUES (11,2,5,10)
    nroFactura = input("Ingrese el NRO de la factura: ")

    if(existeFactura(nroFactura)):

        idProduct = int(input("Ingrese el id del producto: "))

        if(existeProducto(idProduct)):
            cantidad = int(input("Ingrese la cantidad del producto: "))
            precio = int(input("Ingrese el precio del detalle: "))

            query = """
                INSERT INTO ADETALLE (NRO,ID,CANTIDAD,PRECIO) VALUES (?,?,?,?)
            """

            try:
                #Prevent sql injection
                cursor.execute(query, (nroFactura,idProduct,cantidad,precio))
                con.commit()
                print("\nSe ingresaron los datos correctamente\n")
            except Error as e:
                print("Error al ralizar la consulta:",e)

def eliminarProducto():
    idProduct = input("Ingrese el id del producto: ")
    
    if(existeProducto(idProduct)):
        print("--- ADVERTENCIA ---")
        print("Si elimina el producto se eliminaran por completo")
        print("todos los detalles que tengan asociado dicho producto!!")
        
        response = str(input("1. continuar: "))

        if(response == "1"):
            query1 = """
                DELETE FROM ADETALLE d WHERE d.ID = ?

            """

            query2 = """
                DELETE FROM APRODUCTO p WHERE p.ID = ?
            """

            try:
                #Prevent sql injection
                cursor.execute(query1, (idProduct,))
                cursor.execute(query2, (idProduct,))
                con.commit()
                print("\nSe eliminaron los datos correctamente\n")
            except Error as e:
                print("Error al ralizar la consulta:",e)
        else:
            print("No se elimino la factura")

def eliminarDetalle():
    nroFactura = input("Ingrese el numero (NRO) de la factura: ")

    if(existeFactura(nroFactura)):

        idProduct = int(input("Ingrese el id del producto: "))

        if(existeProducto(idProduct)):

            print("--- ADVERTENCIA ---")
            print("Esta accion no se puede revertir")
            print("Desea eliminar el detalle?")
            
            response = str(input("1. continuar: "))

            if(response == "1"):
                query = """
                    DELETE FROM ADETALLE d
                    WHERE d.NRO = ? AND d.ID = ? 
                """

                try:
                    #Prevent sql injection
                    cursor.execute(query, (nroFactura,idProduct))
                    con.commit()
                    print("\nSe elimino el detalle correctamente\n")
                except Error as e:
                    print("Error al ralizar la consulta:",e)
            else:
                print("No se elimino el detalle")

def eliminarFactura():
    nroFactura = int(input("Ingrese numero (NRO) de la factura: "))

    if(existeFactura(nroFactura)):
        print("--- ADVERTENCIA ---")
        print("Si elimina la factura se eliminaran por completo")
        print("todos los detalles asociados a dicha factura!!")
        
        response = str(input("1. continuar: "))
        
        if(response == "1"):
            query1 = """
                DELETE FROM ADETALLE d WHERE d.NRO = ?
            """

            query2 = """
                DELETE FROM AFACTURA f WHERE f.NRO = ?
            """

            try:
                #Prevent sql injection
                cursor.execute(query1, (nroFactura,))
                cursor.execute(query2, (nroFactura,))
                con.commit()
                print("\nSe eliminaron los datos correctamente\n")
            except Error as e:
                print("Error al ralizar la consulta:",e)

        else:
            print("No se elimino el producto")

def main() -> int:

    clearTerminal()
    while True:
        displayMenu()

        opt = input("Elegir opcion:")
        if(opt == "1"):
            mostrarProductos()
        elif(opt == "2"):
            mostrarFacturas()
        elif(opt == "3"):
            mostrarFacturaConDetalles()
        elif(opt == "4"):
            agregarProducto()
        elif(opt == "5"):
            agregarFactura()
        elif(opt == "6"):
            agregarDetalle()
        elif(opt == "7"):
            eliminarProducto()
        elif(opt == "8"):
            eliminarFactura()
        elif(opt == "9"):
            eliminarDetalle()
        elif(opt == "c"):
            clearTerminal()
        elif(opt == "0"):
            break

    con.close()
    
    return 0

main()

