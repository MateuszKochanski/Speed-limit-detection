import cv2
import numpy as np

#Wczytanie obrazu w BGR
img = cv2.imread('zdjeciaWMA/zdj3.jpg')

#cv2.waitKey(0)
#Obraz w odcieniach szarości
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


#obraz w przestrzeni barw HSV
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#maska daje 255 jak kolor w HSV jest w danym zakresie, w przeciwnym wypadku daje 0
maska1 = cv2.inRange(imgHSV, (0,  20, 20), (10, 255, 255))
maska2 = cv2.inRange(imgHSV, (165, 20, 20), (180, 255, 255))
maska = cv2.bitwise_or(maska1, maska2)
#szuka konturów maski
(kr, sth) = cv2.findContours(maska, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#lista przechowywująca kontury o okrągłym kształcie
kolka = []
#iteruję po wszystkich konturach
for i in kr:
    #jeśli jest odpowiednio duży
    if cv2.contourArea(i) > 500:
        #Opisuje na konturze okrąg
        (x, y), r = cv2.minEnclosingCircle(i)
        center = (int(x), int(y))
        radius = int(r)
        #Sprawdzam czy powierzchnia konturu mieści się w odowiednich granicach
        if np.power(radius - 10, 2) * np.pi < cv2.contourArea(i):
            kolka.append(i)

#indeks największego okręgu
idx = 0
#szukam najwięszky okrąg
for i in range(len(kolka)):
    if cv2.contourArea(kolka[i]) > cv2.contourArea(kolka[idx]):
        idx = i
najwiekszeKolko = kolka[idx]
mojeKolko = najwiekszeKolko
kolka.pop(idx)
#sprawdzam czy w największym okręgu jest jakiś okrąg
for i in kolka:
    (x1, y1), r1 = cv2.minEnclosingCircle(najwiekszeKolko)
    (x2, y2), r2 = cv2.minEnclosingCircle(i)
    a = np.sqrt(np.power(x1 - x2, 2) + np.power(y1 - y2, 2))
    if a < 50:
        mojeKolko = i
#ostatecznie otrzymałem kontur wewnętrzny znaku

#Rysuje otrzymany kontur i wyświetlam
img2 = img.copy()
cv2.drawContours(img2, [mojeKolko], -1, (0, 255, 0), 2)
cv2.imshow("Obraz", img2)

#tworzę maskę w o wymiarach obrazu zapisaną zerami
maska3 = np.zeros(img.shape[:2], np.uint8)
#na masce rysuję wypełniony kontur
cv2.drawContours(maska3, [mojeKolko], -1, 255, cv2.FILLED)
#wykonuję erozję żeby odrobinę go poprawić
maska3 = cv2.erode(maska3, np.ones((3, 3), np.uint8))
#kopiuję obraz w odcieniach szarości
img_copy = gray.copy()
#gdy maska różna od 255 to wpisuje 255
img_copy[maska3 != 255] = 255
#wykonanie progowania
a, img_thresh = cv2.threshold(img_copy, 150, 255, 0)
#Dylatacja a potem erozja aby pozbyć się zakłóceń
img_dil = cv2.dilate(img_thresh, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
img_ero = cv2.erode(img_dil,  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
#Obliczam współrzędne do wycięcia 1 cyfry
(x3, y3), r3 = cv2.minEnclosingCircle(mojeKolko)
X = int(x3) - int(r3)
Y = int(y3) - int(r3)
W = int(r3)
H = 2 * int(r3)
#wycinam pierwszą cyfrę
pierwszaCyfra = img_ero[Y:Y+H, X:X+W]
#skaluję pierwszą cyfrę
resized = cv2.resize(pierwszaCyfra, (67, 134), interpolation=cv2.INTER_LINEAR)
#tworzę liste grafik cyfr
cyfry = []
#wczytuje grafiki do listy
cyfry.append(cv2.imread("zdjeciaWMA/cyfry/l0.png", cv2.IMREAD_GRAYSCALE))
cyfry.append(cv2.imread("zdjeciaWMA/cyfry/l1.png", cv2.IMREAD_GRAYSCALE))
cyfry.append(cv2.imread("zdjeciaWMA/cyfry/l2.png", cv2.IMREAD_GRAYSCALE))
cyfry.append(cv2.imread("zdjeciaWMA/cyfry/l3.png", cv2.IMREAD_GRAYSCALE))
cyfry.append(cv2.imread("zdjeciaWMA/cyfry/l4.png", cv2.IMREAD_GRAYSCALE))
cyfry.append(cv2.imread("zdjeciaWMA/cyfry/l5.png", cv2.IMREAD_GRAYSCALE))
cyfry.append(cv2.imread("zdjeciaWMA/cyfry/l6.png", cv2.IMREAD_GRAYSCALE))
cyfry.append(cv2.imread("zdjeciaWMA/cyfry/l7.png", cv2.IMREAD_GRAYSCALE))
cyfry.append(cv2.imread("zdjeciaWMA/cyfry/l8.png", cv2.IMREAD_GRAYSCALE))
cyfry.append(cv2.imread("zdjeciaWMA/cyfry/l9.png", cv2.IMREAD_GRAYSCALE))
#tworze listę dopasowania każdej cyfry
porownanie = []
#porównuje obraz pierwszej cyfry z każdym z obrazów cyfr
for c in cyfry:
    res = cv2.matchTemplate(resized, c, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    porownanie.append(max_val)
#Sprawdzam dla której cyfry otrzymano największa zgodność
cyfra = 0
for i in range(len(porownanie)):
    if porownanie[i] > porownanie[cyfra]:
        cyfra = i
#Liczę położenie drugiej cyfry
X = int(x3)
Y = int(y3) - int(r3)
#wycinam drugą cyfrę
drugaCyfra = img_ero[Y:Y+H, X:X+W]
#skaluję drugą cyfrę
drogaResized = cv2.resize(drugaCyfra, (67, 134), interpolation=cv2.INTER_LINEAR)

#Porównuję obraz drugiej cyfry z obrazem cyfry 0
res = cv2.matchTemplate(drogaResized, cyfry[0], cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
wartoscDlaZera = max_val

#Porównuję obraz drugiej cyfry z obrazem cyfry 5
res = cv2.matchTemplate(drogaResized, cyfry[5], cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
wartoscDlaPieciu = max_val

#liczę wartość ograniczenia prędkości
ograniczenie = cyfra*10
if wartoscDlaPieciu > wartoscDlaZera:
    ograniczenie += 5
#wyświetlam wynik
print("Ograniczenie prędkości do", ograniczenie, "km/h")
#Czekam na wciśnięcie dowolnego przycisku
cv2.waitKey(0)
#Usuwam wszystkie okna
cv2.destroyAllWindows()