import os
import jellyfish as jf
import re

class matching_manager():

    def __init__(self, jw_threshold = 0.85, factors = [1, 1.7, 2, 2.7], sentence_distance_threshold = 0.5):
        '''
            jw_threshold(double) threshold for Jaro Winkler Distance to consider two words similar
        '''
        self.jw_threshold = jw_threshold
        if len(factors) != 4:
            raise Exception('Invalid factors argument.')
        self.factors = factors
        self.sentence_distance_threshold = sentence_distance_threshold
    
    def canonize(self,str):
        return re.sub('[.?!@#$]', '', str).lower()
        
    
    # Return 1 if sentences are the same and 0 if they are completely different
    def sentence_distance(self, sen1, sen2):
        #initiate variables
        distance = count = last_matches = 0        
        
        #generate list of words
        list_w1 = sen1.split(' ')
        list_w2 = sen2.split(' ')
        
        #calculates distance
        for w1 in list_w1:
            word_dist = map( lambda w2 : jf.jaro_winkler(self.canonize(w1),self.canonize(w2)), list_w2)
            val = max(word_dist)
            length = len(w1) * self.factors[last_matches]
            if val > self.jw_threshold:
                distance += val * length
                count += length
                last_matches = min(3,last_matches+1)
            else :
                count += length / 2.0
                last_matches = max(0,last_matches-1)
                
        if count > 0 :
            distance /= count
            
        return distance
    
    # NOT USING THIS...
    def break_into_sentences(self, sen, delimiters=['!','.','?',';']):
        # break transcriptions, generating parts that represent sentences
        for delimiter in delimiters :
            sen = map(lambda tok : tok.split(delimiter), sen)
            sen = reduce(lambda a, b: a+b, sen, [])
            sen = filter(lambda a: len(a) > 0, sen)

    def concatenate_adjacent_sentences(self, sen):
        # concateneting sentences
        sen2 = map(lambda i: (sen[i][0], sen[i+1][1], sen[i][2] + " " + sen[i+1][2]), range(len(sen)-1))        
        sen += sen2
        return sen
    
    def get_best_match_idx(self, sub, trans):
        dists = map( lambda sen: self.sentence_distance(sub[2], sen[2]), trans)
        idxs = [i for i, j in enumerate(dists) if abs(j - max(dists)) < 0.05 ]
        # print sub
        # print trans[idxs[0]]
        # print idxs[0], dists[idxs[0]]
        # print "=============="
        # getting the best match with shortest transcription length (should change that!)
        return dists[idxs[0]], idxs[0]
    
    def get_sub_new_time(self, sub, trans):
        best_dist, idx = self.get_best_match_idx(sub, trans)
        duration = sub[1] - sub[0]
        if best_dist >= self.sentence_distance_threshold :
            new_start_time = trans[idx][0]
        else:
            # doesn't change the original time
            new_start_time = sub[0]
        return (new_start_time, new_start_time + duration, sub[2])
    
    def match_subs_trans(self, subs, trans):
        '''
            match subtitles (subs) stream with transcriptions (trans) stream
            
            returns the subtitle stream with corrected times
        '''
        # in case one subtitle matches with more than one transcription sentence
        trans = self.concatenate_adjacent_sentences(trans)
        
        # maps subtitles times to match transcription
        return map( lambda sub: self.get_sub_new_time(sub, trans), subs)
            
            
            
    
    

