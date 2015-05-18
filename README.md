# Nnavn-til-kjønn
Quick-fix for å konvertere norske egennavn til kjønn (mann/kvinne).


Målet med denne versjonen av koden er bare å forenkle slik at dette kan brukes fort-og-gæli som et bedre-enn-ingenting verktøy.

Omtrent slik er den ment å brukes:

```python
>>> from name2gender import name2gender
>>> name_genie = name2gender()
>>> name_genie.get_gender("Eirik")
('Eirik', u'man', u'list_lookup')
>>> name_genie.get_gender("Ulerikka")
('Ulerikka', u'kvinne', u'predictor')
```


Prosjektet er basert på løse tråder herfra: https://github.com/eiriks/genderPredictor
