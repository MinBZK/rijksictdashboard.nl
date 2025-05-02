"""import v2 update

Revsion ID: b49569d3f0cf
Revises: f5ef73c7a407
Create Date: 2023-02-15 15:45:00

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "b49569d3f0cf"
down_revision = "f5ef73c7a407"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """
        UPDATE "public"."Antwoord"
        SET "IndicatorId"='85'
        WHERE ("Antwoord"."IndicatorId" = 64)
        AND "AanmaakDatum" < '2023-02-14 18:00:00'
        ;

        UPDATE "public"."Antwoord"
        SET "IndicatorId"='87'
        WHERE ("Antwoord"."IndicatorId" = 66)
        AND "AanmaakDatum" < '2023-02-14 18:00:00'
        ;

        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Belastingen, uitkeringen en toeslagen'
        WHERE ("public"."AntwoordOptie"."Id" = 71)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Bouwen en wonen'
        WHERE ("public"."AntwoordOptie"."Id" = 72)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Internationale samenwerking'
        WHERE ("public"."AntwoordOptie"."Id" = 74)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Klimaat, milieu en natuur'
        WHERE ("public"."AntwoordOptie"."Id" = 75)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Migratie en reizen'
        WHERE ("public"."AntwoordOptie"."Id" = 76)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Overheid en democratie'
        WHERE ("public"."AntwoordOptie"."Id" = 78)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Recht, veiligheid en defensie'
        WHERE ("public"."AntwoordOptie"."Id" = 79)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Verkeer en vervoer'
        WHERE ("public"."AntwoordOptie"."Id" = 80)
        ;

        UPDATE "public"."Antwoord" SET "Waarde"='Belastingen, uitkeringen en toeslagen ' WHERE "IndicatorId" = '22' AND "Antwoord"."Waarde" LIKE '%Belastingen uitkeringen toeslagen en subsidies%';
        UPDATE "public"."Antwoord" SET "Waarde"='Bouwen en wonen' WHERE "IndicatorId" = '22' AND "Antwoord"."Waarde" LIKE '%Bouwen en Wonen%';
        UPDATE "public"."Antwoord" SET "Waarde"='Internationale samenwerking' WHERE "IndicatorId" = '22' AND "Antwoord"."Waarde" LIKE '%Internationale Samenwerking%';
        UPDATE "public"."Antwoord" SET "Waarde"='Klimaat, milieu en natuur' WHERE "IndicatorId" = '22' AND "Antwoord"."Waarde" LIKE '%Klimaat milieu en natuur%';
        UPDATE "public"."Antwoord" SET "Waarde"='Migratie en reizen' WHERE "IndicatorId" = '22' AND "Antwoord"."Waarde" LIKE '%Migratie en Reizen%';
        UPDATE "public"."Antwoord" SET "Waarde"='Overheid en democratie' WHERE "IndicatorId" = '22' AND "Antwoord"."Waarde" LIKE '%Overheid en Democratie%';
        UPDATE "public"."Antwoord" SET "Waarde"='Recht, veiligheid en defensie' WHERE "IndicatorId" = '22' AND "Antwoord"."Waarde" LIKE '%Recht Veiligheid en Defensie%';
        UPDATE "public"."Antwoord" SET "Waarde"='Verkeer en vervoer' WHERE "IndicatorId" = '22' AND "Antwoord"."Waarde" LIKE '%Verkeer en Vervoer%';

        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Agile (Scrum)', "Index"='1'
        WHERE ("public"."AntwoordOptie"."Id" = 598)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Agile (SAFe)', "Index"='0'
        WHERE ("public"."AntwoordOptie"."Id" = 597)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Standaard product', "Index"='3'
        WHERE ("public"."AntwoordOptie"."Id" = 604)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Index"='2'
        WHERE ("public"."AntwoordOptie"."Id" = 603)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Index"='4'
        WHERE ("public"."AntwoordOptie"."Id" = 605)
        ;
        DELETE FROM "public"."AntwoordOptie"
        WHERE ("public"."AntwoordOptie"."Id" = 606)
        ;

        UPDATE "public"."Indicator"
        SET "Toelichting"='Nog niet gestart: nog geen goedgekeurd projectplan (of vergelijkbaar). In uitvoering: gestart, niet in heroriëntatie verkerend, nog niet afgeronde of geannuleerde ICT-activiteit. In heroriëntatie: tijdelijk stilgezette ICT-activiteit waarvan de op het dashboard gepubliceerde gegevens nog niet geactualiseerd kunnen worden. Afgerond: ICT-activiteit waarvoor decharge is verleend. Geannuleerd: ICT-activiteit dat is stopgezet en niet is afgerond.'
        WHERE ("public"."Indicator"."Id" = 23)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='De stuurgroep geeft formeel akkoord voor startdatum van de ICT-activiteit.  Bij een beheer en onderhoud traject: gebruik de datum van decharge als startdatum.'
        WHERE ("public"."Indicator"."Id" = 18)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='IT-deel decharge.  Bij een beheer en onderhoud traject: gebruik eind levensduur.'
        WHERE ("public"."Indicator"."Id" = 20)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Indien er sprake is van een herijking moet de reden van de herijking worden gemeld (er kunnen ook meerdere oorzaken aan een herijking ten grondslag liggen): - Wetswijziging - Wens van de Tweede Kamer/Eerste Kamer - Aanpassing (business) doelen/eisen: nieuwe functionaliteiten, extra data(koppelingen), aanpassing business case, scopewijziging - Implementatie: organisatie- en procesaanpassingen (minder/meer) complex, bewerkelijker - Interne scopewijziging: risico’s, afhankelijkheden terugbrengen/opvoeren - Tegenvallers binnen de ICT-activiteit: complicaties, afstemming leverancier, projectleiding - Overnemen aanbeveling(en) van een extern advies - Prijsontwikkeling'
        WHERE ("public"."Indicator"."Id" = 61)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Welke maatschappelijke baat draagt deze ICT-activiteit het meeste aan bij?  Bij twijfel kan contact opgenomen worden met CIO Rijk.'
        WHERE ("public"."Indicator"."Id" = 55)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Wat zijn de mijlpalen voor deze ICT-activiteit? Probeer deze zo burgervriendelijk mogelijk op te schrijven.  Zijn deze nog niet bekend? Vul dan minimaal de al behaalde resultaten van de activiteit in.'
        WHERE ("public"."Indicator"."Id" = 39)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='"Welk systeem van toerekening is gehanteerd? Besteed aandacht aan: - Het hanteren van het kasverplichtingen-  of baten-lastenstelsel; - De wijze van toerekenen van kosten van intern personeel; - Exploitatiekosten die, ten tijde van de uitvoering, nog als kosten van de ICT-activitei worden meegenomen.'
        WHERE ("public"."Indicator"."Id" = 4)
        ;

        UPDATE "public"."Indicator" SET "Toelichting"='Is een organisatie opdrachtgever van de ICT-activiteit? Vermeld die dan hier.' WHERE "public"."Indicator"."Id" = 24
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Kies het onderwerp waar de ICT-activiteit aan bijdraagt.' WHERE "public"."Indicator"."Id" = 22
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='De peildatum waarop de laatste herijking of rapportage van de informatie is vastgesteld.' WHERE "public"."Indicator"."Id" = 59
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Waarom is deze activiteit opgestart?' WHERE "public"."Indicator"."Id" = 54
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Wat wil je met deze activiteit bereiken?' WHERE "public"."Indicator"."Id" = 25
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Geef aan op welke wijze de software wordt ontwikkeld binnen de ICT-activiteit. Niet op de lijst voorkomende methoden kunnen via functioneel beheer worden toegevoegd aan de lijst.' WHERE "public"."Indicator"."Id" = 17
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Is er sprake van maatwerk (geheel of gedeeltelijk)?' WHERE "public"."Indicator"."Id" = 16
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Er is sprake van een herijking als er een significante wijziging in de scope, doorlooptijd of kostenschatting van de ICT-activiteit plaatsvindt.' WHERE "public"."Indicator"."Id" = 58
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Wie profiteert van deze ICT-activiteit?' WHERE "public"."Indicator"."Id" = 56
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Hoe profiteren zij van deze ICT-activiteit?' WHERE "public"."Indicator"."Id" = 5
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='De belangrijkste externe marktpartijen en hun rol in de ICT-activiteit worden hier gemeld. Niet op de lijst voorkomende marktpartijen kunnen via functioneel beheer worden toegevoegd aan de lijst.' WHERE "public"."Indicator"."Id" = 52
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='De verwachte kosten per jaar voor beheer en onderhoud na de oplevering van de ICT-activiteit.' WHERE "public"."Indicator"."Id" = 1
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Met welke (economische) levensduur van het resultaat is gecalculeerd in de businesscase?' WHERE "public"."Indicator"."Id" = 2
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Als in de businesscast geen (economische) levensduur van het resultaat is gecalculeerd wordt dat hier toegelicht.' WHERE "public"."Indicator"."Id" = 3
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='De nummers worden voorzien van Tweede Kamer dossier- en briefnummer.' WHERE "public"."Indicator"."Id" = 49
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='De hyperlink verwijst naar een specifieke pagina op https://www.officielebekendmakingen.nl.' WHERE "public"."Indicator"."Id" = 51
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Kosten personeel werkzaam aan de ICT-activiteit. Voor ‘eigen’ personeel worden de geschatte en gerealiseerde uitgaven gerapporteerd op basis van het in het (bijgewerkte) projectplan (of vergelijkbaar) begrote en geschatte aantal dagen.' WHERE "public"."Indicator"."Id" = 63
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Kosten personeel werkzaam aan de ICT-activiteit. Voor ‘eigen’ personeel worden de geschatte en gerealiseerde uitgaven gerapporteerd op basis van het in het (bijgewerkte) projectplan (of vergelijkbaar) begrote en geschatte aantal dagen.' WHERE "public"."Indicator"."Id" = 64
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Inhuur van externe personele capaciteit van externe bedrijven ten behoeve van ICT-taken.' WHERE "public"."Indicator"."Id" = 65
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Inhuur van externe personele capaciteit van externe bedrijven ten behoeve van ICT-taken.' WHERE "public"."Indicator"."Id" = 66
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Dit is een samenvoeging van wat voorheen hardware, standaardsoftware en dataverbindingen was. Deze kunnen opgeteld worden. ' WHERE "public"."Indicator"."Id" = 67
        ;
        UPDATE "public"."Indicator" SET "Toelichting"='Dit is een samenvoeging van wat voorheen hardware, standaardsoftware en dataverbindingen was. Deze kunnen opgeteld worden. ' WHERE "public"."Indicator"."Id" = 68
        ;

    """
    op.execute(upgrade_query)


def downgrade() -> None:
    pass
