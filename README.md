# praenomen2genus
<dl>
  <dt>praenomen</dt>
  <dd>fornavn.</dd>

  <dt>genus</dt>
  <dd>kjønn</dd>
</dl>
Quick-fix for å konvertere norske egennavn til kjønn (mann/kvinne).
Siste versjon av kode som tidligere het `Navn-til-kj-nn`.


Målet med denne versjonen av koden er bare å forenkle slik at dette kan brukes fort-og-gæli som et bedre-enn-ingenting verktøy.

Omtrent slik er den ment å brukes:

```python
>>> from praenomen2genus import praenomen2genus
>>> genies = praenomen2genus()
>>> genies.get_gender("Eirik")
(u'Eirik', 'man', 'list_lookup')
>>> genies.get_gender("Ulerikka")
(u'Ulerikka', 'kvinne', 'predictor')
```

Navnet `Eirik` ble funnet i listen, mens `Ulerikka` ikke ligger i listen, men ble predikert av maskin-lærings-algoritmen.


Prosjektet er basert på løse tråder herfra: https://github.com/eiriks/genderPredictor

Jeg har noe data på hvor nøyaktig dette er et-eller-annet sted, som jeg skal hoste opp neste gang jeg må rapportere nøyaktighet (som helt sikkert skjer en-gang snart).

PS: Hvis du har noen alternative løsningsforslag til denne oppgaven ("gi meg ditt navn, og jeg skal si deg hvilket kjønn du er"), gi gjerne en lyd.

Har fått noen fine navnelister av Ivar Utne:
* http://www.uib.no/lle/23537/fornavnslister
* http://www.uib.no/lle/23822/navnestatistikk-fra-mange-land
* http://ssb.no/navn (ut over de helt innlysende listen herfra)

