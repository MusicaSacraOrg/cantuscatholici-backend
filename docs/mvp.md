# MVP

## Databáza piesní / spevníkov
- štítková databáza piesní -> katalóg piesní v ktorom sa bude dať vyhľadávať podľa štítkov, fulltextu, zoraďovať. 
- vyhľadávanie piesní: podľa štítkov a fulltextu
- zoraďovanie piesní: podľa názvu a podľa čísla ktoré má zmysel pre daný spevník
- stránkovanie: requesty obsahujú limit, offset, total
- fuzzy search - piesne podla textu a nazvu s roznou prioritou ([https://github.com/rapidfuzz/RapidFuzz](https://github.com/rapidfuzz/RapidFuzz "https://github.com/rapidfuzz/RapidFuzz"))

###### Pieseň
Obsahuje:
- text (nezavisle od musescore)
- oficiálne noty => musescore file, zobrazujeme svg noty. Musí byť kontrolované že ako oficiálny obsah sa dá pridať len musescore súbor.
- aranzmany, upravy, predohry... (užívateľský obsah): verzie piesní, predohry, dohry, medzihry, satb. Môže byť musescore súbor alebo pdf. 
- tagy
- hymnológiu: description (wysivig editor, rich text), prelinkovanie na spevník aj ako referenciu na nenahraný spevník.
- slávenia, kedy hrať

Funkcie
- exportovať (pdf, svg, text, originál musescore file) 
- transponovať (+, -, original)

###### Tagy
- rozdelené do kategorií
- pri vyhľadávaní podľa tagov je medzi kategóriami logický AND
- pri vyhľadávaní podľa tagov je medzi tagmi logický OR

## Liturgický kalendár
- Mat zoznam slaveni a pravidiel (bez ohľadu na deň v kalendári) -> e.g. Na sviatok Petra Pavla hrať toto a toto
- filtrovanie sviatkov
- mať entity sviatkov 

- časti omše/sviatku by mohli byť statické 

- ako pieseň môže byť vzťah medzi existujucou piesňou v datábazi => vynucovať existenciu piesne

- pozrieť mocky vo frontende pre definovanie kategórií sviatkov a slávení v kalendári

## Užívateľský obsah / interakcia
- mať fallback k non musescore formátu - pdf
- bude môcť pridávať užívateľský obsah k už vytvoreným piesňam

- editovať piesne a pridávať piesne bude kontrolované (v MVP kontrolujeme všetko)

- mať a editovať vlastný profil - fotka, kontakt, rola, description

## Redakcia
- kontrolovať užívatelský obsah
- pridávať a editovať piesne
- editovať obsah kalendáru (oboch kalendarov = kalendár + datábaza sviatkov)

-  mat a editovat vlastny profil

## Admin
- pridávať tagy, kategórie tagov, editovať účty => povyšovať ich role
- pridavat kategorie slaveni

## Authentication
- custom riešenie prihlásenia na email a heslo
- mať refresh token
- užívateľské role user, redactor, admin

## DOCS
- vytvoriť templates pre musescore súbory
- vytvoriť o nás stránku
- vytvoriť donate stránku

## Technické detaily
- errorove hlášky: všetky erorové stavy musia mať pekné hlášky
- backend musí mať swagger dokumentáciu
- bude automatické nasadenie frontendu, backendu na hetzner server.
- automatické migrácie databáze pri nasadení

- ... bude určite ešte doplnené

---


# MVP (nice to have)

- preview pdf verzii ako image (e.g. https://imslp.org/wiki/Ach_Gott_und_Herr%2C_BWV_692_(Bach%2C_Johann_Sebastian))

- [https://github.com/marp-team/marp](https://github.com/marp-team/marp "https://github.com/marp-team/marp") - generovanie prezentácie z textov,

- light/dark mode

- pridať redaktorovi možnosť zisťovania unikátnosti obsahu(piesní) => či náhodou užívateľom piesne už nexistuje (to dať už užívateľovi ako warning pri vytváraní piesne)

- tagy budu mat farbicky

- devová databáza

- zobrazovanie viacstranových nôt , gallery mode

- listing redaktorov

- užívateľ môže zmeniť email
 
### Playlist
- pre registrovaneho užívatela
- zgrupenie piesne do entity playlistu
- linked list, poradie
- piesne v playliste niako otagovat častami omše
- !!! pamätať nastavenia/state piesne skrz cely playlist !!! 

playlist bude mat
- description?, vztah k sviatku 

---

# Future ideas
- spevniky
- ukážky, užívateľský obsah s ukážkami
- analyzovať kontrolovanie uživatelskeho obsahu (kontrolovat vsetko alebo len niake veci)
- monetizovanie (mat plateny obsah, _, _, _)
- blokovanie účtov
- - nezobrazovať piesne bez obsahu (e.g. bez nôt) => mať také filter tlačítko
- socialan siet = zdielanie playlistov
- referencie pre autorov notoveho zapisu,
- monitoring LOL
- support for gregorian chant notation
- mat katalog autorov (alebo aspon odkazovat autorov na linky tretich stran, e.g. wiki. teda autora miesto stringu ukladat ako dvojicu name + link)
- mat tlacitko pre vypnutie zhasinania obrazovky ked clovek hra z apky
- tooltips pri hoverovani na piesne kde sa zobrazia detailnejsie informacie
- implementacia refreshovacich tokenov / pouzitie tretej strany pre auth
- napojenie sa na apkku organisti
- poradie tokenov a kategorii tokenov
- blokovať zhasínanie displeja
- dizajn overhaul
- moznost exclude ostatnych tagov z kategorie
- bulk actions