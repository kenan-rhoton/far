#Presentació del projecte


Amnistia Internacional és una organització no gubernamental que defensa els drets humans arreu del món. A Catalunya busquen prendre acció enfront de qualsevol llei o situació que violi aquests drets, i per a fer-ho han de gestionar moltíssima informació.

És aquí on entra aquest projecte: la cerca i ordenació de la informació.

Aquest projecte busca facilitar el màxim possible que qualsevol notícia d'interés per a Amnistia Internacional sigui inmediatament visible, indexada i accessible. Busca, en el fons, treure el màxim de feina a fer en quant a totes les accions que tenen a veure en la informació, per a que l'organització pugui centrar-se en prendre acció.

I és per això el aquest projecte, com un far, intenta ajudar l'usuari a no perdre's en un mar d'informació, sino tenir al seu abast tota la informació que necessita quan la necessita, automatitzant al màxim totes les cerques i peticions possibles.


#Objectius

El objectiu principal d'aquest projecte es ser útil. El que prima per mi és que la eina desenvolupada compleixi completament la seva funció de facilitar les tasques de cerca d'informació que s'efectúen a Amnistia Internacional Catalunya.

Les tasques que es volen cobrir son:

-   *Detecció de notícies clau* Interessa poder saber cada dia quines notícies de la gran quantitat de fonts d'interés són realment rellevant per les causes que Amnistia Internacional defensa, sense haver de filtar la informació manualment
-   *Indexació de la informació* Es vol que la informació quedi organitzada de manera que sigui fàcil filtrar-la i fer cerques, tant per data, com per contigut, temàtica y font.
-   *Extensibilitat* És important que el sistema es pugui extendre fàcilment, que hi hagi un métode senzill que permeti afegir noves fonts d'informació i idealment que sigui fàcil que algú que no conegui el sistema pugui afegir-hi funcionalitats.
-   *Flexible* El sistema ha de funcionar per fonts de diferents tipus, ja siguin pàgines web com documents amb actualitzacions periòdiques (PDF, DOC, etc.), y ha de ser fàcil canviar els paràmetres de cerca, ja que els temes d'interés varien en el temps.
-   *Usabilitat* El sistema ha de ser senzill i intuitiu, sense requerir uns alts coneixements tècnics pel seu correcte funcionament.
-   *Obert* Finalment, un objectiu personal és que el sistema no només sigui útil per a Amnistia, sinó que, sense cap detriment al funcionament necessitat per ells, pugui tenir múltiples utilitats i pugui potencialment ser utilitzat per tothom que necessiti qualsevol sistema similar.


#Decisions de disseny

En el transcurs del projecte s'han hagut de prendre diferents decisions que han determinat bastant tant la estructura com el funcionament intern del sistema.

##Control de versions: Git

A l'hora d'escollir un sistema de control de versions, no ha tingut massa secret la cosa: senzillament he obtat pel software amb el qual estava més familiartitzat - Git.

En quant a l'us de l'eina, he optat per una filosofia "commit often, worry later" per asegurar que en cas d'haver de revertir qualsevol canvi, hi hauria el mínim de problemes posibles.

I donat que és un projecte en solitari, no he fixat cap estructura de branques.

##Plataforma del sistema: Django

Aquesta decisió ja té més interés: Django potser no és la primera plataforma que ve al cap al pensar una solució per al problema esmentat, però hi han hagut molts motius darrere aquesta decisió:

1.  És una plataforma web: Això vol dir que podem fer el sistema accesible des de qualsevol banda enlloc de ser un programa amb una instal·lació que pot o no ser complicada o depenent del sistema operatiu o requerir un software adicional. Tothom té navegador web, així que fer una solució web crec que soluciona molts més problemes a la llarga.
2.  Té un sistema completament modular: Els projectes de Django consisteixen d'apps independents entre si, i dona moltes eines per fer un sistema 100% modular, cosa que en cas de voler incorporar el sistema dins un altre és increíblement pràctic. També proporciona mòduls molt útils que podem fer servir al projecte, com el mòdul d'administració.
3.  Abstracció de models: Django té el que anomena "models", que són abstraccions de les taules i relacions de la base de dades, cosa que permet estalviarse tota la gestió de la BD a més de permetre ser transparents a quina BD concreta es fa servir (canviar entre SQLite i PostgreSQL per exemple és trivial)
4.  Python: Django és pur Python, cosa que fa que sigui 100% independent de la plataforma a més de ser molt fàcil de entendre i, per casualitats de la vida, ser el meu llenguatge de programació preferit :)
5.  Extensibilitat: Lligat amb la seva modularitat, és molt fàcil ampliar el sistema, degut a que cada cosa té el seu lloc i funció clares, permetent entendre el codi fàcilment i ampliar-ho inclús amb un deesconeixement complert del sistema.
6.  TDD: Realment la clau de Django resideix en que fa molt molt fàcil una aproximació de Test Driven Development degut a les seves classes internes de testeig.

