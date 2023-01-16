def ajouteZero(caractere):
    """
    La fonction ajouteZero(caractere) prend en entrée un caractère "caractere" et retourne un caractère.
    Si x n'est pas égal à '1' ou '0', la fonction retourne '0'. Sinon, elle retourne 'caractere'.
    """
    if caractere not in "10":
        return '0'
    else:
        return caractere

def ipToNetworkAdress(ip, cidr):
    """
    La fonction ipToNetworkAdress(ip, cidr) prend en entrée une adresse IP(str) et un masque CIDR(str), et retourne un tuple contenant plusieurs informations sur l'adresse de réseau correspondante.
    """
    ip = ip.split(".")
    adresseReseau = ".".join([str(int(ip[i]) & int(cidrToMasque(cidr).split(".")[i])) for i in range(4)])
    if cidr == "32":
        return 1, cidrToMasque(cidr), adresseReseau, adresseReseau, adresseReseau, None
    elif cidr == "31":
        adressePremierHote = adresseReseau
        adresseDernierHote = ".".join(adresseReseau.split(".")[:3] + [str(int(adresseReseau.split(".")[-1])+1)])
        return 2, cidrToMasque(cidr), adresseReseau, adressePremierHote, adresseDernierHote, None
    else:
        # Calcul de la première adresse IP disponible dans le sous-réseau
        premiereIpDispo = ".".join(adresseReseau.split(".")[:3] + [str(int(adresseReseau.split(".")[-1]) + 1)])

        # Calcul de l'adresse de diffusion dans le sous-réseau
        adresseDifusion = ".".join(
            adresseReseau.split(".")[:3] + [str(int(adresseReseau.split(".")[-1]) + (2 ** (32 - int(cidr)) - 1))])

        # Calcul de la dernière adresse IP disponible dans le sous-réseau
        derniereIpDispo = ".".join(adresseDifusion.split(".")[:3] + [str(int(adresseDifusion.split(".")[-1]) - 1)])

        return 2**(32-int(cidr))-2, cidrToMasque(cidr), adresseReseau, premiereIpDispo, derniereIpDispo, adresseDifusion

def maskTocidr(mask):
    """
    La fonction maskTocidr(mask) prend en entrée une adresse de masque de sous-réseau (str) et retourne le masque CIDR correspondant (int).
    """
    #initialisation du nombre de bits à 1 dans le masque
    cidr = 0
    #pour chaque octet dans le masque
    for octet in mask.split("."):
        #ajouter le nombre de bits à 1 dans cet octet au nombre total de bits à 1
        cidr += bin(int(octet)).count("1")
    #retourner le nombre total de bits à 1 (cidr)
    return cidr

def cidrToMasque(cidr):
    """
La fonction cidrToMasque(cidr) prend en entrée un masque CIDR (int) et retourne l'adresse de masque de sous-réseau correspondante (str).
    """
    #conversion de cidr en entier
    cidr = int(cidr)
    #initialisation d'une liste pour stocker les octets du masque de sous-réseau
    masqueReseau = []
    #pour chaque octet
    for i in range(4):
        #si cidr est supérieur ou égal à 8
        if cidr >= 8:
            #ajouter 255 à l'octet
            masqueReseau.append(255)
            #soustraire 8 à cidr
            cidr -= 8
        else:
            #sinon, ajouter (256-2^(8-cidr)) à l'octet
            masqueReseau.append(256-2**(8-cidr))
            #mettre cidr à 0
            cidr = 0
    #retourner l'adresse de masque de sous-réseau (sous forme de chaîne de caractères)
    return '.'.join(map(str, masqueReseau))

def cidrToHex(cidr):
    """
    La fonction cidr2hex(cidr) prend en entrée un masque CIDR (int) et retourne l'adresse de masque de sous-réseau correspondante (liste).
    """
    #conversion du cidr en adresse de masque de sous-réseau
    masqueReseau = cidrToMasque(cidr)
    #conversion de chaque octet de l'adresse de masque de sous-réseau en hexadécimal (sous forme de chaîne de caractères)
    listeHexa = [hex(int(x))[2:].upper() for x in masqueReseau.split('.')]
    #retourner la liste des octets hexadécimaux
    return listeHexa

def masqueToBinList(masque):
    """
    La fonction masqueToBinList(mask) prend en entrée un masque de sous-réseau (str) et retourne une liste de chaînes de caractères binaires correspondant aux octets de l'adresse de masque de sous-réseau.
    """
    return [bin(int(x) ^ 255)[2:].zfill(8) for x in masque.split(".")]

def ipToBinList(ip):
    """
    La fonction ipToBinList(ip) prend en entrée une adresse IP (str) et retourne une liste de chaînes de caractères binaires correspondant aux octets de l'adresse IP.
    """
    listeIP = [format(int(x), '08b') for x in ip.split('.')]
    return listeIP

def binListToIp(listeBin):
    """
    La fonction binListToIp(listeBin) prend en entrée une liste de chaînes de caractères en binaire correspondant aux octets d'une adresse IP et retourne une adresse IP (str).
    """
    ip = '.'.join([str(int(x, 2)) for x in listeBin])
    return ip

