import os
import tools.jellyfish as jf

# threshold for jaro winkler distance
jw_threshold = 0.8

# Return 1 if sentences are the same and 0 if they are completely different
def sentence_distance( str1, str2, jw_threshold ):
    distance = 0
    count = 0
    last_matches = 0
    list_w1 = str1.split(' ')
    list_w2 = str2.split(' ')
    for w1 in list_w1:
        word_dist = map( lambda w2 : jf.jaro_winkler(w1.lower(),w2.lower()), list_w2)        
        val = max(word_dist)
        length = len(w1)
        if last_matches == 3:
            length *= 2
        if last_matches == 2:
            length *= 1.5
        if last_matches == 1:
            length *= 1.2
        if val > jw_threshold:
            distance += val * length
            count += length
            last_matches = min(3,last_matches+1)
        else :
            count += length / 2.0
            last_matches = max(0,last_matches-1)
    distance /= count
    return distance

# Frase original do arquivo srt
str1 = u"Olhe, eu sei que alguma garota vai ser sortuda... ...de se tornar a senhora Barry Finkel."

# parte do audio correta, traduzido
str2 = u"Eu sei que algumas garotas vai para ser uma sorte incrivel para se tornar a Sra. Barry Finkel"
# parte do audio erradas
str3 = u"Falou com Barry? Nao consigo parar de sorrir. Percebi. Parece que voce dormiu com um cabide na boca."
str4 = u"Voce se casou quando tinha, sei la, oito? Bem vindo de volta ao mundo! Pegue uma colher!"

print sentence_distance(str1, str2, jw_threshold)
print sentence_distance(str1, str3, jw_threshold)
print sentence_distance(str1, str4, jw_threshold)

print ""

# extraido do audio 
sen1 = [u"Nao ha nada para contar", 
        u"Mamae que vai sair com um cara que tem que haver algo de errado com eles", 
        u"Centro de mesa com o que ele fala, porque nao quero que ela para passar o que passei com Carl",
        u"Relaxem. Nao e nem um encontro."]
        
# extraido das legendas
sen2 = [u"Nao ha nada para contar! Ele e so um cara do trabalho!",
        u"Voce esta saindo com esse cara!",
        u"Deve ter alguma coisa errada com ele!",
        u"Tudo bem, Joey, vai com calma.",
        u"Entao, ele e corcunda? Corcunda e careca?",
        u"Espera ai, ele come giz?",
        u"e que eu nao quero que ela passe pela mesma coisa que eu passei com o Carl!",
        u"Isto nao e nem um dia",
        u"bom apenas duas pessoas saindo para jantar em"]

# separar legendas, quebrando em novas linhas
for ponctuation in ['!','.','?',';'] :
    sen2 = map( lambda str : str.split(ponctuation), sen2 )
    sen2 = reduce( lambda a, b: a+b, sen2, [])
    sen2 = filter( lambda a: len(a) > 0, sen2)

        
#concatenando legendas
sen3 = map(lambda i : sen2[i] + " " + sen2[i+1], range(0,len(sen2)-1))
sen2 += sen3
        
for w1 in sen1:
    mapa = map( lambda w2 : sentence_distance(w1,w2, jw_threshold), sen2)
    idx = [i for i, j in enumerate(mapa) if abs(j - max(mapa)) < 0.05 ]
    print "INDEXES = ", idx, " BEST DISTANCE = ", mapa[idx[0]]
    print "========> ", w1
    print "MATCH ==> ", sen2[idx[0]]    
    for i in range(1,len(idx)):
        print "TALVEZ => ", sen2[idx[i]]
    print ""
    
    

