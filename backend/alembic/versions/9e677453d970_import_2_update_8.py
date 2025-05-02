"""import 2 update 8 - toelichtingen en baten aanpassen

Revsion ID: 9e677453d970
Revises: c7f1e1620441
Create Date: 2023-03-29 15:29:00

upgrade
NONE
downgrade
NONE

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "9e677453d970"
down_revision = "c7f1e1620441"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """

        DELETE FROM "public"."AntwoordOptie"
        WHERE ("public"."AntwoordOptie"."Id" = 641)
        ;

        UPDATE "public"."Indicator"
        SET "Toelichting"='IT-deel decharge. <br> Bij een beheer en onderhoud traject: gebruik eind levensduur.'
        WHERE ("public"."Indicator"."Id" = 20)
        ;

        UPDATE "public"."Indicator"
        SET "Toelichting"='<B>Nog niet gestart:</B> nog geen goedgekeurd projectplan (of vergelijkbaar). <br> <B>In uitvoering:</B> gestart, niet in heroriëntatie verkerend, nog niet afgeronde of geannuleerde ICT-activiteit.<br> <B>In heroriëntatie:</B> tijdelijk stilgezette ICT-activiteit waarvan de op het dashboard gepubliceerde gegevens nog niet geactualiseerd kunnen worden.<br> <B>Afgerond:</B> ICT-activiteit waarvoor decharge is verleend.<br> <B>Geannuleerd:</B> ICT-activiteit dat is stopgezet en niet is afgerond.'
        WHERE ("public"."Indicator"."Id" = 23)
        ;

        UPDATE "public"."Indicator"
        SET "Toelichting"='De stuurgroep geeft formeel akkoord voor startdatum van de ICT-activiteit. <br> Bij een beheer en onderhoud traject: gebruik de datum van decharge als startdatum.'
        WHERE ("public"."Indicator"."Id" = 18)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='De peildatum waarop de laatste herijking of rapportage van de informatie is vastgesteld.'
        WHERE ("public"."Indicator"."Id" = 94)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Geef aan op welke wijze de software wordt ontwikkeld binnen de ICT-activiteit. ''Standaard product'' doelt op producten die direct in te kopen zijn zonder verdere aanpassingen.<br><br> Niet op de lijst voorkomende methoden kunnen via functioneel beheer worden toegevoegd aan de lijst.'
        WHERE ("public"."Indicator"."Id" = 17)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Indien er sprake is van een herijking moet de reden van de herijking worden gemeld (er kunnen ook meerdere oorzaken aan een herijking ten grondslag liggen):<br> <LI>Wetswijziging</LI> <LI>Wens van de Tweede Kamer/Eerste Kamer</LI> <LI>Aanpassing (business) doelen/eisen: nieuwe functionaliteiten, extra data(koppelingen), aanpassing business case, scopewijziging</LI> <LI>Implementatie: organisatie- en procesaanpassingen (minder/meer) complex, bewerkelijker</LI> <LI>Interne scopewijziging: risico’s, afhankelijkheden terugbrengen/opvoeren</LI> <LI>Tegenvallers binnen de ICT-activiteit: complicaties, afstemming leverancier, projectleiding</LI> <LI>Overnemen aanbeveling(en) van een extern advies</LI> <LI>Prijsontwikkeling</LI>'
        WHERE ("public"."Indicator"."Id" = 33)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Indien er sprake is van een herijking moet de reden van de herijking worden gemeld (er kunnen ook meerdere oorzaken aan een herijking ten grondslag liggen):<br> <LI>Wetswijziging</LI> <LI>Wens van de Tweede Kamer/Eerste Kamer</LI> <LI>Aanpassing (business) doelen/eisen: nieuwe functionaliteiten, extra data(koppelingen), aanpassing business case, scopewijziging</LI> <LI>Implementatie: organisatie- en procesaanpassingen (minder/meer) complex, bewerkelijker</LI> <LI>Interne scopewijziging: risico’s, afhankelijkheden terugbrengen/opvoeren</LI> <LI>Tegenvallers binnen de ICT-activiteit: complicaties, afstemming leverancier, projectleiding</LI> <LI>Overnemen aanbeveling(en) van een extern advies</LI> <LI>Prijsontwikkeling</LI>'
        WHERE ("public"."Indicator"."Id" = 61)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Wie profiteert van deze ICT-activiteit?'
        WHERE ("public"."Indicator"."Id" = 56)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Wat zijn de mijlpalen voor deze ICT-activiteit? Probeer deze zo burgervriendelijk mogelijk op te schrijven.<br><br>  Zijn deze nog niet bekend? Vul dan minimaal de al behaalde resultaten van de activiteit in.'
        WHERE ("public"."Indicator"."Id" = 39)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Als in de businesscast geen (economische) levensduur van het resultaat is gecalculeerd wordt dat hier toegelicht.'
        WHERE ("public"."Indicator"."Id" = 3)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Welk systeem van toerekening is gehanteerd? Besteed aandacht aan:<br> <LI>Het hanteren van het kasverplichtingen- of baten-lastenstelsel;</LI> <LI>De wijze van toerekenen van kosten van intern personeel;</LI> <LI>Exploitatiekosten die, ten tijde van de uitvoering, nog als kosten van de ICT-activiteit worden meegenomen. </LI>'
        WHERE ("public"."Indicator"."Id" = 4)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='<b>Intern personeel:</b><br> Voor ‘eigen’ personeel worden de geschatte en gerealiseerde uitgaven gerapporteerd op basis van het in het (bijgewerkte) projectplan (of vergelijkbaar) begrote en geschatte aantal dagen.<br> <b>Extern personeel:</b><br> Inhuur van externe personele capaciteit van externe bedrijven ten behoeve van ICT-taken.<br> <b>Overig materieel:</b><br> Dit is een samenvoeging van wat voorheen hardware, standaardsoftware en dataverbindingen was. Deze kunnen opgeteld worden.'
        WHERE ("public"."Indicator"."Id" = 62)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='De belangrijkste externe marktpartijen en hun rol in de ICT-activiteit worden hier gemeld. <br> Niet op de lijst voorkomende marktpartijen kunnen via functioneel beheer worden toegevoegd aan de lijst.'
        WHERE ("public"."Indicator"."Id" = 52)
        ;
        UPDATE "public"."Indicator"
        SET "AntwoordTypeId"='4',"Toelichting"='Welke baat draagt deze ICT-activiteit het meeste aan bij? <br> Let op: vink minimaal één, maximaal drie baten aan.<br><br>Bij twijfel kan contact opgenomen worden met CIO Rijk.'
        WHERE ("public"."Indicator"."Id" = 55)
        ;

        UPDATE "public"."Indicator"
        SET "Index"="Index" + 1
        WHERE ("public"."Indicator"."IndicatorLijstId" = '9bca9116-23a3-43d3-898e-9396a0f82086')
        ;
        INSERT INTO "public"."Indicator" ("Titel", "AntwoordTypeId", "Vereist", "Index", "VerwijderDatum", "IndicatorLijstId", "Toelichting", "AanmaakDatum", "IsLockable") VALUES ('Kwaliteitstoets','5','false','0','0001-01-01 00:00:00','9bca9116-23a3-43d3-898e-9396a0f82086','De CIO maakt in de rapportage melding, zonder de uitkomsten, van een lijst van alle tot dan toe op de ICT-activiteit uitgevoerde kwaliteitstoetsen. <br><br>  Staat je toets niet in het keuzemenu? Dan hoef je hem niet in te vullen. Je hoeft bijvoorbeeld het CIO-oordeel niet in te vullen.','2023-03-29','false');
        ;
        UPDATE "public"."Indicator"
        SET "Index"="Index" + 1
        WHERE ("public"."Indicator"."IndicatorLijstId" = '5ebe3b64-21d0-4657-b8bc-531565c33a1e')
        ;
        INSERT INTO "public"."Indicator" ("Titel", "AntwoordTypeId", "Vereist", "Index", "VerwijderDatum", "IndicatorLijstId", "Toelichting", "AanmaakDatum", "IsLockable") VALUES ('Tweede Kamerstuk','5','false','0','0001-01-01 00:00:00','5ebe3b64-21d0-4657-b8bc-531565c33a1e','De tijdens de ICT-activiteit verstuurde specifieke brieven aan de Tweede Kamer worden hier opgenomen, wanneer ze betrekking hebben op de ICT-component van de ICT-activiteit.<br><br>BIT-adviezen (plus de eventuele bestuurlijke reactie daarop) worden hier ook door het departement als Kamerstuk toegevoegd.','2023-03-29','false');
        ;
        UPDATE "public"."Indicator"
        SET "Index"="Index" + 1
        WHERE ("public"."Indicator"."IndicatorLijstId" = 'a424c56c-e3e0-451a-bd0c-4f1c2d2108f3')
        ;
        INSERT INTO "public"."Indicator" ("Titel", "AntwoordTypeId", "Vereist", "Index", "VerwijderDatum", "IndicatorLijstId", "Toelichting", "AanmaakDatum", "IsLockable") VALUES ('Doorlooptijd en Kosten','5','false','0','0001-01-01 00:00:00','a424c56c-e3e0-451a-bd0c-4f1c2d2108f3','De ICT-activiteit rapporteert over de meerjarige kosten waar door de projectleider invloed op kan worden uitgeoefend, zoals gespecificeerd in het (geüpdatet) projectplan (of vergelijkbaar, inclusief de businesscase). De kosten worden niet uitgesplitst in hoeveel er per jaar verwacht wordt uit te geven; alleen het totale uit te geven bedrag over de hele verwachte looptijd van de ICT-activiteit wordt vermeld. <br><br>Het kan voorkomen dat de initiële kostenschatting bij de start van de ICT-activiteit nog niet volledig bekend is. Deze kostenschatting is verplicht in te voeren bij de start van de ICT-activiteit en is daarna niet zelfstandig meer aan te passen. Het is mogelijk om deze initiële kostenschatting aan te passen, na contact met CIO Rijk. De reden van de wijziging wordt altijd tekstueel toegelicht op het Rijks ICT-dashboard.','2023-03-29','false');
        ;

        INSERT INTO "public"."AntwoordOptie" ("Waarde", "IndicatorId", "Index") VALUES ('Vakmanschap','55','6');
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"='Continuïteit van ICT'
        WHERE ("public"."AntwoordOptie"."Id" = 585)
        ;

        UPDATE public."Project" SET "OrganisatieId" = NULL;
        UPDATE public."Project" SET "OrganisatieId" = neworganisatieid
        FROM
        (
        SELECT
            "ProjectId",
            max(neworganisatieid) as neworganisatieid,
            max(projectnaam) as projectnaam
            FROM
            (
                SELECT
                    pv_1."Id" AS "ProjectVersieId",
                    project."Naam" as  projectnaam,
                    a."Waarde",
                    CASE
                        WHEN a."Waarde" = 'Belastingdienst / IV-Accent'  THEN 2
                        WHEN a."Waarde" = 'Belastingdienst-CAP'  THEN 2
                        WHEN a."Waarde" = 'Belastingdienst, IV-organisatie'  THEN 2
                        WHEN a."Waarde" = 'Belastingdienst/Centrum Facilitaire Dienstverlening'  THEN 2
                        WHEN a."Waarde" = 'Belastingdienst Douane Nederland'  THEN 15
                        WHEN a."Waarde" = 'Centraal Bureau Rijvaardigheidsbewijzen'  THEN 4
                        WHEN a."Waarde" = 'Centraal Justitieel Incassobureau'  THEN 6
                        WHEN a."Waarde" = 'Immigratie- en Naturalisatiedienst'  THEN 17
                        WHEN a."Waarde" = 'Dienst Justis'  THEN 20
                        WHEN a."Waarde" = 'Kamer van Koophandel'  THEN 22
                        WHEN a."Waarde" = 'Koninklijke Bibliotheek'  THEN 25
                        WHEN a."Waarde" = 'Luchtverkeersleiding Nederland'  THEN 29
                        WHEN a."Waarde" = 'Nationaal Coordinator Groningen'  THEN 30
                        WHEN a."Waarde" = 'Openbaar Ministerie'  THEN 33
                        WHEN a."Waarde" = 'Raad voor de Rechtspraak'  THEN 35
                        WHEN a."Waarde" = 'Rijksdienst voor Identiteitsgevens'  THEN 37
                        WHEN a."Waarde" = 'Rijksdienst voor Identiteitsgegevens'  THEN 37
                        WHEN a."Waarde" = 'Rijksvastgoedbedrijf - RVB'  THEN 39
                        WHEN a."Waarde" = 'Sociale Verzekeringsbank'  THEN 42
                        WHEN a."Waarde" = 'Sociale Verzekeringsbank SVB'  THEN 42
                        WHEN a."Waarde" = 'Uitvoeringsinstituut Werknemersvezekeringen'  THEN 43
                        WHEN a."Waarde" = 'Uitvoeringsinstituut Werknemersverzekeringen'  THEN 43
                        WHEN a."Waarde" = 'Uitvoeringsinstituut Werknemers Verzekeringen'  THEN 43
                        WHEN a."Waarde" = 'Uitvoeringinstituut Werknemersverzekeringen UWV'  THEN 43
                        WHEN a."Waarde" = 'CAK'  THEN 3
                        WHEN a."Waarde" = 'CIZ'  THEN 7
                        WHEN a."Waarde" = 'CJIB'  THEN 6
                        WHEN a."Waarde" = 'DICTU'  THEN 8
                        WHEN a."Waarde" = 'DGVBR/SSC-ICT'  THEN 41
                        WHEN a."Waarde" = 'DJI'  THEN 9
                        WHEN a."Waarde" = 'Dienst Uitvoering Subsidies'  THEN 12
                        WHEN a."Waarde" = 'Het Kadaster'  THEN 21
                        WHEN a."Waarde" = 'IND'  THEN 17
                        WHEN a."Waarde" = 'KNMI'  THEN 24
                        WHEN a."Waarde" = 'LVNL'  THEN 29
                        WHEN a."Waarde" = 'NVWA'  THEN 32
                        WHEN a."Waarde" = 'RDW'  THEN 13
                        WHEN a."Waarde" = 'RVO'  THEN 38
                        WHEN a."Waarde" = 'RVO.nl'  THEN 38
                        WHEN a."Waarde" = 'RvIG'  THEN 37
                        WHEN a."Waarde" = 'SVB'  THEN 42
                        WHEN a."Waarde" = 'UWV'  THEN 43
                        WHEN a."Waarde" = 'Agentschap Telecom'  THEN 1
                        WHEN a."Waarde" = 'Belastingdienst'  THEN 2
                        WHEN a."Waarde" = 'Centraal Administratie Kantoor (CAK)'  THEN 3
                        WHEN a."Waarde" = 'Centraal Bureau Rijvaardigheidsbewijzen (CBR)'  THEN 4
                        WHEN a."Waarde" = 'Centraal Bureau voor de Statistiek (CBS)'  THEN 5
                        WHEN a."Waarde" = 'Centraal Justitieel Incassobureau (CJIB)'  THEN 6
                        WHEN a."Waarde" = 'Centrum indicatiestelling zorg (CIZ)'  THEN 7
                        WHEN a."Waarde" = 'Dienst ICT Uitvoering (DICTU)'  THEN 8
                        WHEN a."Waarde" = 'Dienst Justitiële Inrichtingen'  THEN 9
                        WHEN a."Waarde" = 'Dienst Terugkeer en Vertrek'  THEN 10
                        WHEN a."Waarde" = 'Dienst Uitvoering Onderwijs (DUO)'  THEN 11
                        WHEN a."Waarde" = 'Dienst Uitvoering Subsidies aan Instellingen (DUS-I)'  THEN 12
                        WHEN a."Waarde" = 'Dienst Wegverkeer (RDW)'  THEN 13
                        WHEN a."Waarde" = 'Directie Consulaire zaken en Visumbeleid (DCV)'  THEN 14
                        WHEN a."Waarde" = 'Douane'  THEN 15
                        WHEN a."Waarde" = 'Generale Thesaurie'  THEN 16
                        WHEN a."Waarde" = 'Immigratie- en Naturalisatiedienst (IND)'  THEN 17
                        WHEN a."Waarde" = 'Inspectie Gezondheidszorg en Jeugd (IGJ)'  THEN 18
                        WHEN a."Waarde" = 'Inspectie Leefomgeving en Transport'  THEN 19
                        WHEN a."Waarde" = 'Justis'  THEN 20
                        WHEN a."Waarde" = 'Kadaster'  THEN 21
                        WHEN a."Waarde" = 'Kamer van Koophandel (KvK)'  THEN 22
                        WHEN a."Waarde" = 'Kiesraad'  THEN 23
                        WHEN a."Waarde" = 'Koninklijk Nederlands Meteorologisch Instituut (KNMI)'  THEN 24
                        WHEN a."Waarde" = 'Koninklijke Bibliotheek (KB)'  THEN 25
                        WHEN a."Waarde" = 'Koninklijke Marechaussee'  THEN 26
                        WHEN a."Waarde" = 'Kustwacht'  THEN 27
                        WHEN a."Waarde" = 'Logius'  THEN 28
                        WHEN a."Waarde" = 'Luchtverkeersleiding Nederland (LVNL)'  THEN 29
                        WHEN a."Waarde" = 'Nationaal Coördinator Groningen'  THEN 30
                        WHEN a."Waarde" = 'Nederlands Forensisch Instituut'  THEN 31
                        WHEN a."Waarde" = 'Nederlandse Voedsel-en Warenautoriteit (NVWA)'  THEN 32
                        WHEN a."Waarde" = 'Openbaar Ministerie (OM)'  THEN 33
                        WHEN a."Waarde" = 'Organisatie en Personeel Rijk (P-Direkt)'  THEN 34
                        WHEN a."Waarde" = 'Raad voor de rechtspraak'  THEN 35
                        WHEN a."Waarde" = 'Rijksdienst voor het Cultureel Erfgoed'  THEN 36
                        WHEN a."Waarde" = 'Rijksdienst voor Identiteitsgegevens (RvIG)'  THEN 37
                        WHEN a."Waarde" = 'Rijksdienst voor Ondernemend Nederland (RVO)'  THEN 38
                        WHEN a."Waarde" = 'Rijksvastgoedbedrijf (RVB)'  THEN 39
                        WHEN a."Waarde" = 'Rijkswaterstaat'  THEN 40
                        WHEN a."Waarde" = 'Shared Service Center ICT (SSC-ICT)'  THEN 41
                        WHEN a."Waarde" = 'Sociale Verzekeringsbank (SVB)'  THEN 42
                        WHEN a."Waarde" = 'Uitvoeringsinstituut Werknemersverzekeringen (UWV)'  THEN 43
                        WHEN a."Waarde" = 'Directoraat Generaal Belastingdienst' THEN 2
                        WHEN a."Waarde" = 'P-Direkt'  THEN 34
                        ELSE NULL
                    END as neworganisatieid,
                    pv_1."ProjectId",
                    f."Id" AS "FormulierId"
                FROM (((((("ProjectVersie" pv_1
                        JOIN "FormulierProjectVersie" fpv ON ((fpv."ProjectVersiesId" = pv_1."Id")))
                        JOIN "Project" project ON ((pv_1."ProjectId" = project."Id")))
                        JOIN "Formulier" f ON ((f."Id" = fpv."FormulierenId")))
                        JOIN "Antwoord" a ON ((a."FormulierId" = f."Id")))
                        JOIN "Indicator" i ON ((i."Id" = a."IndicatorId")))
                        )
                WHERE "IndicatorId" = 24
                AND project."Nummer" > 0
            ) as modifiedview
        group by "ProjectId"
        ) as buiten
        WHERE "Project"."Id" = buiten."ProjectId"
        ;
        
    """
    op.execute(upgrade_query)
    op.execute("SET search_path TO public")


def downgrade() -> None:
    pass
