README – Stock_flash
Description:
Stock_flash est une application Python permettant de gérer un stock de produits. L’utilisateur peut :
Ajouter des produits
Lister les produits
Modifier la quantité en stock
Rechercher un produit
Supprimer un produit
Consulter un dashboard avec des informations statistiques
Quitter


L’application utilise Python et MySQL
pour connecter mysql et python il faut avoir l’environnement de travail avec cette commande : 
python3 -m venv mon_env


activer l’environnement de travail : 
source mon_env/bin/activate
J’ai installé la  bibliothèque Python permettant de se connecter à MySQL dans le terminal
pip install mysql-connector-python


On passe au code python pour les opérations CRUD
Configuration de la base de données
pour me connecter dans le terminal avec l’environnement mysql je tape cette commande : 
sudo mysql -u root -p

Avant de continuer on crée d’abord la base de donnée dans notre terminal ou bien dans un logiciel SGBD ensuite créer la table
Créez la base de données :
CREATE DATABASE Stock_flash;
USE Stock_flash;


Créez les tables nécessaires
CREATE TABLE categories (
    id_cat INT AUTO_INCREMENT PRIMARY KEY,
    nom_cat VARCHAR(50) NOT NULL
);


Table produits
CREATE TABLE produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prix_unitaire DECIMAL(10,2) NOT NULL,
    disponibilite VARCHAR(20),
    id_cat INT,
    FOREIGN KEY (id_cat) REFERENCES categories(id_cat)
);
Table stocks
CREATE TABLE stocks (
    id_stock INT AUTO_INCREMENT PRIMARY KEY,
    id INT,  
    quantite INT DEFAULT 0,
    FOREIGN KEY (id) REFERENCES produits(id)
);
Configuration du script Python
Avant de faire la connection mysql et python on importe d’abord la bibliotheque de python qu’on deja installer le dubut code on met:


importer mysql.connector


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MotDePasseFort",
    database="Stock_flash"
)


host : Adresse de votre serveur MySQL (localhost si local)
user : Nom d’utilisateur MySQL
password : Mot de passe MySQL
database : Nom de la base de données (Stock_flash)


Dashboard
Le dashboard propose :
Produit le plus cher
Valeur totale du stock (prix × quantité)
Nombre de produits par catégorie
Retour au menu principale


J’ai appris de nouvelle fonction comme:
Date_maj(date mise a jour) = CURDATE()
Et aussi:
"select nom, prix_unitaire from produits order by cast(prix_unitaire as unsigned) desc limit 2"
j’ai appris que CAST(....AS UNSIGNED) il permet de transformer le texte en nombre pour qu'il puisse le trier vu que j’avais mis prix_unitaire en varchar et que MYSQL ne trie pas les caractères pour que ça fonction j’ai  utilisé CAST(prix_unitaire AS UNSIGNED) et ça a regler le probleme
def update():


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


   cursor.close()




Pour la mise à jour, pour mettre à jour la quantité dans la table Stock et que j’ai la table produits aussi donc je doit effectuer comme une sorte de jointure pour permettre l’utilisateur de saisir le nom du produit qui se trouve dans la table produits pour pouvoir mettre à jour sa quantité qui se trouve dans la table Stocks vu que stock a comme clé étrangère id_produit qui se trouve dans la table produits
id_produits = resultat[0]
ici resultat[0] il permet l’extraction de l’id du produit sur résultat = cursor.fetchone  qui récupère une seule ligne du résultat  le résultat sera en tuple 

On a ajouter l'authentification des utilisateurs 
La gestion des utilisateurs (inscription / connexion)

L’attribution des rôles (admin / user)

Ce projet met en pratique :

Manipulation de bases de données relationnelles

Logique métier

Authentification sécurisée (hash mot de passe)

Gestion des rôles utilisateurs

La table utilisateurs
desc users;
+----------+----------------------+------+-----+---------+----------------+
| Field    | Type                 | Null | Key | Default | Extra          |
+----------+----------------------+------+-----+---------+----------------+
| id_user  | int                  | NO   | PRI | NULL    | auto_increment |
| username | varchar(100)         | NO   |     | NULL    |                |
| email    | varchar(100)         | NO   | UNI | NULL    |                |
| password | varchar(100)         | NO   | UNI | NULL    |                |
| role     | enum('admin','user') | YES  |     | user    |                |
+----------+----------------------+------+-----+---------+----------------+
Les utilisateurs que j'ai ajouter
 select * from users;
+---------+----------+-----------------+------------------------------------------------------------------+-------+
| id_user | username | email           | password                                                         | role  |
+---------+----------+-----------------+------------------------------------------------------------------+-------+
|       2 | Adama    | adama@gmail.com | 1fccc7a2ffb2c5cdc6ed0f5c2aef5a287cae786d896d541fd24de8ae6aa14654 | user  |
|       3 | Aicha    | aicha@gmail.com | 33a3b725f9c3697cd6a3edae0a245e5b40568b65ad33ca4e4b2402ce6bbdd230 | admin |
+---------+----------+-----------------+------------------------------------------------------------------+-------+




