##Metodología de treball: TDD

He escollit desenvolupar el projecte seguint una metodología Test Driven Development (TDD) degut als bons resultats que dona, sobretot envers la detecció i prevenció de bugs. De fet, crec que certes parts d'aquest projecte (les referents al tracte amb PDFs) no haurien sigut gaire solucionables si no fos per aquesta metodología, ja que ha permés detectar errors a l'instant en que alguna cosa no funcionava com hauria, si bé en retrospectiva una millor definició dels tests hauria fet tot encara més senzill i millor: la veritat és que aquest projecte ha sigut tot un gran aprenentatge en TDD.

###Problemàtica i desviacions

Periode no-test

###Els workers la base de dades de testeig de Django

Un problema sorgeix a l'hora de testejar: Django pels test automàticament monta una BD independent que només existeix en memòria i només és accessible pel programa principal.

Això no seria un problema si no fos per un petit detall: per a evitar timeouts a les peticions d'actualitzar una font i poder fer-ho asíncron, hem hagut de fer servir una cua de processos worker, els quals son independents i no poden accedir a aquesta base de dades. És a dir: no son testejables.

Es van buscar alternatives en BDs i la seva gestió a través de Django, però aquest comportament és propi dels test de Django i degut a diverses avantatges de la plataforma és va optar per una altra solució: al testejar fer servir els workers inline. (comparativa)


##Deployment: Heroku

Pel deployment del projecte s'ha decidit fer servir Heroku per diversos motius:

1.  Familiaritat
2.  Support per a Django
3.  Facilitat de control de versions, inmutabillitat
4.  Preu gratuit

###Problemàtiques relacionades amb la plataforma Heroku

Al ser Heroku una plataforma ab filosofia de servidors inmutables, això vol dir que tota informació s'ha de guardar a la base de dades. En particular és un problema per guardar els fitxers de l'estat d'una Font, però per sort existeix un mòdul per a Django que permet guardar fitxers a la BD.

##Funcionament intern: Métode de detecció d'avisos

El métode de detecció dels avisos ha canviat des del plantejament original. Ara enlloc d'una cerca sobre els continguts (limitada per zona), es fa una cerca sobre els canvis.

###Problemàtiques relacionades amb PDFs

La funcionalitar que més problemes ha donat de llarg ha sigut l'anàlisi de PDFs. Això es degut a la seva naturalesa com a format d'impressió, no de dades, completament desestructurat en quant al contingut. Això fa que, a la pràctica, sigui impossible reconèixer els títols,paràgrafs, etc. sense conèixer previament el format, fent que no sigui viable basar el sistema e la detecció d'estructures. De fet, la única cosa que podem extreure amb algún tipus de certesa és el contingut de paraules clau i la seva localització.

###Sistemes provats i descartats

pdfrw (only good for structures)

pdfminer (no python 3)

###PyPDF

PyPDF2 acaba sent la resposta que buscàvem: una biblioteca capaç d'extraure text d0un pdf de manera mitjanament ordenada.


#Informació i Capablitats del Sistema

A continuació detallem les característiques del sistema desenvolupat.

##1. Crear Fonts, un tipus de dades que contenen urls i informació del seu estat

En primer lloc, el sistema permet organitzar les Fonts a les quals volem cercar la informació, fent de base de dades de consulta.

##2. Emmagatzemar l'estat d'una font al accedir-hi

En segon lloc, el sistema pot emmagatzemar l'estat de cada font i detectar quan hhi ha un canvi

##3. Crear Catàlegs, un tipus de dades que emmagatzema paraules clau d'interès per a nosaltres

També permet definir Catàlegs de paraules d'interés per l'usuari.

##4. Troba coincidencias amb els Catàlegs en els canvis que es produeixen a les Fonts

Finalment, pot trobar coincidències amb les paraules claus a qualsevol dels canvis detectats i generar els avisos pertinents.


TO TEST
##5. És capaç de endinsar-se dins de fitxers pdf nous que apareguin a les fonts i extreure'n frases amb les paraules clau.

Cal esmentar també que si el sistema com a canvi detecta un hipervincle a un arxiu, fa una cerca exhaustiva a l'arxiu de les paraules clau i detecta qualsevol aparició.

