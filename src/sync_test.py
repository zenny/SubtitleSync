import os
import tools.jellyfish as jf

def sentence_distance( str1, str2 ):
    distance = 0
    count = 0
    for w1 in str1.split(' '):        
        word_dist = map( lambda w2 : jf.jaro_winkler(w1,w2), str2.split(' ') )        
        val = max(word_dist)
        if val > 0.6:
            distance += val * len(w1)
            count += len(w1)
        else :
            count += len(w1) / 2
    distance /= count
    return distance

# Frase original do arquivo srt
str1 = u"Olhe, eu sei que alguma garota vai ser sortuda... ...de se tornar a senhora Barry Finkel."

# parte do audio correta, traduzido
str2 = u"Eu sei que algumas garotas vai para ser uma sorte incrivel para se tornar a Sra. Barry Finkel"
# parte do audio erradas
str3 = u"Falou com Barry? Nao consigo parar de sorrir. Percebi. Parece que voce dormiu com um cabide na boca."
str4 = u"Voce se casou quando tinha, sei la, oito? Bem vindo de volta ao mundo! Pegue uma colher!"

print sentence_distance(str1, str2)
print sentence_distance(str1, str3)
print sentence_distance(str1, str4)






    
    
    

