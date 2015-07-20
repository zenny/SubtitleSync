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
        
#Transcripting speech segments...
#9 out of 9 successful transcriptions.
trans = [
(0, 2915, u"there's nothing to tell it"),
(2901, 4448, u'just some guy I work with'),
(4526, 8581, u'call mom you are going out with a guy that got to be something wrong with them'),
(8427, 10903, u'I like jelly bean ice'),
(11539, 17311, u'so did you have a hard bump and herpes'),
(17437, 20469, u"just as I don't want her to go through what I went through"),
(20316, 21491, u'Ruth Carl'),
(21430, 29014, u"everybody relax relax this is not even a date it's not it's just two people going out to dinner and not having sex"),
(29047, 30040, u'')]

#Translating subtitles...
#10 out of 10 successful translations.
subs = [
(500, 4600, u"N the h nothing to tell!\nHe's a guy from work!"),
(4800, 7040, u"You're dating this guy!"),
(7200, 9600, u'There must be something wrong with him!'),
(9600, 11680, u'Okay, Joey, take it easy.'),
(12000, 14720, u'Then, he hump?\nHunchback and bald?'),
(16200, 18240, u'Wait, he eat chalk?'),
(18600, 21600, u'I do not want her to go through the same thing I went through with Carl!'),
(21600, 23400, u'All right, guys, relax'),
(23400, 25720, u'Relax.\nN or a date.'),
(25800, 29320, u'S s two people going out to dinner together without having sex.')]

original_subs = [(3000, 3100, u"Nao ha nada para contar! Ele e so um cara do trabalho!"),
        (4000, 4100, u"Voce esta saindo com esse cara!"),
        (4500, 4600, u"Deve ter alguma coisa errada com ele!"),
        (5000, 5100, u"Tudo bem, Joey, vai com calma."),
        (6000, 6100, u"Entao, ele e corcunda? Corcunda e careca?"),
        (7000, 7100, u"Espera ai, ele come giz?"),
        (8000, 8100, u"E que eu nao quero que ela passe pela mesma coisa que eu passei com o Carl!"),
        (9000, 9100, u"Relaxem."),
        (9200, 9300, u"Nao E nem um encontro."),
        (9500, 9600, u"Sao so duas pessoas indo jantar juntas sem fazer sexo.")]
        
print len(original_subs)
print len(subs)
print ""

print mm.match_subs_trans(subs, trans, original_subs)

'''
match = [(0, 2915, u"there's nothing to tell it"), (2901, 4448, u'just some guy I work with'),
(500, 4600, u"N the h nothing to tell!\nHe's a guy from work!"),

(4526, 8581, u'call mom you are going out with a guy that got to be something wrong with them'),
(4800, 7040, u"You're dating this guy!"), (7200, 9600, u'There must be something wrong with him!'),

(8427, 10903, u'I like jelly bean ice'),
(9600, 11680, u'Okay, Joey, take it easy.'),

(11539, 17311, u'so did you have a hard bump and herpes'),
(12000, 14720, u'Then, he hump?\nHunchback and bald?'),

(17437, 20469, u"just as I don't want her to go through what I went through"), (20316, 21491, u'Ruth Carl'),
(16200, 18240, u'Wait, he eat chalk?'), (18600, 21600, u'I do not want her to go through the same thing I went through with Carl!'),

(21430, 29014, u"everybody relax relax this is not even a date it's not it's just two people going out to dinner and not having sex"),
(21600, 23400, u'All right, guys, relax'), (23400, 25720, u'Relax.\nN or a date.'), (25800, 29320, u'S s two people going out to dinner together without having sex.'),

(29047, 30040, u'')]
'''




