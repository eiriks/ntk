# Navn-til-kjønn
Quick-fix for å konvertere norske egennavn til kjønn (mann/kvinne).


Målet med denne versjonen av koden er bare å forenkle slik at dette kan brukes fort-og-gæli som et bedre-enn-ingenting verktøy.

Omtrent slik er den ment å brukes:

```python
>>> from name2gender import name2gender
>>> name_genie = name2gender()
>>> name_genie.get_gender("Eirik")
(u'Eirik', 'man', 'list_lookup')
>>> name_genie.get_gender("Ulerikka")
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
