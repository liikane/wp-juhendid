# Turvaline GitHub Copiloti ja WordPressi töövoog

See juhend kirjeldab, kuidas korraldada WordPressi agentuuritööd GitHub Copiloti pilveagendiga nii, et muudatused oleksid piiratud, kontrollitavad ja enne paigaldamist inimese poolt üle vaadatud. See täiendab [WordPressi agentioskuste ülevaadet](wordpress-agent-skills.md) ja [lihtsat töövoogu](lihtne_toovoog.md); see ei asenda projekti enda juurutus- ega varundusjuhiseid.

## Töövoog: issue’st võimaliku tootmispaigalduseni

1. **Kirjuta issue.** Kirjelda soovitud tulemust, mõjutatud komponente, vastuvõtukriteeriume ja seda, millises keskkonnas tööd kontrollida. Ütle selgelt, kas ülesanne on ainult lugemiseks või lubab failide muutmist. Ära lisa issue’sse päris kasutajaandmeid, ligipääsuandmeid ega saladusi.
2. **Anna pilveagendile piiritletud ülesanne.** Palu muuta ainult vajalikke faile, käivitada sobivad kontrollid ja jätta kõik andmeid või päriskeskkonda muutvad tegevused tegemata. Agent töötab GitHubi koodikoopiaga ega näe automaatselt sinu arendaja arvutit, WordPressi andmebaasi, veebihosti ega privaatseid teenuseid.
3. **Tööta eraldi harus.** Hoia iga issue muudatus omaette harus. Kontrolli diffi enne commit’i; ära pane samasse muudatusse sõltumatuid ülesandeid ega saladusi.
4. **Ava pull request.** Lisa PR-i kokkuvõte, tehtud muudatused, kontrollide tulemused ja teadaolevad piirangud. Vaata muudatused ise üle ning lahenda kommentaarid. Automatiseeritud kontrolli läbimine ei tähenda, et muudatus sobib kohe tootmisse.
5. **Käivita kontrollid.** Kasuta projektis olevaid teste ja CI-kontrolle ning kontrolli vähemalt diffi. WordPressi koodi puhul lisa vajaduse korral PHP süntaksikontroll ja read-only WP-CLI/API kontrollid (näited allpool). Need ei asenda funktsionaalset testimist.
6. **Varunda ja kontrolli staging’us.** Enne andmeid, faile, pluginaid või seadeid muutvat paigaldust tee taastatav andmebaasi- ja failivarukoopia. Proovi muudatust esmalt staging-keskkonnas, kontrolli tulemust ja vajadusel taasta varukoopia. Kasuta võimalusel sünteetilisi või anonüümitud andmeid.
7. **Küsi inimese kinnitus.** Enne staging’u või tootmise muutmist peab vastutav inimene diffi, kontrollid, varunduse ja tagasipööramise plaani üle vaatama ning tegevuse selgesõnaliselt heaks kiitma. Tootmisse paigaldamine on eraldi otsus pärast staging’u kontrolli; ära käsitle PR-i ühendamist automaatse tootmisloana.

## Mida pilveagent saab ja ei saa teha

Pilveagent saab aidata hoidlas olevat koodi, konfiguratsiooni, dokumentatsiooni ja teste muuta ning kasutada talle keskkonnas antud tööriistu. Ta ei saa ainult hoidla põhjal kindlaks teha, mis toimub päris WordPressi saidil, ega kontrollida andmebaasi, makseid, serveri seadeid või kasutajakogemust.

Päris saidiga seotud kontroll vajab selleks eraldi seadistatud ja volitatud keskkonda. Kasuta ligipääsu vastavalt ülesandele:

- **WP-CLI** sobib kohaliku arenduse või staging’u WordPressi oleku kontrollimiseks ja haldamiseks. Käivita käsud WordPressi paigalduse kontekstis. Pilveagendi terminali käsk ei saa eeldada ligipääsu sinu arvuti või hosti WordPressile.
- **REST API** sobib HTTP kaudu WordPressi avaliku või õigustega kaitstud liidese kontrollimiseks. Kasuta GET-päringuid lugemiseks; kirjutavad päringud nõuavad õigusi ja eraldi kinnitust.
- **MCP** võib vahendada WordPressi või muid tööriistu, kuid selle võimekus sõltub ühendatud serverist ja antud õigustest. Sea vaikimisi võimalusel ainult lugemisõigus ning luba kirjutamine üksnes konkreetse, inimese kinnitatud ülesande jaoks.

