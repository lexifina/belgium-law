<a name="LNK0001" href="#LNKR0001">TITRE Ier.</a> - DISPOSITIONS GENERALES ET DEFINITIONS

<a name="Art.1er"></a>Article <a href="#Art.2"> 1er</a>. Aux fins du présent arrêté, les définitions suivantes s'appliquent :
1° `Système de caisse': tout système informatisé pouvant être utilisé pour enregistrer des transactions de vente dans un environnement B2C normal, indépendamment de sa dénomination ou de la technologie utilisée ;
2° `Système de caisse certifié': un système de caisse qui satisfait aux exigences techniques reprises aux articles 4 à 57 de cet arrêté ministériel et pour lequel le service compétent du SPF Finances a délivré un certificat ;
3° `Fiscal Data Module': le module de contrôle tel que prévu à l'article 2, point 7 de l'arrêté royal du 30 décembre 2009 et à l'article 2, 3° de la loi du 30 juillet 2013 relative à la certification d'un système de caisse enregistreuse, pourvu d'un certificat de signature valable ;
4° `Fiscal Data Module certifié': le module de données fiscales qui satisfait aux exigences techniques visées aux articles 58 à 93 de cet arrêté ministériel et pour lequel le service compétent du SPF Finances a délivré un certificat ;
5° `Données introduites': les données mentionnées à l'article 2, points 1 et 2, de l'arrêté royal du 30 décembre 2009 fixant la définition et les conditions auxquelles doit répondre un système de caisse enregistreuse et relatives à :
- les enregistrements des livraisons de biens et des prestations de services (y compris le taux de T.V.A. applicable) ;
- l'enregistrement de début et de fin d'une prestation de travail ;
- l'établissement d'events training ;
- l'établissement d'events pro forma ;
- les modifications de prix et de taux de T.V.A. applicable ;
- les corrections et retours ;
- les paiements enregistrés, y compris les pourboires et les arrondissements ;
- les ouvertures du tiroir-caisse via la fonction de caisse éventuellement prévue (y compris le fond de caisse, les entrées/sorties en espèces, les comptages d'argent) ;
- l'établissement des rapports ;
- les modifications de programmation et de configuration suivantes: dataclear, dump, toute forme de réinitialisation (reset), changements de configuration PLU et changements des paramètres du système ;
- chaque enregistrement au sein d'une fonction qui peut temporairement interrompre, mettre en pause ou reprendre un enregistrement.
6° `Event `: tout event qui se produit dans le système de caisse et pour lequel des données sont établies et échangées entre le système de caisse et le fiscal data module.
Un système de caisse peut établir les events suivants :
- event Normal (label N) ;
- event Financial (label F) ;
- event Social (label S) ;
- event Report (label R) ;
- event Pro Forma (label P) ;
- event Invoice (label I) ;
- event Training (label T) ;
- event Copy (label C).
7° `Données de contrôle': les données que le système de caisse va recevoir du fiscal data module et qui doivent être mentionnées dans le bas du ticket ;
8° `ticket de caisse T.V.A.': Le ticket de caisse, visé à l'article 21bis de l'arrêté royal n° 1 du 29 décembre 1992 relatif aux mesures tendant à assurer le paiement de la taxe sur la valeur ajoutée, et qui est délivré au client soit sur papier, soit sous forme numérique, soit à la fois sur papier et sous forme numérique ;
9° `Utilisateurs': personnes qui enregistrent des events au moyen du système de caisse et sont identifiées à l'aide du numéro de Registre national ou du numéro BIS ;
Un utilisateur du système de caisse externe à l'entreprise doit toujours être identifié dans le système de caisse sous le numéro "00000000097".
Pour les commandes en ligne et en kiosque qui sont sous l'entière responsabilité de l'exploitant, le numéro "00000000029" doit être utilisé.
10° `Période d'ouverture' : la période pendant laquelle un établissement est ouvert. Cette période peut s'étendre sur plusieurs jours, mais ne peut jamais dépasser 24 heures. Les recettes réalisées pendant cette période sont toujours affectées à une date d'enregistrement. Cette date d'enregistrement est la date de début de la période en question. La période peut être divisée en plusieurs périodes d'enregistrement (shifts), de sorte qu'une date d'enregistrement peut contenir plusieurs périodes d'enregistrement.
11° `Fabricant': toute personne physique ou morale qui fabrique un produit fini destiné à être mis sur le marché en Belgique, soit comme système de caisse, soit comme fiscal data module, au sein d'un système de caisse enregistreuse ;
12° `Importateur': toute personne physique ou morale qui introduit sur le marché en Belgique un produit fini fabriqué en dehors de la Belgique et destiné à être utilisé soit comme système de caisse, soit comme fiscal data module, au sein d'un système de caisse enregistreuse ;
13° `Distributeur': toute personne physique ou morale qui vend ou donne en location, à un assujetti, en Belgique, un système de caisse certifié ou un fiscal data module certifié, destiné à être utilisé au sein d'un système de caisse enregistreuse ;
14° `Assujetti-exploitant': tout assujetti à la T.V.A., personne physique ou morale, tenu à la délivrance d'un ticket de caisse au moyen d'un système de caisse enregistreuse en vertu de l'arrêté royal n° 1 du 29 décembre 1992 relatif aux mesures tendant à assurer le paiement de la taxe sur la valeur ajoutée ou qui utilise ce système de caisse enregistreuse sur base volontaire ;
15° `Service compétent du SPF Finances': le service qui, sur base de cet arrêté, traitera toutes les demandes de certification et d'enregistrement, qui exécutera la procédure de certification et qui délivrera ou révoquera les certificats.
Au moment de la publication du présent arrêté, il s'agit de :
Administration de la Fiscalité
Centre National de Recherches - Division SCE - team SCE 1
E-mail: secr.gksce@minfin.fed.be

<a name="Art.2" href="#Art.1er">Art.</a> <a href="#LNK0002"> 2</a>. Aux fins de cet arrêté, les abréviations suivantes sont utilisées :
API - Application Programming Interface
B2C - Business-to-Consumer
BCE - Banque-Carrefour des Entreprises
CE - Conformité Européenne
CSAM - Control Sequence Access Method
DBMS - DataBase Management System
EEPROM - Electrically Erasable Programmable Read-Only Memory
FDM - Fiscal Data Module
GPIO - General Purpose Input/Output
GPS - Global Positioning System
GraphQL - Graph Query Language
HTTP - HyperText Transfer Protocol
JSON - JavaScript Object Notation
JWT - JSON Web Token
LAN - Local Area Network
LiPo - Lithium-Polymeer
LTE - Long Time Evolution
mTLS - Mutual Transport Layer Security
NISS - Numéro d'Identification de la Sécurité Sociale
NOP -No Operation
PD - Powered Device
PLU - Price Look-Up code
PoE - Power over Ethernet
POS - Point Of Sale
QR code - Quick Response code
RGPD - Règlement Général sur la Protection des Données
RTC - Real Time Clock
SCE - Système de Caisse Enregistreuse
SHA - Secure Hash Algorithm
URL - Uniform Resource Locator
USB - Universal Serial Bus
WiFi - Wireless Fidelity

<a name="LNK0002" href="#LNKR0002">TITRE II.</a> - EXIGENCES TECHNIQUES CONCERNANT LES ELEMENTS D'UN SYSTEME DE CAISSE ENREGISTREUSE

<a name="Art.3" href="#Art.2">Art.</a> <a href="#LNK0003"> 3</a>. Un système de caisse enregistreuse, tel que visé à l'article 2 de la loi du 30 juillet 2013 relative à la certification d'un système de caisse enregistreuse, se compose toujours d'un système de caisse certifié et d'un Fiscal Data Module (FDM) certifié. Les deux éléments doivent répondre aux exigences techniques visées au Titre II de cet arrêté.

<a name="LNK0003" href="#LNKR0003">CHAPITRE 1er.</a> - Exigences techniques concernant le système de caisse certifié

<a name="LNK0004" href="#LNKR0004">Section 1re.</a> - Fonctions obligatoires

<a name="LNK0005" href="#LNKR0005">Sous-section 1re.</a> - Enregistrement des events

<a name="Art.4" href="#Art.3">Art.</a> <a href="#Art.5"> 4</a>. Le système de caisse doit au minimum être capable de générer les events suivants :
- Normal (N)
- Financial (F)
- Social (S)
- Report (R)
Si le système de caisse prévoit également les events :
- Pro Forma (P),
- Invoice (I),
- Training (T),
- Copy (C)
les exigences techniques prévues dans le présent arrêté ministériel doivent être respectées.

<a name="Art.5" href="#Art.4">Art.</a> <a href="#Art.6"> 5</a>. Event Normal
1° Un event qui est établi lorsque l'enregistrement d'une opération de vente prend fin et qui donne toujours lieu à l'établissement d'un ticket de caisse T.V.A., tel que visé à l'article 2, point 4, de l'arrêté royal du 30 décembre 2009 fixant la définition et les conditions auxquelles doit répondre un système de caisse enregistreuse et à l'article 21bis de l'arrêté royal n° 1 relatif au paiement de la T.V.A..
2° Une entrée sous forme d'event Normal ne contient que les lignes de produits enregistrées auxquelles il se rapporte dans l'ordre chronologique, y compris les corrections et les changements de prix liés à la ligne de produit correcte.
3° Lorsqu'un ticket de caisse T.V.A. ne contient que des lignes de produits négatives, la mention "REFUND" est ajoutée. S'il s'agit d'une annulation complète d'un ticket de caisse T.V.A. précédemment émis, la référence au ticket de caisse T.V.A. original est ajoutée.

<a name="Art.6" href="#Art.5">Art.</a> <a href="#Art.7"> 6</a>. Event Pro Forma
Un event Pro Forma est établi dans une des situations suivantes :
a. un enregistrement dans lequel tout le système de caisse se trouve en mode pro forma ;
b. chaque entrée au sein d'une fonction qui peut temporairement interrompre, mettre en pause ou reprendre un enregistrement ;
c. l'établissement de l'aperçu d'addition.
Par mode Pro Forma, il est entendu les enregistrements strictement illustratifs, dans lequel le système de caisse peut faire des enregistrements, sans influencer les résultats de ventes.
Dans le cas d'une vente interrompue, les transactions partielles (entrées) doivent être enregistrées comme event Pro Forma. Ces enregistrements doivent in fine résulter dans un event Normal.
Une entrée en tant qu'event Pro Forma est effectué conformément aux règles d'un event Normal, sauf si l'event concerne un aperçu d'addition.
L'aperçu d'addition donne un résumé des commandes enregistrées et/ou le montant à payer avant que le paiement ne soit enregistré et que l'event Normal ne soit établi. Cela inclut également l'appel et l'affichage de l'état d'une table sur une tablette, un smartphone ou tout autre appareil connecté ou faisant partie du système de caisse.
Chaque enregistrement d'une transaction de vente interrompu doit résulter in fine dans un event Normal, à l'exception d'un transfert d'une table vers un compte hôtelier global.
Les impressions, peu importe leurs formes, des entrées visés dans le point b ci-dessus ne peuvent pas contenir de montants.

<a name="Art.7" href="#Art.6">Art.</a> <a href="#Art.8"> 7</a>. Event Training
Tous les enregistrements établis lorsque le système de caisse ou l'utilisateur se trouve en mode training.

<a name="Art.8" href="#Art.7">Art.</a> <a href="#Art.9"> 8</a>. Event Copy
La copie d'un event établi au préalable. Il y est toujours fait référence à l'event d'origine. Une copie peut être établie pour les events suivants : Normal, Pro Forma, Invoice, Social, Financial et Report.