# Nøyaktighet
Da tradisjonelle norske navn er et ganske lite knippe navn som brukes ofte, og som har liten grad av tvetydighet når det kommer til kjønn blir nøyaktigheten ganske bra, da mange Ola og Kari telles rett gang på gang.
Jeg kjørte f.eks. dette over alle navnene i [Norsk Biografisk Leksikon (NBL)](https://no.wikipedia.org/wiki/Wikipedia:Norsk_biografisk_leksikon/artikler) og får rett kjønn på `97.83%`.
eller
`Riktige: 5715 og feil 127 gir en prosent på 97.83`
Dette forklares også med at navnelistene plukker opp da aller fleste navnene. (Det er dog fint å ha AI'n som backup da det ofte er bedre med et gjett enn bare tomme felter).

## Nøyaktighet2
Mye av den høye nøyaktigheten kan spores i at de samme Ola og Kari går igjen gang på gang. Ved å kun kjøre unike navn (Ola får kun kjøre en eneste gang) får vi følgende nøyaktighet på NBL: `92.57%`
Ved at:
```python
len(navn)  5842
len(set(navn))   1265
# altså har vi 1265 unike fornavn i datasettet
Riktige: 1171 og feil 94 gir en prosent på 92.57
```
Feilene kan jo være informative å legge ved:
```python
('Øvre', 'kvinne', 'predictor')
('Willi', 'kvinne', 'predictor')
('Ludwig', 'kvinne', 'predictor')
('Hartvig', 'kvinne', 'predictor')
('Quiwe', 'kvinne', 'predictor')
('Såda', 'kvinne', 'predictor')
('Kaci', 'man', 'predictor')
('G', 'kvinne', 'predictor')
('Vidkunn', 'kvinne', 'predictor')
('Th', 'kvinne', 'predictor')
('Gjeble', 'kvinne', 'predictor')
('Fam', 'man', 'predictor')
('Annik', 'man', 'predictor')
('Gidsken', 'man', 'predictor')
('Gunde', 'kvinne', 'predictor')
('Katti', 'man', 'predictor')
('Tharald', 'man', 'predictor')
('Engebret', 'kvinne', 'predictor')
('Lillebil', 'man', 'predictor')
('Lillemor', 'man', 'predictor')
('Dore', 'kvinne', 'predictor')
('A', 'kvinne', 'predictor')
('Ulvljot', 'kvinne', 'predictor')
('Ellisif', 'man', 'predictor')
('Auguste', 'kvinne', 'predictor')
('Sossen', 'man', 'predictor')
('Bjørnstjerne', 'kvinne', 'predictor')
('Pola', 'kvinne', 'predictor')
('Volrath', 'kvinne', 'predictor')
('Aadel', 'man', 'predictor')
('Botten', 'man', 'predictor')
('Herlaug', 'kvinne', 'list_lookup')
('Havtore', 'kvinne', 'predictor')
('Rauni', 'man', 'predictor')
('Palle', 'kvinne', 'predictor')
('Guy', 'kvinne', 'predictor')
('Kim', 'man', 'predictor')
('Lul', 'man', 'predictor')
('Helly', 'kvinne', 'predictor')
('Willie', 'kvinne', 'list_lookup')
('Hagbarth', 'kvinne', 'predictor')
('Tønne', 'kvinne', 'predictor')
('Hilchen', 'man', 'predictor')
('Grethe,', 'man', 'predictor')
('Heyerdahl,', 'man', 'predictor')
('Margareta', 'kvinne', 'list_lookup')
('Eindride', 'kvinne', 'predictor')
('Sørle', 'kvinne', 'predictor')
('Bokken', 'man', 'predictor')
('Nico', 'man', 'list_lookup')
('Gösta', 'kvinne', 'predictor')
('Babbis', 'man', 'predictor')
('Valgerd', 'man', 'predictor')
('Thorry', 'kvinne', 'predictor')
('Knute', 'kvinne', 'predictor')
('Geburg', 'kvinne', 'predictor')
('Dikken', 'man', 'predictor')
('Otte', 'kvinne', 'predictor')
('Cleng', 'kvinne', 'predictor')
('Skofte', 'kvinne', 'predictor')
('Sig', 'kvinne', 'predictor')
('Zinken', 'man', 'predictor')
('Signi', 'man', 'predictor')
('Mon', 'man', 'predictor')
('Skule', 'kvinne', 'predictor')
('Westye', 'kvinne', 'predictor')
('Torberg', 'kvinne', 'predictor')
('Frede', 'kvinne', 'predictor')
('Eske', 'kvinne', 'predictor')
('Adelsteen', 'kvinne', 'predictor')
('Jolly', 'kvinne', 'predictor')
('E', 'kvinne', 'predictor')
('Eugène', 'kvinne', 'predictor')
('Ridley', 'kvinne', 'predictor')
('Køla', 'kvinne', 'predictor')
('“lille', 'kvinne', 'predictor')
('Gørvel', 'man', 'predictor')
('Truid', 'kvinne', 'predictor')
('Anneken', 'man', 'predictor')
('Joronn', 'man', 'predictor')
('Jeremi', 'kvinne', 'predictor')
('Hellmuth', 'kvinne', 'predictor')
('Torvild', 'kvinne', 'predictor')
('Strange', 'kvinne', 'predictor')
('“grynet”', 'man', 'predictor')
('Tyge', 'kvinne', 'predictor')
('Dyre', 'kvinne', 'predictor')
('Torrey', 'kvinne', 'predictor')
('Gisken,', 'man', 'predictor')
('Svale', 'kvinne', 'predictor')
('Moltke', 'kvinne', 'predictor')
('Brynild', 'kvinne', 'predictor')
('Sigtrygg', 'kvinne', 'predictor')
('Iben', 'man', 'predictor')
```

Dette er da altså navn som `navn-til-kjønn` tar feil av, gitt "fasitten" på [wikipedia artikelen om Norsk Biografisk Leksikon (NBL)](https://no.wikipedia.org/wiki/Wikipedia:Norsk_biografisk_leksikon/artikler).

Det kunne jo være fristende å legge disse feilene inn i navnelistene, men da de er rimelig uvanlige, så lar jeg de være for denne gang. Du kan selv legge dem inn hvis du ser behovet.

NB: Denne typen nøyaktighet som er gjort her (kun tillate unike navn) gir urimelig lave forventninger til programvaren gitt "normale" norske navn, da vi jo navngir de fleste
norske barn med enda flere Ola, Oscar, Silje og Mari´r. Det er kun en demonstrasjon av begrensningene gitt metoden på et reelt datasett.
