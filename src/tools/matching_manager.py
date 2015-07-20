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
        return map(lambda i: (sen[i][0], sen[i+1][1], sen[i][2] + " " + sen[i+1][2]), range(len(sen)-1))        
        
    
    def get_best_match_idx(self, sub, trans):
        dists = map( lambda sen: self.sentence_distance(sub[2], sen[2]), trans)
        idxs = [i for i, j in enumerate(dists) if abs(j - max(dists)) < 0.05 ]
        # getting the best match with shortest transcription length (should change that!)
        return dists[idxs[0]], idxs[0]
    
    def match_subs_trans(self, subs, trans, original_subs):
        '''
            match subtitles (subs) stream with transcriptions (trans) stream
            
            returns the subtitle stream with corrected times
        '''
        
        # in case one subtitle matches with more than one transcription sentence
        trans2 = self.concatenate_adjacent_sentences(trans)
        
        matching = []
        
        # match subtitles to transcriptions
        for idx in range(len(subs)):
            sub = subs[idx]
            best_dist1, best_idx1 = self.get_best_match_idx(sub, trans)
            best_dist2, best_idx2 = self.get_best_match_idx(sub, trans2)
            
            best_dist = max(best_dist1, best_dist2)
            
            if best_dist >= self.sentence_distance_threshold :
                if best_dist == best_dist1:
                    matching.append([best_idx1])
                else :
                    matching.append([best_idx2,best_idx2+1])
            else:
                matching.append([])
        
        print matching
        
        # maps subtitles times to match transcriptions
        for idx in range(len(matching)):
            n_match = len(matching[idx])
            new_start_time = duration = 0
                        
            if n_match == 0:
                print "not matched"
                if idx > 0 and len(matching[idx-1]) == 1:
                    best_idx = matching[idx-1][0] + 1
                elif idx > 0 and len(matching[idx-1]) == 2:
                    best_idx = matching[idx-1][1] + 1
                elif idx+1 < len(matching) and len(matching[idx+1]) >= 1:
                    best_idx = matching[idx+1][0] - 1 
                else :
                    #keep the same time
                    best_idx = idx
                
                best_idx = max(best_idx, 0)
                best_idx = min(best_idx, len(trans)-1)
            else :
                best_idx = matching[idx][0]           
            
            print "idx , best_idx = ", idx, best_idx
            
            if idx > 0 and matching[idx-1] == matching[idx]:
                print "handles multiple subs to one transcription"
                # handles multiple subs to one transcription
                original_subs[idx] = (
                    original_subs[idx-1][0], #keep previous start time
                    trans[best_idx][1], #change to new final time
                    original_subs[idx-1][2] + "\n" + original_subs[idx][2]) #concatenate texts
                
                original_subs[idx-1] = None
            else :
                sub = subs[idx]
                new_start_time = trans[best_idx][0]
                duration = sub[1] - sub[0]
                print "handles normal case = ", new_start_time, duration
                original_subs[idx] = (new_start_time, new_start_time + duration, original_subs[idx][2])        
            
        return filter( lambda x: x is not None , original_subs)
            
            
            
    
    