<a name="Art.9" href="#Art.8">Art.</a> <a href="#Art.10"> 9</a>. Event Social
L'enregistrement de l'heure de début et de fin de présence d'un membre du personnel sur le lieu de travail.

<a name="Art.10" href="#Art.9">Art.</a> <a href="#Art.11"> 10</a>. Event Report
L'établissement des rapports fiscaux relatifs au chiffre d'affaires ou aux utilisateurs avec des données provenant du système de caisse et du FDM tels que décrits dans les articles 21 à 30.

<a name="Art.11" href="#Art.10">Art.</a> <a href="#Art.12"> 11</a>. Event Financial
L'enregistrement des transactions financières qui ne sont pas considérées comme du chiffre d'affaires pour la T.V.A. et qui se rapportent à l'une des situations suivantes :
- l'entrée en espèces ;
- la sortie en espèces ;
- le remboursement des MultiPurpose Vouchers contre paiement en espèces ;
- le paiement de tickets de caisse T.V.A. émis antérieurement ;
- les corrections de méthodes de paiement incorrectement enregistrées après la clôture.

<a name="Art.12" href="#Art.11">Art.</a> <a href="#Art.13"> 12</a>. Event Invoice
Un event dans lequel une facture, visée à l'article 53, § 2, alinéa 1er, du Code de la taxe sur la valeur ajoutée, d'un (ou plusieurs) ticket(s) de caisse T.V.A. émis antérieurement est établie.

<a name="Art.13" href="#Art.12">Art.</a> <a href="#Art.14"> 13</a>. Le système de caisse attribue un numéro à chaque event. Cette numérotation doit être continue pour tous les events, par event label, par terminal ou par une combinaison des options précédentes.

<a name="Art.14" href="#Art.13">Art.</a> <a href="#Art.15"> 14</a>. Le système de caisse ne doit pouvoir enregistrer des events que seulement si le FDM est connecté et est entièrement opérationnel.
Une transaction, dont l'enregistrement a commencé ne peut pas être clôturée tant qu'une signature n'a pas été reçue du FDM.

<a name="Art.15" href="#Art.14">Art.</a> <a href="#LNK0006"> 15</a>. Sur un système de caisse, aucun event ne peut être enregistré sans qu'un utilisateur ne soit identifié.

<a name="LNK0006" href="#LNKR0006">Sous-section 2.</a> - Conservation des données

<a name="Art.16" href="#Art.15">Art.</a> <a href="#Art.17"> 16</a>. Le système de caisse doit pouvoir conserver les données créées par le système de caisse lui-même et celles reçues du FDM, sous leur forme originale, conformément au délai de conservation fiscal en vigueur.
Aucun format spécifique n'est prescrit. Conformément à l'article 61, § 1er, du Code de la T.V.A., toutes les données créées et stockées par le système de caisse doivent être présentées sous une forme lisible et compréhensible. Pour faciliter la prise de copie de données, au moins un port (de type courant) de la caisse doit être accessible/activé pour un support de données externe.

<a name="Art.17" href="#Art.16">Art.</a> <a href="#LNK0007"> 17</a>. Un aperçu de toutes les configurations de logiciels et des tables de base de données doit pouvoir être produit sur simple requête de l'agent contrôleur.

<a name="LNK0007" href="#LNKR0007">Sous-section 3.</a> - Codes T.V.A. à utiliser

<a name="Art.18" href="#Art.17">Art.</a> <a href="#LNK0008"> 18</a>. Le système de caisse doit prévoir les codes et labels de T.V.A. suivants :

<table border="1"><tr><td valign="top">BTW-CODE </td><td valign="top">BTW-TARIEF OMSCHRIJVING </td><td valign="top">BTW-TARIEF </td><td valign="top">CODE TVA </td><td valign="top">DESCRIPTION TAUX DE TVA </td><td valign="top">TAUX DE TVA </td></tr><tr><td valign="top">A </td><td valign="top">Hoog </td><td valign="top">21 % </td><td valign="top">A </td><td valign="top">Haut </td><td valign="top">21 % </td></tr><tr><td valign="top">B </td><td valign="top">Midden </td><td valign="top">12 % </td><td valign="top">B </td><td valign="top">Moyen </td><td valign="top">12 % </td></tr><tr><td valign="top">C </td><td valign="top">Laag </td><td valign="top">6 % </td><td valign="top">C </td><td valign="top">Bas </td><td valign="top">6 % </td></tr><tr><td valign="top">D </td><td valign="top">Nultarief </td><td valign="top">0 % </td><td valign="top">D </td><td valign="top">Taux zéro </td><td valign="top">0 % </td></tr><tr><td valign="top">X </td><td valign="top">Buiten btw- toepassingsgebied </td><td valign="top">Geen </td><td valign="top">X </td><td valign="top">Hors du champ d'application de la TVA </td><td valign="top">Néant</td></tr></table>

<a name="LNK0008" href="#LNKR0008">Sous-section 4.</a> - Le ticket de caisse T.V.A.

<a name="Art.19" href="#Art.18">Art.</a> <a href="#Art.20"> 19</a>. Le ticket de caisse T.V.A., tel que prévu à l'article 21bis de l'arrêté royal n° 1 du 21 décembre 1992 est considéré fiscalement comme un document de contrôle nécessitant l'émission d'un ticket de caisse T.V.A..
Cela signifie que l'acheteur/consommateur doit recevoir ce document (pour vérification, comme document de garantie, comme justificatif, etc.). Ce document peut être délivré sur papier, sous forme numérique ou des deux manières. Lorsque le ticket de caisse T.V.A. est délivré sous forme numérique, l'exploitant doit s'assurer que ce ticket de caisse T.V.A. est effectivement à la disposition du consommateur.

<a name="Art.20" href="#Art.19">Art.</a> <a href="#LNK0009"> 20</a>. Le ticket de caisse T.V.A. contient, en application de l'article 2, 7°, de l'arrêté royal du 30 décembre 2009 fixant la définition et les conditions auxquelles doit répondre un système de caisse enregistreuse, au moins les mentions suivantes :
a. la dénomination complète : "TICKET DE CAISSE T.V.A." ;
b. l'identification de l'émetteur au moyen de son nom ou de sa dénomination sociale, de son adresse et de son numéro d'identification à la T.V.A. visé à l'article 50 du Code de la T.V.A. ;
c. la dénomination commerciale de l'exploitation ;
d. le numéro d'unité d'établissement (tel qu'il est enregistré auprès de la BCE) ;
e. l'identification du système de caisse au moyen du numéro de fabrication mentionné dans l'article 46, et du numéro de version du logiciel de caisse qui y est installé ;
f. l'identification du terminal ;
g. l'identification du dispositif d'entrée; on vise ici (par ordre de disponibilité : l'adresse MAC, le numéro de série, l'adresse IP, etc.) ;
h. l'identification de l'utilisateur (de manière à ce qu'il soit identifiable au sein de l'entreprise), comme prévu dans l'article 1, 9° ;
i. la date et l'heure de délivrance du ticket de caisse T.V.A. (généré par le système de caisse) ;
j. un numéro de ticket continu issu d'une série ininterrompue (conformément à l'article 13 de cet arrêté) ;
k. les opérations ou lignes de produits enregistrées; qui contiennent :
- la quantité, la description, le prix total de la ligne, le code du taux de T.V.A. ;
- les modifications de prix appliquées et messages ;
l. le montant total à payer du ticket, T.V.A. comprise ;
m. la base imposable par taux de T.V.A. applicable, telle que calculée par le FDM ;
n. le montant de la T.V.A. due, par taux de T.V.A. applicable, tel que calculé par le FDM ;
les modifications de prix non mentionnées dans les lignes de produits ;
o. les données de contrôle créées et transmises par le FDM. Celles-ci sont imprimées de manière lisible ;
p. les lignes de paiement applicables, y compris les arrondissements éventuels, les pourboires et les autres paiements (remboursements) ;
q. le code QR, qui contient l'URL tel que transmis par le FDM.

<a name="LNK0009" href="#LNKR0009">Sous-section 5.</a> - Les rapports

<a name="Art.21" href="#Art.20">Art.</a> <a href="#Art.22"> 21</a>. Conformément à l'article 2, point 5, de l'arrêté royal du 30 décembre 2009 mentionné ci-dessus, l'assujetti qui utilise un système de caisse enregistreuse est tenu d'établir un rapport chiffre d'affaires journalier ainsi qu'un rapport utilisateur journalier (rapports Z).
En exécution de l'article 2, point 3, de l'arrêté royal du 30 décembre 2009, il doit en outre être possible de générer les dénommés rapports intermédiaires (rapports X). Ces rapports sont un résumé des enregistrements dans le système de caisse relatifs au chiffre d'affaires et à toutes les autres données pour la période d'ouverture en cours, depuis le dernier rapport sur le chiffre d'affaires et jusqu'à la date d'établissement du rapport intermédiaire.
Ces rapports contiennent des données provenant à la fois du système de caisse et du FDM.