def nbHostToCidr(nb):
    """
La fonction nbHostToCidr(nb) prend en entrée un entier nb qui représente le nombre d'hôtes souhaités dans un sous-réseau, et retourne un entier correspondant au masque de sous-réseau (CIDR) qui permet ce nombre d'hôtes.
    """
    # Boucle à partir de 32 jusqu'à -1 avec un pas de -1
    for cidr in range(32, -1, -1):
        # Si 2**(32-cidr) est supérieur ou égal à nb, retourne cidr
        if 2**(32-cidr) >= nb:
            return cidr

def ipToClasse(ip):
    """
    La fonction ipToClasse(ip) prend en entrée une adresse IP sous forme de chaîne de caractères et retourne une lettre correspondant à la classe de cette adresse IP (A, B, C, D ou E).
    """
    # convertit l'adresse IP en une liste de binaires
    ip = int(ipToBinList(ip)[0], 2)
    # vérifie si l'adresse IP est dans la classe A
    if ip < 128:
        return 'A'
    # vérifie si l'adresse IP est dans la classe B
    elif ip < 192:
        return 'B'
    # vérifie si l'adresse IP est dans la classe C
    elif ip < 224:
        return 'C'
    # vérifie si l'adresse IP est dans la classe D
    elif ip < 240:
        return 'D'
    else:
        # Si l'adresse IP est supérieure à 240, elle est dans la classe E
        return 'E'

def binToBinList(binStr):
    return [binStr[i:i+8] for i in range(0, len(binStr), 8)]

def int2binlist(i):
    """
    La fonction prend en entrée un nombre i sous forme d'un entier et génére une liste de chaînes binaires
    """
    return [bin(x)[2:].zfill(i) for x in range(2 ** i)]

def sousReseau(ip, nbHotes=None, nbReseaux=None):
    """
    La fonction 'sousReseau' prend en compte deux paramètres, 'ip', 'nbHotes' et 'nbReseaux'.
    Elle convertit l'adresse IP donnée en sa classe de réseau correspondante et trouve la notation CIDR du réseau.
    Si le nombre d'hôtes est choisi dans la fonction menu(), il calcule la notation CIDR à l'aide du nombre d'hôtes. Si le nombre de sous-réseaux est choisi dans la fonction menu(), il calcule la notation CIDR en utilisant le nombre de sous-réseaux et trouve le nombre disponible de sous-réseaux et les adresses réseau pour chacun des sous-réseaux.
    Elle renvoie un tuple contenant le CIDR, la classe de réseau, le nombre de sous-réseaux et une liste d'adresses réseau pour chaque sous-réseau et le nombre d'hôtes maximales disponibles.
    """

    bitsReseaux = [8, 16, 24]
    classeReseau = ['A', 'B', 'C']
    classeIP = ipToClasse(ip)

    cidrReseau = bitsReseaux[classeReseau.index(classeIP)]
    adresseReseau = ipToNetworkAdress(ip, cidrReseau)[2]
    adresseReseauListe = ipToBinList(adresseReseau)
    adresseReseauStr = ''.join(adresseReseauListe)
    if nbHotes:
        hote = int(nbHotes)
        cidr = nbHostToCidr(hote)
    elif nbReseaux:
        nbSousReseau = int(nbReseaux)
        bitsz = min([subnet_bits for subnet_bits in range(32) if 2 ** subnet_bits >= nbSousReseau])
        cidr = bitsz + cidrReseau

    bitsSousReseau = cidr - cidrReseau
    hotesDisponibles = ipToNetworkAdress(ip, cidr)[0]
    if bitsSousReseau > 0:
        nbReseaux = 2 ** bitsSousReseau
        binlistReseau = int2binlist(bitsSousReseau)
        listeAdresseReseau = []
        for cpt in binlistReseau:
            binstr = ''.join([adresseReseauStr[x] for x in range(cidrReseau)]) + cpt + '0' * (32 - cidr)
            binliste = binToBinList(binstr)
            listeAdresseReseau.append(binListToIp(binliste))
    return cidr, classeIP, nbReseaux, listeAdresseReseau, hotesDisponibles

def affichage(sousReseau):
    listeAdresseReseau = sousReseau[3]
    if listeAdresseReseau:
        cidr = sousReseau[0]
        listeSortie = [ipToNetworkAdress(subnet, cidr) for subnet in listeAdresseReseau]
        print(" ")
        print("Nouveau masque réseau : " + str(listeSortie[0][1]) + " (/" + str(cidr) + ")")
        print("Nombre de sous-réseaux : " + str(sousReseau[2]))
        print("Classe : " + str(sousReseau[1]))
        print(" ")

        for i in range(int(sousReseau[2])):

            print("Réseau n°", i+1)
            print("Masque réseau : ", listeSortie[i][1])
            print("Adresse réseau : ", listeSortie[i][2])
            print("Adresse du premier hôte : ", listeSortie[i][3])
            print("Adresse du dernier hôte : ", listeSortie[i][4])
            print("Adresse de broadcast : ", listeSortie[i][5])
            print("Nombre maximal d'hôtes : ", listeSortie[i][0])
            print(" ")

def menu():

    adresseIP = input("Entrez une adresse IP : ")
    masque = input("Entrez un masque valide : ")
    choix = int(input("Définir le nombre d'hôtes (1) ou de sous réseaux (2) : "))

    if choix == 1:
        hotes = int(input("Entrez le nombre d'hôtes souhaités : "))
        affichage(sousReseau(adresseIP, nbHotes=hotes))

    elif choix == 2:
        reseaux = int(input("Entrez le nombre de sous réseaux souhaités : "))
        affichage(sousReseau(adresseIP, nbReseaux=reseaux))

menu()

