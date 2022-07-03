# Predefinisani projekat NTP

Predefinisan projekat - rešavanje N-dimenzionalnih problema uz pomoć PSO algoritma

#### Student - Filip Živanac SW-66-2018

### Opis algoritma

PSO(Particle swarm optimization) jer algoritam za optimizaciju funkcija. Koristi se za rešavanje komleksnih optimizacionih problema zbog svoje robusnoti.
PSO  algoritam je zasnovan na imitaciji ponašanja
životinjskih skupina, odnosno, jedinki u tim skupinama
(jata ptica i riba, rojevi insekata itd.). PSO je
evolutivna, populaciona tehnika. Skup tačaka
(potencijalnih rešenja) posmatramo kao čestice, čije
promene položaja posmatramo kao pomeranje pozicije
usled pretrage.
Algoritmu se prosleđuje:
<ol>
<li>broj dimenzija optimizacionog problema,</li>
<li>tolerancija kriterijuma zaustavljanja,</li>
<li>funkcija za evaluaciju,</li>
<li>broj čestica,</li>
<li>maksimalni broj iteracija.</li>
</ol>
Kao rezultat algoritam vraća:
<ol>
<li>poziciju optimuma,</li>
<li>vrednost funkcije u optimumu,</li>
<li>vreme izvršavanja.</li>
</ol>
Koraci navedenog algoritma su inicijalizacija
čestica, računanje njihovih novih pozicija, kao i
kriterijum zaustavljanja

Svaka čestica pamti:
<ol>
<li>svoju tekuću poziciju (potencijalno rešenje),</li>
<li>najbolju poziciju ikad dostignutu (najbližu</li>
rešenju) i
<li>tekuću brzinu.</li>
 </ol>
Roj, kao celina, pamti svoju najbolju poziciju ikada
postignutu.
Iterativno, za svaku česticu k računa se njena brzina,
nakon čega dolazi do promene pozicije prema sledećim
formulama:

𝑣[𝑘] = 𝑤[𝑘] ⋅ 𝑣[𝑘 − 1] + 𝑐𝑝[𝑘] ⋅ 𝑟𝑝[𝑘] ⋅ (𝑝[𝑘] −𝑥[𝑘])+
𝑐𝑔[𝑘] ⋅ 𝑟𝑔[𝑘] ⋅ (𝑔[𝑘] −𝑥[𝑘])
𝑥 𝑘 + 1 = 𝑥 𝑘 + 𝑣 𝑘 

### Rešenje

Kao optimizacioni problem koji se rešava koristiće se Aklijeva funkcija.
U izlanom fajlu će se prikazivati globalni optimum i njegova lokacija nakon svake iteracije.
Sekvencijalno i paralelno izvršavanje algoritma biće implementiranu u jeziku Python.