<a name="Art.22" href="#Art.21">Art.</a> <a href="#Art.23"> 22</a>. Le système de caisse peut, en outre, prévoir d'autres rapports pour soutenir la gestion quotidienne de l'entreprise. Ces rapports doivent être parfaitement conformes au contenu des rapports Z obligatoires. Il s'agit notamment de rapports périodiques sur le chiffre d'affaires par article/groupe d'articles/exploitation et de rapports périodiques sur les utilisateurs.
Si, pour une période d'ouverture, aucun ou seulement un des deux rapports Z obligatoires a été établi, le système de caisse devra, lors de l'établissement du premier rapport (qu'il s'agisse d'un rapport X ou Z) pour la période d'ouverture suivante, d'abord établir tous les rapports Z manquants reprenant toutes les données relatives au(x) période(s) d'ouverture précédente(s).
Le système de caisse peut prévoir une fonction d'établissement automatique de ces rapports. Ces rapports Z doivent toujours mentionner clairement la période qu'ils concernent.

<a name="Art.23" href="#Art.22">Art.</a> <a href="#Art.24"> 23</a>. Un rapport Z `chiffre d'affaires` est assimilé, à des fins fiscales, à un journal de recettes tenu sous forme numérique.

<a name="Art.24" href="#Art.23">Art.</a> <a href="#Art.25"> 24</a>. Si un système de caisse utilise plusieurs FDM liés à lui pour des raisons de sécurité ou de load balancing, les rapports doivent contenir les données cumulées de tous les FDM liés.

<a name="Art.25" href="#Art.24">Art.</a> <a href="#Art.26"> 25</a>. Dans le cas d'un système de caisse composé de plusieurs terminaux, si un ou plusieurs terminaux ne sont pas accessibles lors de l'établissement du rapport Z, le système de caisse doit établir et transmettre, dès que possible, un rapport supplémentaire qui contient UNIQUEMENT les données manquantes dans le rapport d'origine.

<a name="Art.26" href="#Art.25">Art.</a> <a href="#Art.27"> 26</a>. Les rapports Z `chiffre d'affaires' et `utilisateurs', après signature par le FDM, sont conservés dans un fichier JSON, qui comprend la signature, sur le système de caisse et doivent pouvoir être présentés de manière simple immédiatement sur demande des agents du SPF Finances.

<a name="Art.27" href="#Art.26">Art.</a> <a href="#Art.28"> 27</a>. Les rapports Z et X ont exactement le même contenu à l'exception que le rapport Z contient, en plus, une numérotation continue.

<a name="Art.28" href="#Art.27">Art.</a> <a href="#Art.29"> 28</a>. L'event Report donne TOUJOURS lieu à la création d'un fichier MAIS il doit aussi être facilement imprimable par l'exploitant, soit sur papier, soit sous forme numérique.

<a name="Art.29" href="#Art.28">Art.</a> <a href="#Art.30"> 29</a>. Le rapport `chiffre d'affaires' doit, en plus de sa dénomination `X CHIFFRE D'AFFAIRES' ou `Z CHIFFRE D'AFFAIRES' au-dessus et en lettres capitales, pour la période d'ouverture concernée, au moins reprendre les données suivantes :
a. le nom ou la dénomination sociale de l'entreprise assujettie ;
b. le numéro d'identification à la T.V.A. visé à l'article 50 du Code de la T.V.A. de l'entreprise mentionnée au point a. (numéro de T.V.A.) ;
c. le numéro d'établissement (BCE) de l'établissement où le SCE est installé et est concerné par le rapport ;
d. la date et l'heure d'établissement du rapport ;
e. l'identification de la (des) caisse(s) concernée(s) par le rapport ;
f. le numéro de production du FDM et les références du premier et du dernier event repris dans les FDM, dont les données sont reprises dans le rapport ;
g. la date d'enregistrement concernée par le rapport ;
h. la date et l'heure du début et de la fin de la période d'ouverture ;
i. le montant total du chiffre d'affaires réalisé pour le eventlabel N (T.V.A. comprise) ;
j. le montant total du chiffre d'affaires réalisé pour le eventlabel N (T.V.A. comprise) le cas échéant par groupe principal/département ;
k. le montant total de la base d'imposition par taux de T.V.A. applicable, pour le eventlabel N ;
l. le montant de T.V.A. par taux de T.V.A. applicable pour le eventlabel N ;
m. le montant total du chiffre d'affaires réalisé pour le eventlabel N (T.V.A. comprise), ventilé par taux de T.V.A. applicable (somme des montants repris dans k. et l.) ;
n. le montant total des paiements enregistrés ventilé par moyens de paiement utilisés et enregistrés ;
o. le montant total des arrondissements, tel qu'enregistré dans les lignes de paiement ;
p. le nombre de tickets de caisse T.V.A. délivrés (eventlabel N) ;
q. le nombre d'ouvertures du tiroir-caisse sans enregistrement d'opérations ;
r. le nombre de tickets training générés ainsi que leur montant total (T.V.A. comprise) (eventlabel T) ;
s. le nombre de tickets de reprise générés ainsi que leur montant total (T.V.A. comprise) ;
t. le nombre de tickets pro forma générés ainsi que leur montant total (T.V.A. comprise) (eventlabel P) ;
u. le nombre de réductions et de majorations accordées ainsi que leur montant total (T.V.A. comprise), ventilé par type ;
v. un aperçu des montants (T.V.A. comprise) des fonctions, telles que corrections, reprises, annulations de lignes, etc., autres que celles visées au point u, qui ont diminué le montant total du chiffre d'affaires, indépendamment du eventlabel dans lequel elles ont été initialement entrées (eventlabel P ou N), ventilés par type ;
w. les numéros et montants (T.V.A. comprise) des factures établies conformément à l'article 31 ;
x. la référence du premier et du dernier event qui sont repris dans le rapport.
y. uniquement pour le rapport Z : une numérotation continue issue d'une série ininterrompue.

<a name="Art.30" href="#Art.29">Art.</a> <a href="#LNK0010"> 30</a>. Le rapport `utilisateurs' doit, en plus de sa dénomination `X UTILISATEURS' ou `Z UTILISATEURS' au-dessus et en lettres capitales, au moins reprendre les données suivantes :
a. le nom ou la dénomination sociale de l'entreprise assujettie ;
b. le numéro d'identification à la T.V.A. visé à l'article 50 du Code de la T.V.A. de l'entreprise mentionnée au point a. (numéro de T.V.A.) ;
c. le numéro d'établissement (BCE) de l'établissement où le SCE est installé et est concerné par le rapport ;
d. la date et l'heure d'établissement du rapport ;
e. l'identification de la (des) caisse(s) concernée(s) par le rapport ;
f. par utilisateur : son nom d'utilisateur et numéro NISS ;
g. par utilisateur : le montant total du chiffre d'affaires réalisé (T.V.A. comprise), tel que calculé dans i. pour le rapport 'chiffre d'affaires' ;
h. par utilisateur : l'état du contenu du tiroir-caisse, à la fin de la période concernée, si cette fonction est utilisée, ventilé par moyens de paiement utilisés et enregistrés ;
i. par utilisateur : les heures de connexion et de déconnexion au système de caisse, telles qu'enregistrées via l'event Social et transmises au FDM, dans la mesure où l'exploitant souhaite utiliser l'event Social ;
j. par utilisateur : l'heure à laquelle le premier et le dernier event sont générés ;
k. la référence du premier et du dernier event qui sont repris dans le rapport ;
l. uniquement pour le rapport Z : une numérotation continue issue d'une série ininterrompue.

<a name="LNK0010" href="#LNKR0010">Sous-section 6.</a> - Factures créées avec le système de caisse

<a name="Art.31" href="#Art.30">Art.</a> <a href="#Art.32"> 31</a>. A titre facultatif, l'émission de factures au moyen du système de caisse peut être prévue. Cette facture doit être transmise au FDM en tant qu'event Invoice. Une facture ne peut être établie qu'après l'établissement effectif d'un ticket de caisse T.V.A. (event N).
Si cette modalité est prévue dans le système de caisse, elle fait partie intégrante de la procédure de certification, quel que soit le format ou la forme de cette facture.

<a name="Art.32" href="#Art.31">Art.</a> <a href="#Art.33"> 32</a>. L'event Invoice donne TOUJOURS lieu à une impression (sur papier, sous forme numérique ou les deux).
La facture émise doit, en plus de la mention `FACTURE' en lettre capitales, contenir au moins les données suivantes :
- toutes les mentions obligatoires visées à l'article 5 de l'arrêté royal n° 1 du 29 décembre 1992 relatif aux mesures tendant à assurer le paiement de la taxe sur la valeur ajoutée (dont plus particulièrement le nom, l'adresse et le numéro d'identification à la T.V.A. du client) ;
- une numérotation continue séparée et spécifique à l'ensemble des factures émises au moyen du système de caisse, combinée au numéro d'event continu ;
- une référence au(x) numéro(s) d'origine du(des) ticket de caisse T.V.A. ;
- les lignes de produits du (des) ticket(s) de caisse T.V.A. concerné(s) ;
- les données de contrôle de la communication avec le FDM.

<a name="Art.33" href="#Art.32">Art.</a> <a href="#LNK0011"> 33</a>. Toutes les données des factures établies doivent pouvoir être exportées du système de caisse enregistreuse en tant que sous-facturier de sortie.

<a name="LNK0011" href="#LNKR0011">Sous-section 7.</a> - Règles de consolidation

<a name="Art.34" href="#Art.33">Art.</a> <a href="#Art.35"> 34</a>. Pour optimiser la lisibilité des impressions données aux clients, les consolidations sont autorisées.
Lors de l'impression, les lignes positives et négatives peuvent être consolidées et même l'ordre des lignes peut être modifié selon le système de caisse.

<a name="Art.35" href="#Art.34">Art.</a> <a href="#LNK0012"> 35</a>. Ces consolidations ne sont jamais appliquées aux messages que le système de caisse envoie vers le FDM. Ces messages doivent contenir toutes les données introduites, dans l'ordre chronologique.

<a name="LNK0012" href="#LNKR0012">Sous-section 8.</a> - Impressions

<a name="Art.36" href="#Art.35">Art.</a> <a href="#Art.37"> 36</a>. Aux fins du présent arrêté, il convient de toujours établir une distinction claire entre les termes suivants : EVENT &lt;&lt; &gt;&gt; IMPRESSION (ticket) &lt;&lt; &gt;&gt; MESSAGE vers le FDM.
CHAQUE event donne TOUJOURS lieu à un message vers le FDM, mais pas nécessairement à une impression.

<a name="Art.37" href="#Art.36">Art.</a> <a href="#Art.38"> 37</a>. Le système de caisse prévoit l'impression obligatoire du ticket de caisse T.V.A., comme le prévoit l'article 21bis de l'arrêté royal n° 1 relatif aux mesures tendant à assurer le paiement de la taxe sur la valeur ajoutée.

<a name="Art.38" href="#Art.37">Art.</a> <a href="#LNK0013"> 38</a>. Un event Normal donne toujours lieu à une impression.
Lorsqu'un event Normal de type REFUND (article. 5, 3° ) est effectué, cela doit être clairement indiqué sur le ticket par la mention REFUND.
Lorsque le système de caisse prévoit une fonction d'impression ou de génération des tickets training et/ou d'impression des tickets pro forma et/ou des tickets de copie, ces tickets doivent être clairement dissociés du ticket de caisse T.V.A.. A cette fin, les dénominations respectives TRAINING, PRO FORMA ou COPIE doivent être clairement apposées sur le ticket.
Un aperçu d'addition, porte la mention "ADDITION PROVISOIRE" de manière clairement lisible.
Sur toutes les impressions papier produites par le système de caisse, et ce, peu importe leur dénomination et qui ne sont pas des tickets de caisse T.V.A. tels que prévus dans l'article 1, 8°, le texte suivant doit être imprimé dans le bas du ticket, en lettres capitales : "CECI N'EST PAS UN TICKET DE CAISSE T.V.A. VALABLE".

<a name="LNK0013" href="#LNKR0013">Sous-section 9.</a> - Arrondissement des paiements

<a name="Art.39" href="#Art.38">Art.</a> <a href="#LNK0014"> 39</a>. Le système de caisse doit prévoir l'application des règles d'arrondissement des articles VI.7/1 et VI.7/2 du Code de droit économique.

<a name="LNK0014" href="#LNKR0014">Section 2.</a> - Fonctions interdites

<a name="Art.40" href="#Art.39">Art.</a> <a href="#Art.41"> 40</a>. Aucun matériel informatique ou logiciel qui influence, modifie ou perturbe le fonctionnement normal des fonctions mentionnées dans le présent arrêté ministériel, ne peut être connecté ou intégré au système de caisse. Ceci vise également le logiciel de caisse ou programme de caisse non repris dans les manuels ou toute autre documentation soumise au SPF Finances, qui est installé sur un système de caisse ou qui fonctionne sur ce système de caisse.

<a name="Art.41" href="#Art.40">Art.</a> <a href="#Art.42"> 41</a>. Tous les changements apportés à une ligne de produit déjà introduite, qui se produisent dans le cadre d'un même event, doivent être clairement mentionnés de manière distincte comme une ligne de produit supplémentaire, négative ou positive, dans le message d'event envoyé au FDM, qu'il s'agisse d'un event Pro Forma ou Normal.

<a name="Art.42" href="#Art.41">Art.</a> <a href="#Art.43"> 42</a>. Un event ne peut plus être modifié ou effacé une fois que son enregistrement est envoyé au FDM.
Les corrections d'un event clôturé ne peuvent se faire que par l'établissement d'un nouvel event supplémentaire.

<a name="Art.43" href="#Art.42">Art.</a> <a href="#Art.44"> 43</a>. Un système de caisse ne peut offrir la possibilité d'imprimer un ticket de caisse T.V.A. (event Normal) avant que l'opération ne soit finalisé(e). Cela signifie qu'aucune impression ne peut être possible sans que le système de caisse n'ait reçu une signature du FDM.
Sur les impressions, autres que le ticket de caisse T.V.A., la signature numérique reçue n'est pas mentionnée.

<a name="Art.44" href="#Art.43">Art.</a> <a href="#Art.45"> 44</a>. Un système de caisse ne peut pas comporter de fonction permettant de modifier les données préprogrammées (description, unité, prix, taux de T.V.A., ...) des articles ou services, entre l'introduction de l'opération et sa finalisation dans le ticket de caisse T.V.A., de telle sorte que les enregistrements originaux (déjà signés par le FDM) soient également modifiés.

<a name="Art.45" href="#Art.44">Art.</a> <a href="#LNK0015"> 45</a>. Un système de caisse ne peut offrir la possibilité de modifier, de quelque manière que ce soit, les réglages (paramètres) de façon à quand même autoriser les fonctions interdites.

<a name="LNK0015" href="#LNKR0015">Section 3.</a> - Identification du système de caisse

<a name="Art.46" href="#Art.45">Art.</a> <a href="#Art.47"> 46</a>. Tout système de caisse doit être doté d'une indication de son modèle et de son numéro de fabrication. Ce numéro de fabrication doit être un numéro unique, permettant d'identifier sans ambiguïté tant le système de caisse que son fabricant. Le numéro de fabrication est constitué comme suit :
CXXXNNNPPPPPP
où :
- CXXX = le numéro d'identification du fabricant d'un système de caisse (fourni par l'administration sur demande) ;
- NNN = le numéro de série, attribué au modèle par l'administration ;
- PPPPPPP = le numéro de fabrication unique alphanumérique (basé sur le numéro de série ou la clé de licence).
Ce numéro de fabrication unique doit être clairement visible ou facilement consultable sur chaque système de caisse installé (procédure à présenter par le fabricant).

<a name="Art.47" href="#Art.46">Art.</a> <a href="#LNK0016"> 47</a>. Le logiciel de caisse doit être doté d'un numéro de version. Ce numéro de version doit être une mention unique d'une version de logiciel et doit être adapté à chaque modification du logiciel.
Le numéro de version du logiciel de caisse et le nom du fabricant du programme doivent être facilement lisibles. La version du logiciel doit être facilement identifiable et doit au moins apparaître de manière claire sur l'écran d'ouverture de session. Ces données de version sont envoyées lors de chaque communication avec le FDM.

<a name="LNK0016" href="#LNKR0016">Section 4.</a> - Communication avec le Fiscal Data Module

<a name="Art.48" href="#Art.47">Art.</a> <a href="#Art.49"> 48</a>. Le système de caisse doit pouvoir envoyer au FDM les données telles que déterminées à l'article 1, 5° du présent arrêté ministériel.
Les montants transmis pour les différents events sont toujours exprimés en EURO; les montants en devises étrangères ne peuvent être mentionnés qu'à titre informatif et doivent être pourvus de leur code ISO d'identification.

<a name="Art.49" href="#Art.48">Art.</a> <a href="#Art.50"> 49</a>. Cette communication doit obligatoirement comporter les messages énumérés à l'article 53 et selon le protocole de communication à l'article 54. Tout autre message éventuel entre les deux appareils doit être documenté dans la demande de certification et contribuer au bon fonctionnement du système. Les extensions non documentées sont strictement interdites.

<a name="Art.50" href="#Art.49">Art.</a> <a href="#Art.51"> 50</a>. Le système de caisse doit être en mesure de recevoir, stocker et imprimer les bases imposables calculées et les montants de T.V.A. - tous les deux calculés par le FDM - sur le ticket de caisse T.V.A.. Ces informations ne sont fournies que sur ce type de ticket.

<a name="Art.51" href="#Art.50">Art.</a> <a href="#LNK0017"> 51</a>. Le système de caisse doit être en mesure de recevoir les données de contrôle suivantes du FDM et de les stocker :
- le pied de page tel que configuré par le SPF Finances et transmis par le FDM ;
- le numéro d'identification unique de la transaction ;
- les signatures numériques.
Ces données de contrôle sont imprimées sur le ticket de caisse T.V.A..

<a name="LNK0017" href="#LNKR0017">Sous-section 1re.</a> - Connexion physique avec le Fiscal Data Module

<a name="Art.52" href="#Art.51">Art.</a> <a href="#LNK0018"> 52</a>. Le système de caisse et le FDM sont connectés par un câble (LAN) ou sans fil (WiFi). La configuration de la connexion entre le système de caisse et le FDM a lieu dans le back-office.
Le système de caisse et le FDM communiquent entre eux par le biais de messages sur HTTPS. A cette fin, le FDM met son service GraphQL à la disposition du POS.
Pour la sécurité, mTLS est utilisé, sur la base du certificat intermédiaire du fabricant du FDM.
Le FDM est connecté par internet à l'API du cloud SPFFIN et reçoit également de manière régulière des instructions du cloud SPFFIN API par ce biais. Dans certains cas, de telles instructions peuvent mener à l'affichage d'un message sur le système de caisse et/ou à une intervention manuelle via le système de caisse.

<a name="LNK0018" href="#LNKR0018">Sous-section 2.</a> - Messages du système de caisse au Fiscal Data Module

<a name="Art.53" href="#Art.52">Art.</a> <a href="#Art.54"> 53</a>. Les messages sont envoyés par le système de caisse vers le service GraphQL du FDM.
Les données envoyées comprennent notamment :
- les données de transaction (events P et N) ;
- les données financières (event F) ;
- les données sociales (event S) ;
- les copies (event C) ;
- les events training (event T) ;
- les factures (event I) ;
- les rapports (event R).

<a name="Art.54" href="#Art.53">Art.</a> <a href="#LNK0019"> 54</a>. Tous les events sont envoyés au FDM pour être signés numériquement. Pour ce faire, diverses mutations sont mises à disposition par le service GraphQL du FDM.

<a name="LNK0019" href="#LNKR0019">Sous-section 3.</a> - Réponse du Fiscal Data Module

<a name="Art.55" href="#Art.54">Art.</a> <a href="#Art.56"> 55</a>. En réponse aux messages, le système de caisse reçoit les données de contrôle, les montants imposables calculés, les montants de T.V.A. calculés, les signatures et divers messages. Cette réponse suit toujours la structure définie par le service GraphQL du FDM, décrite dans les descriptions détaillées.

<a name="Art.56" href="#Art.55">Art.</a> <a href="#LNK0020"> 56</a>. La signature numérique, visée à l'article 54, est apposée sur les champs de données dont le contenu et la structure sont décrits dans les descriptions détaillés.

<a name="LNK0020" href="#LNKR0020">Section 5.</a> - Descriptions détaillées

<a name="Art.57" href="#Art.56">Art.</a> <a href="#LNK0021"> 57</a>. Les descriptions techniques détaillées complètes et actualisées (descriptions des champs, formats de données, mutations GraphQL, contenu, use cases) de la communication entre le système de caisse et le FDM, y compris la gestion d'erreurs, sont mises à disposition par le SPF Finances sur son site web : www.systemedecaisseenregistreuse.be.

<a name="LNK0021" href="#LNKR0021">CHAPITRE 2.</a> - Exigences techniques concernant le fiscal data module

<a name="Art.58" href="#Art.57">Art.</a> <a href="#Art.59"> 58</a>. Ce chapitre comprend, clarifie et spécifie les exigences techniques auxquelles doit répondre le FDM du SCE, tel que prévu à l'article 2, point 7, de l'arrêté royal du 30 décembre 2009.
Le FDM doit être connecté au système de caisse et fait donc partie intégrante du système de caisse enregistreuse.

<a name="Art.59" href="#Art.58">Art.</a> <a href="#LNK0022"> 59</a>. Compte tenu de sa nature et de sa fonction, le FDM doit toujours se trouver dans l'entreprise, connecté au système de caisse. Il peut s'agir de l'adresse d'exploitation (recommandé), mais également de l'adresse administrative ou du domicile fiscal de l'entreprise ou toute autre place au sein de l'UE.
Un FDM ne peut pas être utilisé pour plusieurs exploitations (donc minimum un FDM par exploitation).

<a name="LNK0022" href="#LNKR0022">Section 1re.</a> - Prescriptions générales

<a name="Art.60" href="#Art.59">Art.</a> <a href="#Art.61"> 60</a>. Tout FDM installé doit satisfaire aux exigences énoncées dans le présent arrêté ministériel.

<a name="Art.61" href="#Art.60">Art.</a> <a href="#Art.62"> 61</a>. Le FDM ne peut contenir que les fonctions décrites dans cet arrêté ministériel.
Toute fonction supplémentaire ne peut être autorisée que si elle contribue au bon fonctionnement d'ensemble. Ces fonctions doivent être décrites en détail dans la documentation jointe à la demande de certification.

<a name="Art.62" href="#Art.61">Art.</a> <a href="#Art.63"> 62</a>. Le fonctionnement du FDM ne peut être perturbé par la connexion d'autres matériels informatiques au système de caisse.

<a name="Art.63" href="#Art.62">Art.</a> <a href="#LNK0023"> 63</a>. Le FDM doit pouvoir recevoir, valider et répondre aux messages du système de caisse tout en transmettant simultanément les données de transaction en ligne aux serveurs du SPF Finances.

<a name="LNK0023" href="#LNKR0023">Sous-section 1re.</a> - Compteurs

<a name="Art.64" href="#Art.63">Art.</a> <a href="#LNK0024"> 64</a>. . Le FDM contient au moins les compteurs suivants, qui sont mis à jour lorsque le contenu des events concernés est signé :
- nombre d'events Normal ;
- nombre d'events Pro Forma ;
- nombre d'events Invoice ;
- nombre d'events Financial ;
- nombre d'events Social ;
- nombre d'events Copy ;
- nombre d'events Training ;
- nombre d'events Report ;
- compteur continu pour tous les events.

<a name="LNK0024" href="#LNKR0024">Sous-section 2.</a> - Calcul des bases imposables et des montants de T.V.A.

<a name="Art.65" href="#Art.64">Art.</a> <a href="#Art.66"> 65</a>. Le FDM reçoit du SPF Finances, lors de son initialisation et lors de chaque modification, les taux de T.V.A. applicables aux codes de T.V.A. A, B, C, D et X mentionnés précédemment. Cela permet au FDM de calculer les bases d'imposition et les montants de T.V.A. pour les events Normal.
Ce calcul du montant de la T.V.A. par taux de T.V.A. est effectué conformément aux articles 26, 28 et 33 de l'arrêté royal n° 8 du 12 mars 1970, déterminant, en matière de taxe sur la valeur ajoutée, les modalités d'arrondissement des taxes dues, à déduire ou à restituer.

<a name="Art.66" href="#Art.65">Art.</a> <a href="#LNK0025"> 66</a>. Le calcul de la base d'imposition et de la T.V.A. due se fait comme suit.
1. Le FDM effectue, par code T.V.A., la somme de tous les montants pour toutes les lignes de produits.
2. Le FDM calcule la T.V.A., à partir de ce prix, pour déterminer la base d'imposition, à l'aide de la formule suivante :
P x (t/(100 + t))
où :
P = prix T.V.A. comprise
t = le taux de T.V.A. en vigueur à ce moment-là, exprimé par un nombre avec deux décimales.
Au moment de la publication du présent arrêté ministériel, les taux de T.V.A. suivants sont d'application :
- pour le code T.V.A. A : 21 ;
- pour le code T.V.A. B : 12 ;
- pour le code T.V.A. C : 6 ;
- pour le code T.V.A. D : 0 ;
- pour le code T.V.A. X : 0.
3. Ce montant de T.V.A. est arrondi au cent inférieur ou supérieur selon que la troisième décimale atteint ou n'atteint pas 5.
4. Le montant éventuellement arrondi est déduit du montant T.V.A. comprise et la différence constitue la base d'imposition.

<a name="LNK0025" href="#LNKR0025">Sous-section 3.</a> - Buffering

<a name="Art.67" href="#Art.66">Art.</a> <a href="#Art.68"> 67</a>. Le FDM doit pouvoir mettre en mémoire tampon (buffer) les messages reçus dans sa mémoire interne pendant une période suffisamment longue pour garantir que ces messages ont été effectivement envoyés aux serveurs du SPF Finances.

<a name="Art.68" href="#Art.67">Art.</a> <a href="#LNK0026"> 68</a>. En cas d'inaccessibilité des serveurs du SPF Finances, le FDM continue à recevoir des messages du système de caisse, à envoyer des réponses et à stocker ces messages dans la capacité de buffer du FDM. Dès que les serveurs sont à nouveau disponibles, le FDM transmet, dès que possible, les messages non encore envoyés. La capacité du buffer est toutefois limitée et, une fois cette limite atteinte, le FDM refusera de signer de nouveaux messages. Chaque réponse du FDM à un message de la caisse contient une mention concernant la capacité du buffer déjà utilisée.

<a name="LNK0026" href="#LNKR0026">Sous-section 4.</a> - Paramètres personnalisables

<a name="Art.69" href="#Art.68">Art.</a> <a href="#LNK0027"> 69</a>. Le FDM doit permettre une adaptation limitée de ses paramètres par (ou pour) le SPF Finances, en particulier pour :
- l'horloge (connexion à un time server externe) ;
- la durée maximale de mise hors ligne (des serveurs du SPF Finances) ;
- le niveau des taux de T.V.A. (en cas de modification) ;
- la fréquence de transmission des messages de transaction ;
- le certificat client pour la connexion sécurisée ;
- les paramètres ;
- les url et les services web à appeler.

<a name="LNK0027" href="#LNKR0027">Sous-section 5.</a> - Identification et sécurité des produits

<a name="Art.70" href="#Art.69">Art.</a> <a href="#Art.71"> 70</a>. Chaque FDM portera un numéro de fabrication unique qui sera composé comme suit :
AAABBNNNNNN,
où :
- AAA = le numéro d'identification du fabricant (fourni par le SPF Finances sur demande) ;
- BB = le numéro de modèle du fabricant (fourni par le SPF Finances sur demande) ;
- NNNNNN = le numéro de série (croissant, déterminé par le fabricant).

<a name="Art.71" href="#Art.70">Art.</a> <a href="#Art.72"> 71</a>. Chaque FDM est conforme aux directives européennes applicables en matière de sécurité des produits. Le marquage CE obtenu doit être communiqué avec le formulaire de demande de certification.

<a name="Art.72" href="#Art.71">Art.</a> <a href="#LNK0028"> 72</a>. Chaque FDM porte de manière visible les informations suivantes :
- l'indication du modèle ;
- le numéro de fabrication visée à l'article 70 ;
- la date de fabrication ;
- le marquage CE.

<a name="LNK0028" href="#LNKR0028">Section 2.</a> - Exigences Hardware

<a name="LNK0029" href="#LNKR0029">Sous-section 1re.</a> - Processeur (module)

<a name="Art.73" href="#Art.72">Art.</a> <a href="#Art.74"> 73</a>. Le FDM est développé autour d'un processeur ARM/CORTEX ou équivalent. Ce dernier a ou supporte au minimum :
- le nombre de GPIO nécessaires pour soutenir la fonction demandée ;
- une température de fonctionnement comprise entre 0° C et 70 ° C (norme commerciale) ;
- un RTC.

<a name="Art.74" href="#Art.73">Art.</a> <a href="#Art.75"> 74</a>. Le FDM est alimenté par le port USB-C (+5V) et/ou PoE (PD).

<a name="Art.75" href="#Art.74">Art.</a> <a href="#Art.76"> 75</a>. La communication avec le système de caisse se fait au minimum via Ethernet LAN et WiFi.

<a name="Art.76" href="#Art.75">Art.</a> <a href="#LNK0030"> 76</a>. Le FDM doit être doté d'une mémoire interne suffisante pour assurer son bon fonctionnement (stockage du système d'exploitation, stockage du firmware, stockage des compteurs, etc.), compte tenu des exigences techniques visées dans le présent arrêté.

<a name="LNK0030" href="#LNKR0030">Sous-section 2.</a> - Sécurité

<a name="Art.77" href="#Art.76">Art.</a> <a href="#LNK0031"> 77</a>. Le FDM est équipé d'un secure element (ATECC608B ou équivalent), comprenant notamment les caractéristiques suivantes :
- mémoire non volatile, stockage d'au moins 2 compteurs (chacun d'au moins 256 bits), certificats et données mixtes read/write, read only ou secret data ;
- l'accès aux différentes sections de la mémoire est protégé ;
- conforme au RGPD.

