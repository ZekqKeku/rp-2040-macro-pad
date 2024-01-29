Dostęone metody:
key<> - Wciska klawisz przez chwilę, jeśli poprzedza go Ctrl, Alt lub Shift nie zastaną nacisnięte do następnego klawisza. Pozostawienie key<ctrl> zostanie pominięte.
 
press<> - Funckja wciska i przytrzymuje wybrany klawisz do chwili zwolnienia go 

realese<> - Funckja zwalnia wciskany klawisz, zalecane dla kązdego klawisza na którym zostałła użyta metoda press<>

Jeśli klawisz Ctrl, Shift lub Alt nie został sprecyzowany domyślnie zostaje użyty ten lewy

text<> - Funkcja wysyła automatycznie tekst w oparciu o metodę key<> z automatycznym użyciem shifta dla dużych liter i rozpoznawaniem polskich znaków diakretycznych

media<> - Funckja pozwalająca na sterowanie między innymi muzykę, głośnąścia komputera czy jasnąścią ekranu


Przykłady użycia:
By użyć więcej metod na jeden bind konieczne jest użycie łącznika + bez dodatkowych spacji

key<ctrl>+key<a>+key<ctrl>+key<c>+key<DOWN_ARROW> - Ctrl+A Ctrl+C (Strzałka w dół)
key<ctrl>+key<v> - Ctrl+V
media<volup> - Podłośnienie dźwieku systemowego
media<volup:10> - Podłośnienie dźwieku systemowego (z krokiem 10)
media<play> - Puszczenie zapałzowanej muzyki lub filmu
press<right_ctrl>+key<A>+realese<right_ctrl> - Ctrl+A

Dokładny opis metod:
key<> - Przyjmuje znaczną większość klawiszy które można 
uzyskać na klawiaturze bez wciskania shift'a etc.
Obsługuje klaiwsze F1 - F24, 
liczby w sposób dosłowny (1 zamiast one)
numpada (num1 zamiast numpad_one)

press<> oraz realese<> - Przyjmują te same paarametry co key<>

media<>
W rzeczywistości użycie play i pause daje ten sam efekt
działają przemiennie, jesli coś gra to play zadziała jak pause 
Play - Sterowanie muzyką
Pause - Sterowanie muzyką
VolUp - Zwiększanie głośności systemu
VolDown - Zmniejszanie głośności systemu
Skip - Przejście do następnego utworu
BackSkip - Powrót do poprzedniego utworu
Stop - Zatrzymanie odtwarzania
Eject - Wyrzucenie płyty
Fast_Forward - Szybkie przewijanie do przodu
Rewind - Szybkie przewijanie do tyłu
Mute - Wyciszenie dźwięku
BrightnessUp - Zwiększanie jasności
BrightnessDown - Zmniejszanie jasności

Metody VolUp, VolDown, BrightnessUp, BrightnessDown przyjmują kroki z zakresu 1-100
np <BrightnessUp:20>, przy przekroczeniu wartości zostaje ona ograniczona do tego zakresu
przy podaniu 234 zostanie zinterpretowana jako 100.


Do dodania
mause<> - strerowanie myszką
wait<> - opóźnienie w sekundach