Ära ühenda agenti päris serveri, andmebaasi ega kirjutamisõigusega MCP-tööriistaga lihtsalt mugavuse pärast. Kui töö nõuab sellist ligipääsu, kasuta eraldi volitatud keskkonda, piira õigusi ja kooskõlasta tegevus enne ühendamist.

## Ohutud kontrollinäited

Allolevad näited on mõeldud kohaliku arenduse või staging’u jaoks. Need ei muuda WordPressi sisu ega seadeid. Ära käivita neid keskkonnas, millele sul puudub luba.

```sh
git diff --check
php -l index.php
wp plugin list --format=table
wp core version
```

`git diff --check` leiab diffist muu hulgas tühikuvigu. `php -l` kontrollib ainult nimetatud PHP-faili süntaksit. Kaks WP-CLI käsku loevad paigalduse ja pluginate infot ega tõesta, et sait töötab tervikuna.

REST API avaliku lugemispäringu näide kasutab spetsiaalselt näidiseks mõeldud domeeni `example.test`:

```sh
curl --fail --silent --show-error \
  https://example.test/wp-json/wp/v2/
```

See on GET-päring; ära asenda näidisdomeeni päris saidiga ilma loata. Autentimisega päringute puhul ära kirjuta kasutajanime, parooli, tokenit ega küpsist käsureale ega dokumentatsiooni.

## Luba, saladused ja muutvad toimingud

- **Vaikeseade on read-only.** Koodi ülevaatus, GET-päringud ja siin toodud loetlevad WP-CLI käsud on sobivad alguseks. Sisu, kasutajate, tellimuste, maksete, pluginaseadete, failide või andmebaasi muutmine pole vaikimisi lubatud.
- **Päris keskkond ja pärisandmed vajavad eraldi luba.** Küsi enne serveriühendust või päris kasutajaandmete kasutamist selgesõnaline, konkreetse ülesande ja keskkonnaga piiratud kinnitus. Maksete või rahaliste toimingute jaoks on alati vaja eraldi luba ja asjakohast inimkontrolli.
- **Hoia saladused väljaspool prompti ja hoidlat.** Ära lisa võtmeid, paroole, tokeneid, privaatseid URL-e ega varukoopiaid issue’sse, prompti, logisse või commit’i. Kasuta organisatsiooni heakskiidetud saladuste hoidlat ja minimaalse õigusega, piiratud kehtivusajaga ligipääsu. GitHub Actionsi saladusi kasuta ainult usaldatud töövoos ja vajaliku skoobiga; ära väljasta neid logisse. Kui saladus satub valesse kohta, eemalda see ja vaheta saladus välja.
- **Kasuta dry-run’i, kui see on saadaval.** Kontrolli konkreetse käsu dokumentatsioonist, et `--dry-run` on toetatud ja mida see täpselt teeb. Vaata kavandatavad muudatused üle; dry-run ei asenda varukoopiat ega inimese kinnitust. Ära kasuta muutvat käsku enne PR-i kontrolli ja selgesõnalist luba.
- **Kinnita kõik kirjutavad tegevused.** Enne REST API või MCP kirjutamistoimingut vaata üle sihtkeskkond, muutmise ulatus ja taastamisplaan ning küsi inimese kinnitus. Kui ulatus või mõju pole selge, peatu ja küsi täpsustust.

## Kulude jälgimine

Pilveagendi ega GitHub Actionsi kasutamist ei tohi eeldada tasuta või nullkuluga. Jälgi Copiloti kasutus- ja krediiditeavet ning Actionsi jooksutusaega ja arveldust konto või organisatsiooni seadetes. Arvesta, et korduvad töövood, pikad jooksutused ja suuremad kontrollid võivad kulusid kasvatada; järgi organisatsiooni limiite ja teavitusreegleid.