<a name="LNK0031" href="#LNKR0031">Sous-section 3.</a> - Connectivité

<a name="Art.78" href="#Art.77">Art.</a> <a href="#Art.79"> 78</a>. Le FDM est équipé d'un module Wi-Fi certifié, d'un port LAN et peut être équipé en option d'un module minimum LTE 4/5G.

<a name="Art.79" href="#Art.78">Art.</a> <a href="#Art.80"> 79</a>. Le FDM peut, en outre, être équipé d'un récepteur GPS, qui transmet sa géolocalisation par communication.

<a name="Art.80" href="#Art.79">Art.</a> <a href="#LNK0032"> 80</a>. Un FDM peut contenir des éléments matériels supplémentaires (p. ex. : une batterie LiPo), à condition qu'ils permettent de mieux soutenir les fonctions demandées et/ou qu'ils n'aient pas d'incidence négative ou limitative sur celles-ci.

<a name="LNK0032" href="#LNKR0032">Sous-section 4.</a> - Capacité de stockage physique

<a name="Art.81" href="#Art.80">Art.</a> <a href="#LNK0033"> 81</a>. Le FDM dispose d'une capacité de stockage minimale de 2 GB disponible pour stocker les données de transaction.

<a name="LNK0033" href="#LNKR0033">Sous-section 5.</a> - Software

