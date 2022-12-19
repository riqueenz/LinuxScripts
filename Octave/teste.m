clear # zera as variáveis
clc # apaga a tela

pkg load symbolic # carrega modulo simbólico

# Declarando variaveis simbolicas
syms A D pi S Vdu rv z Vd V1 V2

disp("Inicio da resolução")

disp("\nDados do problema:")
Vd = 5.2 # litros
D = 10.2  # cm
z = 6 # cilindros
V2 = 54.2 # cm3

Vd = Vd * 1000 # cm3
# Passando tudo para simbolico para evitar mensagem chata
# E melhorar precisão do cálculo
Vd = sym (Vd, 'r');
D = sym (D, 'r');
z = sym (z, 'r');
V2 = sym (V2, 'r');

disp("Vdu = Vd / z")
Vdu = Vd / z
disp("Volume de 1 cilindro - Vdu em cm3:")
double(Vdu)

disp("\nVdu = A * S:")
disp("Então S = Vdu / A:")
A = (pi * D * D) / 4;
S = Vdu / A;
disp("Curso S em cm:")
double(S)

rv = (Vdu + V2) / V2;
disp("\ntaxa de compressão rv")
double(rv)

disp("\nrv = V1 / V2:")
disp("Então V1 = rv * V2:")
V1 = rv * V2;
double(V1)
