import mysql.connector
#===========================ETABLISSEMENT DE LA CONNEXION===========================
connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "MotDePasseFort",
    database = "Stock_flash"
)

if connection.is_connected():
    print("Base de donnee connecter!")

#===============================MENU=======================================

def menu():
    print("========================MENU==========================")
    print("1: Ajouter un produit")
    print("2: Lister les produits")
    print("3: Modifier la quantite")
    print("4: Rechercher un produit")
    print("5: Supprimer un produit")
    print("6: Dashboard")
    print("0: Quitter")
    print("=======================================================")


#================================AJOUTER PRODUITS====================================

def ajout_produit():

    nom = input("Entrez le nom du produit:").strip()
    if not nom.isalpha():
        print("Erreur de saisie")
        return
    
    prix_unitaire = input("Entrez le prix du produit:")
    if not prix_unitaire.isdigit():
        print("Erreur de saisie")
        return
    
    disponibilite = input("Entrez la disponibilite du produit:")
    if not disponibilite.isalpha():
        print("Erreur de saisie")
        return
    id_cat = input("Entrez id categorie:")

    cursor = connection.cursor()
    query = "insert into produits (nom, prix_unitaire, disponibilite, id_cat) values (%s, %s, %s, %s)"
    cursor.execute(query, (nom, prix_unitaire, disponibilite, id_cat))
    connection.commit()
    print("produit bien ajouter")

#===================================AFFICHER PRODUITS=================================

def afficher_produits():
    cursor = connection.cursor()
    query = "select * from produits"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

#============================MISE A JOUR STOCK=============================================

def affiche_quantite_stock():
    cursor = connection.cursor()
    query = "select stocks.quantite, produits.nom from stocks inner join produits on produits.id = stocks.id;"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)


def update():
    affiche_quantite_stock()
    nom_produit = input("Entrez le nom du produit : ").strip()

    quantite_stock = input("Entrez la nouvelle quantite : ")
    if not quantite_stock.isdigit():
        print("Erreur : la quantité doit être un nombre.")
        return

 
    cursor = connection.cursor()
    query = "SELECT id FROM produits WHERE nom = %s"
    cursor.execute(query, (nom_produit,))
    result = cursor.fetchone()

    if not result:
        print("Produit introuvable.")
        return

    id_produit = result[0]

    query = "update stocks set quantite = %s, date_maj = CURDATE() where id = %s"
    cursor.execute(query, (quantite_stock, id_produit))
    connection.commit()
    print(f"Stock du produit '{nom_produit}' a été mis à jour à {quantite_stock}")
    for row in cursor.fetchone():
        print(row)

    cursor.close()
#=============================RECHERCHE PRODUITS========================================

def recherche():
    afficher_produits()
    rechercher = input("Entrer nom prosuits a rechercher:")
    if not rechercher.isalpha():
        print("Erreur de saisie")
        return

    cursor = connection.cursor()
    query = "select id, nom, prix_unitaire, disponibilite from produits where nom LIKE %s"
    cursor.execute(query, (rechercher,))
    for row in cursor.fetchall():
        print(row)

#================================SUPPRIMER PRODUITS=========================================

def supprimer():
    afficher_produits()
    delete_pro = input("Entrez le nom du produits que vous voulais supprimer:")
    if not delete_pro.isalpha():
        print("Erreur de saisie")
        return
    
    cursor = connection.cursor()
    query = "delete from produits where nom = %s"
    cursor.execute(query, (delete_pro,))
    connection.commit()
    print(f"{delete_pro} est bien supprimer")

#==============================DASHBOARD==================================================

def Dashboard():
    print("====================DASHBOARD==========================")
    print("1: produit le plus chere")
    print("2: la total financiere du stock")
    print("3: Le nombre de produits par categories")
    print("4: Retourner menu principale")
    print("========================================================")

    while True:
        choix = input("Entrez votre choix:")

        if choix == "1":
            produit_cher()
        elif choix == "2":
            valeur_total()
        elif choix == "3":
            produits_par_categorie()
        elif choix == "4":
            break
        else:
            print("Erreur de saisie")


#============================PRODUITS LE PLUS CHER=======================================

def produit_cher():
    cursor = connection.cursor()
    query = "select nom, prix_unitaire from produits order by cast(prix_unitaire as unsigned) desc limit 2"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"le produit le plus cher est {row[0]} avec un prix de {row[1]}")

#================================VALEUR TOTAL STOCK=========================================

def valeur_total():

    cursor = connection.cursor()
    query = "select sum(p.prix_unitaire * stocks.quantite) as valeur_totale from produits p inner join stocks on p.id = stocks.id "
    cursor.execute(query)
    for row in cursor.fetchone():
        print(f"la totale de tout le stock {row}")


#==================================NOMBRE DE PRODUITS PAR CATEGORIE=============================

def  produits_par_categorie():
    cursor = connection.cursor()
    query = "SELECT c.nom_cat, COUNT(p.id) AS nombre_produits FROM categories c LEFT JOIN produits p ON c.id_cat = p.id_cat GROUP BY c.nom_cat"
    cursor.execute(query)
    resultats = cursor.fetchall()

    # Définir la largeur des colonnes
    col1_width = 8
    col2_width = 25

    # En-tête
    print("+" + "-"*col1_width + "+" + "-"*col2_width + "+")
    print(f"| {'categories':<{col1_width}} | {'nombre de produits':<{col2_width}} ")
    print("+" + "-"*col1_width + "+" + "-"*col2_width + "+")

    # Données
    for id_cat, nom_cat in resultats:
        print(f"| {id_cat:<{col1_width}} | {nom_cat:<{col2_width}} ")
        print("-" * 40)

    # Ligne finale
    print("+" + "-"*col1_width + "+" + "-"*col2_width + "+")

#============================CHOIX MENU==================================================

def choix_menu():

    while True:
        menu()
        choix = input("Entrez votre choix:")

        if choix == "1":
            ajout_produit()
        elif choix == "2":
            afficher_produits()
        elif choix == "3":
            update()
        elif choix == "4":
            recherche()
        elif choix == "5":
            supprimer()
        elif choix == "6":
             Dashboard()
        elif choix == "0":
            exit()
        else:
            print("Erreur")

choix_menu()

connection.close()