<a name="Art.82" href="#Art.81">Art.</a> <a href="#LNK0034"> 82</a>. Au minimum, le firmware répond aux exigences énoncées dans le présent arrêté ministériel et dans les descriptions détaillées susmentionnées. Le firmware peut comprendre davantage de fonctions, qui ne doivent toutefois pas affecter les exigences techniques fixées et qui doivent être décrites de manière claire dans la documentation accompagnant la demande de certification.
En respectant les règles décrites dans cet arrêté ministériel (le cas échéant, la soumission et l'obtention de l'autorisation du service compétent du SPF Finances), le firmware peut recevoir un patch ou un upgrade nécessaire. Cette procédure ne peut être réalisée que par le fabricant ou son délégué et de manière sécurisée. Une description détaillée est fournie dans la documentation jointe à la demande de certification et fait partie du processus de certification.

<a name="LNK0034" href="#LNKR0034">Section 3.</a> - User interface - fonctionnement

<a name="LNK0035" href="#LNKR0035">Sous-section 1re.</a> - Obligatoire sur l'appareil lui-même

<a name="Art.83" href="#Art.82">Art.</a> <a href="#LNK0036"> 83</a>. Les indicateurs de santé minimaux suivants doivent être mis à la disposition de l'utilisateur :
- l'état de la batterie (si l'appareil peut fonctionner sans adaptateur secteur) ;
- l'état de la communication avec le système de caisse connectée (communication `réussie', communication `non réussie') ;
- l'état du buffer : au minimum `near full buffer' et `buffer full' ;
- l'état du réseau internet : `communication réussie' avec SPFFIN, `communication erronée' avec SPFFIN.
Ces indicateurs peuvent être visibles sur un display ou par LED, au choix du fabricant. Le manuel d'utilisation fourni indique clairement tous les états possibles de ces indicateurs.

<a name="LNK0036" href="#LNKR0036">Sous-section 2.</a> - A fournir sur l'appareil

<a name="Art.84" href="#Art.83">Art.</a> <a href="#Art.85"> 84</a>. L'accès au backoffice du FDM est sécurisé de manière adéquate afin de protéger le bon fonctionnement de l'appareil. Le fabricant documente ce point en détail dans sa demande de certification.

<a name="Art.85" href="#Art.84">Art.</a> <a href="#LNK0037"> 85</a>. L'interface utilisateur du FDM peut :
- soit être prévue sur l'appareil lui-même ;
- soit être accessible via un appareil connecté ;
- soit être accessible via le système de caisse connecté ;
- soit une combinaison des options énumérées ci-dessus.

<a name="LNK0037" href="#LNKR0037">Sous-section 3.</a> - Interface utilisateur - configuration

<a name="Art.86" href="#Art.85">Art.</a> <a href="#LNK0038"> 86</a>. Sont visées ici tant la configuration de la connexion réseau au système de caisse que celle aux serveurs du SPF Finances.

<a name="LNK0038" href="#LNKR0038">Sous-section 4.</a> - Cybersécurité

<a name="Art.87" href="#Art.86">Art.</a> <a href="#LNK0039"> 87</a>. Les fabricants de FDM doivent respecter les dispositions de la directive (UE) 2022/2555 du Parlement européen et du Conseil du 14 décembre 2022 concernant des mesures destinées à assurer un niveau élevé commun de cybersécurité dans l'ensemble de l'Union, modifiant le règlement (UE) no 910/2014 et la directive (UE) 2018/1972, et abrogeant la directive (UE) 2016/1148 (directive SRI 2).

<a name="LNK0039" href="#LNKR0039">Section 4.</a> - Communication entre le Fiscal Data Module et le service cloud du SPF Finances

<a name="LNK0040" href="#LNKR0040">Sous-section 1re.</a> - Premier démarrage

<a name="Art.88" href="#Art.87">Art.</a> <a href="#LNK0041"> 88</a>. Conformément aux dispositions relatives à l'enregistrement des composants du système de caisse enregistreuse visées dans le présent arrêté, tant le système de caisse que le FDM sont enregistrés par les parties prenantes concernées au cours des différentes phases (production, livraison) dans le e-service SCE du SPF FINANCES.
Il s'agit de déterminer au niveau de l'entreprise et de l'établissement quel FDM est lié à quel système de caisse.
Lors de la mise en service du SCE, le système de caisse et le FDM sont liés. Après un démarrage correct (responsabilité unique de l'entreprise et de son (ses) fournisseur(s)), le FDM se connectera au cloud service du SPF Finances via une connexion internet sécurisée.
Le service cloud du SPFFIN :
1. vérifie le numéro de série du FDM et du système de caisse, attribue le certificat d'authentification unique et personnalisé et l'envoie via la connexion sécurisée au FDM, qui le stocke dans l'environnement sécurisé ;
2. envoie simultanément un aperçu des taux de T.V.A. applicables ;
3. envoie simultanément les paramètres de fréquence personnalisés ;
4. transmet, lors de ce premier contact, les 'données de pied de page' qui figurent sur le ticket de caisse T.V.A.

<a name="LNK0041" href="#LNKR0041">Sous-section 2.</a> - Connexion et sécurité

<a name="Art.89" href="#Art.88">Art.</a> <a href="#Art.90"> 89</a>. La connexion via internet est configurée via le backoffice du FDM. Ce backoffice est spécifique au fabricant et l'interface utilisateur peut être différent. Au minimum, le backoffice offre les options de configuration suivantes :
- les URLs du service cloud SPFFIN ;
- l'URL du time server.

<a name="Art.90" href="#Art.89">Art.</a> <a href="#LNK0042"> 90</a>. Toute communication est sécurisée par l'utilisation :
- du certificat d'authentification ;
- du protocole mTLS qui crypte les envois.

<a name="LNK0042" href="#LNKR0042">Sous-section 3.</a> - Transmission en ligne des données de transaction

<a name="Art.91" href="#Art.90">Art.</a> <a href="#LNK0043"> 91</a>. En fonction de la fréquence de transmission configurée, le FDM transmet au service cloud du SPFFIN des paquets contenant des données de transaction provenant du FDM (messages JSON). Ces paquets contiennent au moins le contenu d'un event complet ou d'un NOP.
Le service cloud du SPFFIN accuse (ou refuse) la bonne réception des paquets. Le FDM conserve ces paquets pendant 10 jours supplémentaires, après quoi ils peuvent être effacés de la mémoire du buffer.
Ces paquets sont conservés par le service cloud du SPFFIN pendant au moins trois ans.
Cette conservation n'affecte pas les obligations légales de conservation et d'introduction fiscales des données originales sur le système de caisse (articles 315bis et 315ter du CIR92 et articles 60 et 63 du Code de la T.V.A.).
Les données autres que celles reprises dans cet arrêté ministériel ne peuvent et ne doivent pas être transmises via cette connexion.

<a name="LNK0043" href="#LNKR0043">Sous-section 4.</a> - API Application programming interface

<a name="Art.92" href="#Art.91">Art.</a> <a href="#LNK0044"> 92</a>. Le FDM communique avec les serveurs (cloud) du SPFFIN via le protocole décrit ci-dessous. Aucune autre communication n'est autorisée.

<a name="LNK0044" href="#LNKR0044">Section 5.</a> - Descriptions détaillées

<a name="Art.93" href="#Art.92">Art.</a> <a href="#LNK0045"> 93</a>. Les descriptions techniques détaillées complètes et actualisées (hardware, firmware, descriptions des champs, formats de données, API, JSON, protocole) de la communication entre le FDM et les serveurs du SPF Finances sont disponibles sur son site web : www.systemedecaisseenregistreuse.be.

<a name="LNK0045" href="#LNKR0045">TITRE III.</a> - OBLIGATIONS DES DIFFERENTES PARTIES CONCERNEES

<a name="LNK0046" href="#LNKR0046">CHAPITRE 1er.</a> - Obligations du fabricant ou importateur d'éléments du système de caisse enregistreuse

<a name="LNK0047" href="#LNKR0047">Section 1re.</a> - Procédure de certification

<a name="LNK0048" href="#LNKR0048">Sous-section 1re.</a> - Service compétent

<a name="Art.94" href="#Art.93">Art.</a> <a href="#LNK0049"> 94</a>. Le service compétent du SPF Finances est l'unique autorité de certification dans ce processus et règle de manière unilatérale tous les différends portant sur la certification, sans communiquer avec des tiers à ce sujet.
Le service compétent du SPF Finances peut, à tout moment, procéder à de nouveaux tests sur un appareil/ logiciel déjà certifié.

<a name="LNK0049" href="#LNKR0049">Sous-section 2.</a> - Principes généraux

<a name="Art.95" href="#Art.94">Art.</a> <a href="#Art.96"> 95</a>. Toute constatation (ou suspicion) de non-conformité soit d'un système de caisse, soit d'un FDM, doit être immédiatement signalée à cette autorité de certification qui, après analyse éventuelle, prendra les mesures appropriées pour corriger l'infraction constatée.
Ces mesures de correction peuvent être les suivantes :
- le retrait du certificat, dans le cas d'une infraction qui compromet le bon fonctionnement fiscal du SCE ;
- exiger une correction pour les fabrications futures, en combinaison avec une tolérance unique de la non-conformité constatée, si le bon fonctionnement du SCE n'est pas compromis et que le fabricant a agi de bonne foi ;
- exiger une correction du logiciel dans les appareils déjà en service ;
- la régularisation des constatations et des éclaircissements supplémentaires de la réglementation si la non-conformité résulte d'un manque de clarté de la réglementation.

<a name="Art.96" href="#Art.95">Art.</a> <a href="#Art.97"> 96</a>. L'autorité de certification ne s'exprime que sur les questions relatives au présent arrêté ministériel et à son interprétation (en d'autres termes la conformité du produit avec les dispositions techniques de l'arrêté ministériel).

<a name="Art.97" href="#Art.96">Art.</a> <a href="#Art.98"> 97</a>. L'autorité de certification se réserve le droit de vérifier l'implémentation correcte des appareils certifiés, dans le cadre du maintien du certificat.

<a name="Art.98" href="#Art.97">Art.</a> <a href="#LNK0050"> 98</a>. Les modifications des dispositions techniques relatives au fonctionnement du FDM par rapport à la précédente Circulaire AGFisc N° 33/2016 (n° E.T.124.747) du 8 novembre 2016 ne s'appliquent qu'aux appareils soumis à la procédure de certification, après la date d'entrée en vigueur du présent arrêté.

<a name="LNK0050" href="#LNKR0050">Sous-section 3.</a> - La demande de certification

<a name="Art.99" href="#Art.98">Art.</a> <a href="#Art.100"> 99</a>. Pour chaque version ou modèle de FDM ou de système de caisse qui sera mis sur le marché belge en vue d'être installé comme élément d'un système de caisse enregistreuse et conformément à l'article 3 de la loi du 30 juillet 2013, précitée, relative à la certification d'un système de caisse enregistreuse, une demande de certification doit être introduite soit par le fabricant, soit par l'importateur auprès du service compétent du SPF Finances.

<a name="Art.100" href="#Art.99">Art.</a> <a href="#Art.101"> 100</a>. Lors de toute demande de certification, chaque fabricant ou importateur doit remettre au service compétent du SPF Finances, un dossier complet qui indique que, selon le fabricant ou importateur, le produit satisfait aux exigences techniques établies dans le présent arrêté ministériel.
La procédure dure maximum 3 mois, à moins que des informations supplémentaires soient demandées.

<a name="Art.101" href="#Art.100">Art.</a> <a href="#Art.102"> 101</a>. Lors d'une demande de certification, le demandeur doit remettre au service compétent du SPF Finances un dossier de demande complet, reprenant au moins les documents et informations suivants :
- une liste avec un aperçu des documents et informations remis ;
- l'identification complète du fabricant, comprenant entre autres :
* la dénomination sociale, la forme juridique ;
* l'adresse ;
* la personne de contact mandatée pour la procédure de certification, son numéro de téléphone et son adresse e-mail ;
* le numéro d'identification à la T.V.A. ;
le cas échéant, l'identité complète de l'importateur, comprenant entre autres :
* la dénomination sociale, la forme juridique ;
* l'adresse ;
* la personne de contact, son numéro de téléphone, son adresse e-mail et son site internet ;
* le numéro d'identification à la T.V.A. ;
- un relevé comportant les données relatives au demandeur (activité, gamme de produits, moyens de production, ...) et un aperçu des distributeurs ;
- la liste des distributeurs auxquels une partie du procédé de fabrication est déléguée ;
- tous les manuels disponibles (manuel d'utilisation, manuel de configuration, manuel de programmation, manuel d'entretien,....) qui sont destinés soit à l'utilisateur final, soit au distributeur ;
- une description exhaustive des données utilisées et établies par le FDM ou le système de caisse ;
- la méthode selon laquelle les données susmentionnées sont conservées dans le système de caisse conformément au RGDP (par l'utilisateur/l'exploitant) ;
- une description technique du processus de fabrication ;
- une description technique détaillée de la manière dont l'ensemble des exigences techniques ont été incorporées ;
- une description des résultats des tests qu'il a lui-même exécutés (ou fait exécuter par un labo accrédité) sur le produit ;
- pour le FDM: la construction et sa conformité avec les normes CE imposées dans le présent arrêté ministériel ;
- pour le FDM: les fonctions, y compris les dispositions techniques mentionnées dans les descriptions détaillées ;
- pour le FDM: le fonctionnement au sein de l'environnement de travail défini, y compris le respect des critères de performance requis dans le présent arrêté ministériel.

<a name="Art.102" href="#Art.101">Art.</a> <a href="#Art.103"> 102</a>. Lors de la demande de certification, le fabricant du système de caisse fournit une description détaillée de la base de données et, plus particulièrement, de toutes les tables contenant des données d'events ou une description complète de toute autre manière de conserver les données mentionnées dans l'arrêté ministériel.
Le fabricant déclare expressément dans sa demande que :
- l'utilisateur-opérateur a des droits en lecture seule sur la base de données,
- le SPF Finances a accès, si nécessaire et sur simple demande, aux données pertinentes sur les systèmes installés chez les utilisateurs pour les copier.
Le fabricant fournit en outre au service compétent du SPF Finances les informations suivantes :
- le logiciel (et la version) du DBMS ;
- le chemin d'accès à la base de données (et, pour les systèmes basés dans le cloud, la manière d'en obtenir un extrait complet) ;
- le langage de programmation utilisé ;
- un login et un mot de passe pour le SPF Finances.
Il est expressément rappelé aux fabricants de systèmes de caisse qu'ils sont responsables de la manière dont sont sécurisées les données de la base de données relatives aux events précités. Lors de la demande de certification, le fabricant mentionnera les mécanismes de sécurité utilisés (qu'ils soient intégrés dans le logiciel lui-même ou fournis par des tiers).

<a name="Art.103" href="#Art.102">Art.</a> <a href="#Art.104"> 103</a>. Un formulaire de demande sera disponible électroniquement sur le site web du SPF Finances (www.systemedecaisseenregistreuse.be), qui doit être complété et envoyé pour chaque demande.
Le SPF Finances met également à disposition un manuel de certification.

<a name="Art.104" href="#Art.103">Art.</a> <a href="#Art.105"> 104</a>. Toute demande qui ne comprendrait pas l'ensemble des documents et rapports requis sera renvoyée au demandeur par le service compétent du SPF Finances en vue d'être complétée. La procédure de certification ne sera officiellement lancée qu'après réception de tous les documents demandés.

<a name="Art.105" href="#Art.104">Art.</a> <a href="#Art.106"> 105</a>. Au moins un appareil en état de marche doit être mis à la disposition du service compétent du SPF Finances. Pour le FDM, il s'agit d'au moins trois appareils en état de marche.
Conformément à l'article 2, § 1er, dernier alinéa de l'arrêté royal du 1er octobre 2013 relatif aux modalités d'application concernant la certification d'un système de caisse enregistreuse, ces appareils sont conservés au service compétent du SPF Finances comme point de référence pour le certificat. Pour chaque modèle individuel, il sera décidé d'un commun accord de ce qui sera spécifiquement conservé par le SPF Finances et sous quelle forme (matériel, virtualisation, image, etc.).
Les fabricants de FDM mettront à la disposition du service compétent du SPF Finances le même simulateur FDM que celui proposé aux développeurs de logiciels de caisse intéressés.

<a name="Art.106" href="#Art.105">Art.</a> <a href="#LNK0051"> 106</a>. Le service compétent du SPF Finances peut encore demander des informations complémentaires après le début de la procédure de certification, si les documents et informations décrits ci-dessus semblent incomplets et/ou pour éclaircir les renseignements obtenus. Le demandeur dispose d'un délai d'un mois pour y répondre. En l'absence de réponse dans ce délai, la demande de certification est considérée comme retirée. Le demandeur peut toujours demander une prolongation du délai mentionné ci-dessus, au moyen d'un courrier motivé qui doit parvenir au service compétent du SPF Finances avant la date d'échéance initiale.

<a name="LNK0051" href="#LNKR0051">Sous-section 4.</a> - Déroulement de la procédure de certification

<a name="Art.107" href="#Art.106">Art.</a> <a href="#Art.108"> 107</a>. La certification d'un système de caisse comporte deux grands volets :
- dossier de vérification : vérifier si les tests effectués garantissent de manière suffisante la conformité du système de caisse ;
- test du système de caisse : effectuer des tests fonctionnels, y compris des simulations, et vérifier la communication avec le FDM.
La certification se concentrera principalement sur les fonctions du système de caisse et comprendra au minimum l'analyse des points suivants, qui sont également mentionnés dans le manuel de certification que le SPF Finances mettra à disposition des fabricants :
- le (bon) fonctionnement des fonctions obligatoires ;
- l'impossibilité d'utiliser des fonctions interdites ;
- vérifier si tous les types d'events et de transaction sont possibles et correctement indiqués ;
- vérifier si le système de caisse peut correctement communiquer avec n'importe quel FDM certifié ;
- vérifier si le système de caisse convertit correctement les events dans les JSON et réagit correctement aux réponses du FDM ;
- vérifier si le système de caisse arrête effectivement de fonctionner si le buffer du FDM est rempli ;
- contrôler la conformité aux dispositions techniques de l'arrêté ministériel et aux descriptions détaillées.

<a name="Art.108" href="#Art.107">Art.</a> <a href="#LNK0052"> 108</a>. La certification d'un FDM comporte deux grands volets :
- un dossier de vérification : vérifier si les tests effectués garantissent de manière suffisante la conformité du système de caisse ;
- les tests techniques du FDM : conformité aux exigences techniques minimales, vérification des fonctions obligatoires et interdites, vérification des performances, évaluation de la fiabilité (concept technique et stockage de la mémoire), réalisation d'essais fonctionnels et de régression, y compris des simulations, remplissage automatique de la mémoire avec les données de transaction et examen des données stockées (exactitude des calculs, vérification que les données ne peuvent pas être corrompues), vérification de la communication entre le système de caisse et le FDM (en particulier la gestion des mutations dans le service GraphQL) et entre le FDM et les serveurs du SPF Finances (protocole, JSON, etc.).
Le respect des normes contenues dans le marquage CE est garanti par le fabricant. Le fabricant fournit les déclarations nécessaires à cet effet.
En cas de doute sérieux, le SPF Finances se réserve le droit de faire tester le dispositif par un organisme de certification accrédité, aux frais du demandeur.
La certification par le service compétent du SPF Finances ne garantit PAS la conformité aux normes européennes contenues dans le marquage CE global. La conformité est en effet garantie par le fabricant lui-même.

<a name="LNK0052" href="#LNKR0052">Sous-section 5.</a> - Attribution du certificat

<a name="Art.109" href="#Art.108">Art.</a> <a href="#Art.110"> 109</a>. Si l'examen indique que le système de caisse soumis ou le FDM soumis ne satisfait pas aux exigences techniques, le service compétent du SPF Finances informe le fabricant ou l'importateur. Ce dernier peut alors soit retirer sa demande, soit adapter le produit aux remarques et le soumettre à nouveau pour certification.
Si, après adaptation, le système de caisse soumis ou le FDM soumis ne satisfait pas aux exigences techniques, le certificat sera refusé. Le fabricant ne peut représenter à la certification le même produit adapté qu'après 3 mois, ce qui lui permet de développer davantage le produit et de le tester.

<a name="Art.110" href="#Art.109">Art.</a> <a href="#Art.111"> 110</a>. 1° Si l'examen indique que le système de caisse soumis ou le FDM soumis satisfait aux conditions techniques, le fabricant ou importateur est informé.
Pour un système de caisse : le fabricant ou importateur reçoit du service compétent du SPF Finances un certificat mentionnant le numéro d'identification du fabricant (CXXX) et le numéro de certificat pour ce fabricant (NNN). La combinaison du numéro d'identification et du numéro de certificat constitue la base pour les numéros de fabrication. La version du logiciel est toujours mentionnée sur le certificat.
Pour un FDM: le fabricant/l'importateur reçoit du service compétent du SPF Finances un certificat mentionnant le numéro d'identification du fabricant ou importateur (AAA) et le numéro de certificat du fabricant ou importateur (BB), qui, entre autres, serviront de base pour les numéros de fabrication uniques.
2° La notification et le certificat seront envoyés à l'adresse du demandeur reprise dans le dossier de demande. Sur le certificat, le numéro de version est toujours mentionné.
3° Le SPF Finances conserve un exemplaire du rapport de test et de la documentation reçue, ainsi que les exemplaires-modèles sur lesquels les tests ont été effectués.
4° Les données relatives au produit et au certificat sont chargées dans la banque de données d'enregistrement par le SPF Finances.
5° L'attribution du certificat est également publiée sur le site internet prévu par l'administration dans le cadre du "système de caisse enregistreuse", accessible via le portail global du SPF Finances.

<a name="Art.111" href="#Art.110">Art.</a> <a href="#LNK0053"> 111</a>. Le SPF Finances insiste sur le fait que les travaux de certification se limitent exclusivement à ce qui est décrit dans l'arrêté royal du 1er octobre 2013 (Moniteur belge du 8 octobre 2013) pris en exécution de la loi du 30 juillet 2013 relative à la certification d'un système de caisse enregistreuse, comme adapté par les articles 101 à 103 de la loi portant des dispositions fiscales diverses du 28 décembre 2023 et du présent arrêté ministériel.
Le certificat délivré par le service compétent du SPF Finances ne couvre pas les fonctions de l'élément concerné du système de caisse enregistreuse, qui n'ont pas été documentées dans le dossier soumis par le demandeur.

<a name="LNK0053" href="#LNKR0053">Sous-section 6.</a> - Obligations après la certification

<a name="Art.112" href="#Art.111">Art.</a> <a href="#Art.113"> 112</a>. Garantie de fabrication
Dès qu'un fabricant a reçu un certificat pour son modèle de système de caisse ou de FDM, il garantit que chaque exemplaire fabriqué pour fonctionner en tant qu'élément d'un système de caisse enregistreuse et pour être vendu sur le marché belge est identique à l'exemplaire soumis pour certification.
Pour un système de caisse, cette garantie sera, entre autres, assurée par la fourniture de la hash value, calculée soit sur le code source complet du logiciel de caisse, soit sur les éléments pertinents du programme. Pour le calcul de cette hash value, au moins un SHA-1 doit être généré.

<a name="Art.113" href="#Art.112">Art.</a> <a href="#LNK0054"> 113</a>. Modifications
1° Dans le cas où le fabricant ou importateur souhaite apporter des modifications à un système de caisse déjà certifié ou à un FDM déjà certifié, il est tenu de démarrer une nouvelle procédure de certification. Le service compétent du SPF Finances décide, sur la base des changements renseignés, dans quelle mesure la procédure de test doit être recommencée (totalement ou partiellement). La suite est identique à la procédure décrite ci-dessus.
Le fabricant ou importateur communique les modifications apportées au produit au service compétent du SPF Finances, et ce, au moins un mois avant de mettre la nouvelle version sur le marché belge.
Toute modification relative à l'identité du fabricant ou importateur doit être immédiatement communiquée au service compétent du SPF Finances.
2° Hormis l'élimination de bugs critiques, les updates ayant trait aux fonctions telles que visées dans le présent arrêté doivent être limités à/regroupés à 12 updates par année civile.
Pour permettre au service compétent du SPF Finances d'examiner les changements mentionnés ci-dessus, le fabricant fournit les éléments suivants :
- la nouvelle version du logiciel (de préférence installée par le fabricant lui-même) ;
- une release note décrivant en détail les changements et les modifications ;
- les informations concernant la garantie du produit.
3° A l'exception des modifications en vue de corriger les bugs critiques, qui peuvent être effectuées immédiatement, le service compétent du SPF Finances dispose de 15 jours pour rendre sa décision à propos de l'update, à moins que des renseignements complémentaires doivent être fournis. Dans ce cas, le service compétent dispose d'un nouveau délai supplémentaire de 15 jours, à compter de la réception des renseignements demandés pour prendre une décision. L'update ne pourra être commercialisé qu'à l'issue de cette période et à condition d'en avoir reçu l'autorisation du service compétent.
4° Si un nouveau certificat doit être demandé, la suite est identique à la procédure décrite ci-dessus. Les modalités pratiques sont décrites dans le manuel de certification.
5° Toute modification relative à l'identité du fabricant ou importateur doit être immédiatement communiquée au service compétent du SPF Finances.

<a name="LNK0054" href="#LNKR0054">Sous-section 7.</a> - Récupération de l'exemplaire-modèle

<a name="Art.114" href="#Art.113">Art.</a> <a href="#LNK0055"> 114</a>. Lorsqu'une procédure de certification est arrêtée (pour cause de non-attribution de certificat ou de retrait volontaire), le fabricant peut venir chercher l'exemplaire-modèle (les exemplaires-modèles) fourni(s) auprès du service compétent du SPF Finances. Il dispose de six mois après l'arrêt de la procédure pour venir le chercher. Après cette période, le SPF Finances devient définitivement propriétaire de ce matériel et peut en disposer librement.

<a name="LNK0055" href="#LNKR0055">Section 2.</a> - Procédure d'enregistrement

<a name="Art.115" href="#Art.114">Art.</a> <a href="#Art.116"> 115</a>. L'article 2bis de l'arrêté royal du 30 décembre 2009, l'article 4 de la loi du 30 juillet 2013 relative à la certification d'un système de caisse enregistreuse et l'article 5 de l'arrêté royal du 1er octobre 2013 relatif aux modalités d'application en ce qui concerne la certification d'un système de caisse enregistreuse prévoient l'enregistrement, par toutes les personnes concernées, de tous les éléments du système de caisse enregistreuse, à savoir :
- le système de caisse ;
- le FDM.

<a name="Art.116" href="#Art.115">Art.</a> <a href="#Art.117"> 116</a>. Après l'octroi de son premier certificat, le fabricant ou importateur est enregistré dans le module d'enregistrement par le service compétent du SPF Finances, qui lui accorde ensuite l'accès à cette application internet par le biais de la procédure CSAM.
Quand le fabricant ou importateur produit à la fois un système de caisse et un FDM, ils doivent alors s'inscrire séparément pour chacun des deux produits.
Les changements des personnes responsables des enregistrements (s'il s'agit de fabricants/importateurs ou de distributeurs) doivent être communiqués au préalable au service compétent du SPF Finances, afin de pouvoir adapter les droits d'accès à temps.

<a name="Art.117" href="#Art.116">Art.</a> <a href="#Art.118"> 117</a>. 1° Lorsque le premier certificat est accordé à un fabricant ou importateur, il reçoit un code d'identification (AAA pour un FDM, CXXX pour un système de caisse). Sur cette base, le préfixe du modèle certifié est créé, qui sert de base à la création des numéros de production individuels des appareils. Conformément aux dispositions des articles 46 et 70 du présent arrêté, ils sont composés comme suit :
- pour un système de caisse : CXXXNNN, suivi de 7 caractères ;
- pour un FDM : AAABB, suivi de 6 caractères.
2° Le certificat et le préfix, mentionné dans le point 1° seront enregistrés dans l'application internet par le service compétent du SPF Finances.

<a name="Art.118" href="#Art.117">Art.</a> <a href="#Art.119"> 118</a>. Dès qu'un lot d'un système de caisse ou FDM est fabriqué/prêt à être livré à destination du marché belge comme élément d'un système de caisse enregistreuse, tel que visé dans le présent arrêté ministériel, le fabricant ou importateur doit enregistrer la série de numéros de production via l'application internet.

<a name="Art.119" href="#Art.118">Art.</a> <a href="#LNK0056"> 119</a>. Dès qu'un fabricant ou importateur livre un système de caisse ou un FDM à un distributeur, il doit en informer le SPF Finances sans délai, via l'application internet. Les données suivantes lui seront, au minimum, demandées :
- l'identification du distributeur (numéro d'identification à la T.V.A.) ;
- la date de livraison ;
- les numéros de fabrication des appareils livrés.
La livraison d'un FDM ou d'un système de caisse doit être enregistrée à la première des deux dates suivantes :
- celle où le distributeur en devient le propriétaire juridique ;
- celle où le distributeur a physiquement la pièce en sa possession.

<a name="LNK0056" href="#LNKR0056">CHAPITRE 2.</a> - Obligations du distributeur d'éléments du système de caisse enregistreuse

<a name="Art.120" href="#Art.119">Art.</a> <a href="#Art.121"> 120</a>. Chaque entreprise qui veut vendre (livrer et facturer) un système de caisse ou FDM, destiné à être utilisé dans un système de caisse enregistreuse, à un contribuable, opérateur ou distributeur, doivent s'identifier, au préalable, comme tel auprès du SPF Finances.
Cette inscription se fait via l'application internet. Les informations à fournir sont au minimum les suivantes :
- l'identité complète du distributeur (numéro d'identification à la T.V.A., dénomination sociale, forme juridique, adresse, personne de contact, téléphone, e-mail, site internet) ;
- l'adresse des points de distribution et des points de vente ;
- une brève description des références et produits.
Le service compétent du SPF Finances valide cette demande d'enregistrement après examen administratif.
Le fabricant ou importateur qui souhaite livrer directement aux utilisateurs finaux ne doit pas seulement s'enregistrer en tant que fabricant ou importateur, mais également en tant que distributeur.
Les changements des personnes responsables des enregistrements (s'il s'agit de fabricants, importateurs ou de distributeurs) doivent être communiqués au préalable au service compétent du SPF Finances, afin de pouvoir adapter les droits d'accès à temps.

<a name="Art.121" href="#Art.120">Art.</a> <a href="#LNK0057"> 121</a>. Dès que le distributeur livre un ou plusieurs éléments des systèmes de caisse enregistreuse à l'utilisateur final, l'assujetti-exploitant, il doit en informer le SPF Finances sans délai via l'application internet. Sur cette page, les données suivantes doivent au minimum être remplies :
- l'identification de l'assujetti-exploitant (numéro d'identification à la T.V.A., nom, adresse) ;
- l'identification de l'établissement d'exploitation (enseigne, adresse, lieu d'installation) ;
- la date de livraison ;
- le (les) numéro(s) de fabrication du (des) appareil(s) livré(s).
Dans l'hypothèse où le distributeur revend un ou plusieurs composants des systèmes de caisse enregistreuse à un autre distributeur, il doit également en informer le SPF Finances sans délai, via la page prévue à cet effet dans l'application internet, et sur laquelle les informations suivantes doivent au minimum être fournies :
- l'identification de l'autre distributeur (numéro d'identification à la T.V.A., dénomination sociale, forme juridique, adresse) ;
- la date de livraison ;
- les numéros de fabrication des appareils revendus.

<a name="LNK0057" href="#LNKR0057">CHAPITRE 3.</a> - Obligations de l'utilisateur du système de caisse enregistreuse

<a name="Art.122" href="#Art.121">Art.</a> <a href="#Art.123"> 122</a>. Toute entreprise qui, en vertu de l'article 21bis de l'arrêté royal n° 1 relatif au régime de paiement de la taxe sur la valeur ajoutée, est tenue d'utiliser un système de caisse enregistreuse pour l'enregistrement de ses opérations sortantes, pour lesquelles elle n'est pas tenue de délivrer une facture, doit s'inscrire en tant qu'utilisateur d'un système de caisse enregistreuse. Cette inscription se fait toujours via l'application internet du SPF Finances prévue à cet effet.

<a name="Art.123" href="#Art.122">Art.</a> <a href="#Art.124"> 123</a>. Pour rendre le système de caisse enregistreuse opérationnel, l'assujetti-exploitant doit valider via l'application internet les livraisons des éléments de son SCE (système de caisse et FDM). Il relie ensuite dans l'application la (les) caisse(s) au(x) FDM correct(s). Une fois cette étape complétée, le SCE peut être rendu opérationnel et le FDM tentera de se connecter aux serveurs du SPF Finances.

<a name="Art.124" href="#Art.123">Art.</a> <a href="#Art.125"> 124</a>. Si le FDM ne se trouve pas dans l'établissement et qu'il est connecté à la caisse enregistreuse via un réseau (réseau interne, Internet, etc.), la caisse enregistreuse ne pourra plus communiquer avec le FDM en cas de défaillance de ce réseau. En conséquence, il sera impossible de continuer à enregistrer des transactions sur le SCE.
En cas de panne importante du SCE, l'assujetti-exploitant doit informer le service compétent du SPF Finances par e-mail (au début et à la fin de la panne).

<a name="Art.125" href="#Art.124">Art.</a> <a href="#Art.126"> 125</a>. La mise hors service
1° Un système de caisse et/ou un FDM peut être mis hors service par un assujetti-exploitant pour diverses raisons : irrévocablement défectueux, revente ou cession à un autre assujetti-exploitant, revente à un distributeur de systèmes de caisse ou reprise par ce dernier.
L'assujetti-exploitant doit alors effectuer sans délai les formalités nécessaires, via l'application internet. Dans ce cas, l'attention est particulièrement attirée sur l'obligation de conservation légale relative aux données stockées dans le système de caisse.
2° En exception au point 1°, un FDM ne peut sous aucun prétexte être cédé par un assujetti-exploitant à un autre assujetti-exploitant. Le FDM contient en effet des données qui restent des éléments de la comptabilité.

<a name="Art.126" href="#Art.125">Art.</a> <a href="#LNK0058"> 126</a>. L'assujetti-utilisateur d'un système de caisse enregistreuse est responsable de la conservation des données créées par le système de caisse conformément à la législation sur la T.V.A. (et, par extension, à la législation comptable). Ainsi, l'assujetti-utilisateur est notamment responsable de la conservation des données sur le système de caisse et sur le FDM. Les sauvegardes créées des données de caisse font toujours partie du système de caisse et sont donc soumises aux mêmes délais de conservation.

<a name="LNK0058" href="#LNKR0058">TITRE IV.</a> - SANCTIONS - MOYENS DE RECOURS

<a name="LNK0059" href="#LNKR0059">CHAPITRE 1er.</a> - Sanctions relatives à la certification d'éléments du système de caisse enregistreuse

<a name="Art.127" href="#Art.126">Art.</a> <a href="#Art.128"> 127</a>. 1° Lorsque le service compétent du SPF Finances constate que le producteur ou l'importateur ne respecte les obligations visées aux articles 97 à 122, ou est en défaut à l'égard d'une ou plusieurs de ces obligations, il est informé par écrit afin de rétablir le respect de ces obligations. Le certificat est suspendu pendant deux mois.
2° Si le(s) manquement(s) subsiste(nt) dans le chef du fabricant ou de l'importateur, le SPF Finances peut retirer le certificat.

<a name="Art.128" href="#Art.127">Art.</a> <a href="#LNK0060"> 128</a>. 1° S'il est constaté que ces appareils ont été installés en tant qu'éléments d'un système de caisse enregistreuse, mais qu'ils ne sont pas conformes au certificat et/ou qu'ils ne satisfont pas aux conditions fixées dans le présent arrêté ministériel, le fabricant ou importateur est informé par écrit par le service compétent.
2° Cette information suspend le certificat durant deux mois à compter de la date de réception (article 5 de la loi du 30 juillet 2013, relative à la certification d'un système de caisse enregistreuse et article 6, § 2, de l'arrêté royal relatif aux modalités d'application en ce qui concerne la certification d'un système de caisse enregistreuse).
3° Après examen par le SPF Finances, le certificat peut être définitivement retiré.
4° Le retrait du certificat a automatiquement pour conséquence que tous les systèmes de caisse enregistreuse qui utilisent le système de caisse dont la certification a été retirée ou le FDM dont la certification a été retirée, ne satisfont plus aux exigences formulées dans l'arrêté royal du 30 décembre 2009 fixant la définition et les conditions auxquelles doit répondre un système de caisse enregistreuse.
5° Le SPF Finances informe les utilisateurs de ce système de caisse enregistreuse du retrait du certificat. Conformément à l'article 7 de l'arrêté royal du 1er octobre 2013 relatif aux modalités d'application en ce qui concerne la certification d'un système de caisse, ces utilisateurs doivent à nouveau disposer d'un système certifié complet dans les trois mois qui suivent.
Si un utilisateur estime que son (ses) appareil(s) satisfait (satisfont) bien aux exigences du certificat, il doit en informer le service compétent du SPF Finances dans le mois. Le SPF Finances viendra juger sur place de la conformité dans le mois qui suit la réception de cette information.

<a name="LNK0060" href="#LNKR0060">CHAPITRE 2.</a> - Moyens de recours relatifs à la révocation/le refus du certificat

<a name="Art.129" href="#Art.128">Art.</a> <a href="#LNK0061"> 129</a>. Si le fabricant estime que la décision de l'administration de refuser ou de retirer le certificat n'est pas justifiée (et que son produit est entièrement conforme aux exigences techniques) il peut, conformément aux dispositions de l'article 569, 32 ° du Code judiciaire, introduire un recours par citation contre cette décision auprès du tribunal de première instance de Bruxelles.

<a name="LNK0061" href="#LNKR0061">CHAPITRE 3.</a> - Sanctions relatives a l'enregistrement des éléments d'un système de caisse enregistreuse

<a name="Art.130" href="#Art.129">Art.</a> <a href="#Art.131"> 130</a>. Si, chez un assujetti-exploitant, un élément de son système de caisse enregistreuse n'est pas enregistré conformément à la procédure mentionnée dans cet arrêté, cela impliquera que le système de caisse installé dans cet établissement N'EST PAS conforme aux exigences indiquées dans l'arrêté royal du 30 novembre 2009 fixant la définition et les conditions auxquelles doit répondre un système de caisse enregistreuse. Cette infraction peut entrainer l'imposition de l'amende administrative prévue dans la section 2, rubrique II.A de l' arrêté royal n° 44 fixant le montant des amendes fiscales non proportionnelles en matière de taxe sur la valeur ajoutée.

<a name="Art.131" href="#Art.130">Art.</a> <a href="#LNK0062"> 131</a>. Le non-enregistrement des éléments d'un système de caisse enregistreuse par des fabricants ou importateurs et distributeurs peut entrainer l'imposition de l'amende administrative prévue dans la section 6 de l'arrêté royal n° 44 fixant le montant des amendes fiscales non proportionnelles en matière de taxe sur la valeur ajoutée.

<a name="LNK0062" href="#LNKR0062">TITRE V.</a> - DISPOSITIONS FINALES

<a name="Art.132" href="#Art.131">Art.</a> 132. Cet arrêté remplace la Circulaire AGFISC N° 33/2016 (E.T. 124.747) du 8 novembre 2016 (Moniteur belge 16 janvier 2017).
