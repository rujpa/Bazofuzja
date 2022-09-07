Projekt jest stworzony przez zespół 12 na Programowanie Zespołowe na Uniwersytecie Mikołaja Kopernika

Program uruchamia się po włączeniu MainWindow.pyw
Należy mieć zainstalować:
PyQT5, Psutils, PyMySQL, Pandas, SQLAlchemy, RSA, Crypto Tools, XLWT, LXML, Psycopg2, OpenPyXL, Xlrd
1. Transfer danych
a. system danych relacyjnych na system danych relacyjnych
	Należy wybrać system z listy i zalogować się do bazy albo wczytać bazę z pliku. Potem należy wybrać, które tabele trafią do nowego miejsca. Jeżeli tabela już występuje w nowym miejscu, można wybrać czy chcemy nadpisać rekordy czy dodać jako nowe.
	Następnie wybieramy system danych wyjściowych i otrzymujemy podsumowanie. Na końcu klikamy wykonaj.
b. system danych płaskich na system danych relacyjnych
	Po wybraniu systemu i pliku wejściowego, rozdzielamy i łaczymy kolumny w tabele. Reszta analogicznie
c. system danych relacyjnych na system danych płaskich
	Analogicznie jak w pierwszym, dane w miejscu wyjściowym będą osobnymi plikami.
2. Edycja danych
	Po wybraniu wejścia i wyjścia, można przeprowadzić edycję danych np. usunięcie duplikatów.
3. Edycja relacji
	Można stworzyć nowe relację lub przenieść już istniejące. Aby stworzyć należy wybrać, które kolumny w tabeli są kluczami i z jakimi tabelami można je połączyć.
4. Wykonywanie transferu z linii poleceń.
 Aby móc wykonywać transfer z CLI należy wykonać zwykły transfer i na końcu zapisać do pliku binarnego operacje. Potem możmy wykonać plik binarny z linii poleceń.
