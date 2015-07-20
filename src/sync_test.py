import os
from tools.matching_manager import matching_manager

# Frase original do arquivo srt
str1 = u"Olhe, eu sei que alguma garota vai ser sortuda... ...de se tornar a senhora Barry Finkel."

# parte do audio correta, traduzido
str2 = u"Eu sei que algumas garotas vai para ser uma sorte incrivel para se tornar a Sra. Barry Finkel"
# parte do audio erradas
str3 = u"Falou com Barry? Nao consigo parar de sorrir. Percebi. Parece que voce dormiu com um cabide na boca."
str4 = u"Voce se casou quando tinha, sei la, oito? Bem vindo de volta ao mundo! Pegue uma colher!"

mm = matching_manager()

print mm.sentence_distance(str1, str2)
print mm.sentence_distance(str1, str3)
print mm.sentence_distance(str1, str4)

print ""
        
# extraido das legendas
subs = [(3000, 3100, u"Nao ha nada para contar! Ele e so um cara do trabalho!"),
        (4000, 4100, u"Voce esta saindo com esse cara! Deve ter alguma coisa errada com ele!"),
        (5000, 5100, u"Tudo bem, Joey, vai com calma."),
        (6000, 6100, u"Entao, ele e corcunda? Corcunda e careca?"),
        (7000, 7100, u"Espera ai, ele come giz?"),
        (8000, 8100, u"E que eu nao quero que ela passe pela mesma coisa que eu passei com o Carl!"),
        (9000, 9100, u"Relaxem. Nao E nem um encontro."),
        (9500, 9600, u"Sao so duas pessoas indo jantar juntas sem fazer sexo.")]

# extraido do audio 
trans = [(1000, 1100, u"Nao ha nada para contar"),
        (1500, 1600, u"Mamae que vai sair com um cara que tem que haver algo de errado com eles"), 
        (2000, 2100, u""), #could not transcript
        (2500, 2600, u"Centro de mesa com o que ele fala, porque nao quero que ela para passar o que passei com Carl"),
        (3000, 3100, u"Isto nao e nem um dia"),
        (3500, 3500, u"bom apenas duas pessoas saindo para jantar em")]
    
print mm.match_subs_trans(subs, trans)

