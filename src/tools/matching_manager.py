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
        return re.sub('[.?!@#$&123456789;]', '', str).lower()
        
    
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
    
    def match_subs_trans(self, subs, trans, original_subs, acceptable_near_time = 1000):
        '''
            match subtitles (subs) stream with transcriptions (trans) stream
            
            returns the subtitle stream with corrected times
        '''
        
        # in case one subtitle matches with more than one transcription sentence
        trans2 = self.concatenate_adjacent_sentences(trans)
        
        matching = []
        # [[], [1], [1], [2], [2], [3], [4], [], [5, 6], [7], [], []]        
        
        # match subtitles to transcriptions
        for idx in range(len(subs)):
            sub = subs[idx]
            best_dist1, best_idx1 = self.get_best_match_idx(sub, trans)
            best_dist2, best_idx2 = self.get_best_match_idx(sub, trans2)
            
            best_dist = max(best_dist1, best_dist2)
            list_of_matches = []
            
            if best_dist >= self.sentence_distance_threshold :
                if best_dist == best_dist1:
                    list_of_matches = [best_idx1]
                else :
                    list_of_matches = [best_idx2,best_idx2+1]
            else:
                list_of_matches = []
            
            matching.append(list_of_matches)
            
            print "Matching", idx, " -> %7s"%list_of_matches, "(%.2f"%best_dist, " of certainty)"
        
        print "\nIntermediate matching = "
        print matching
        
        # maps subtitles times to match transcriptions
        for idx in range(len(matching)):
            n_match = len(matching[idx])
            new_start_time = duration = 0
                        
            if n_match == 0:      
                possible_idx = 0
                
                can_previous = idx > 0 and len(matching[idx-1]) >= 1
                can_next = idx+1 < len(matching) and len(matching[idx+1]) >= 1
                
                if can_previous and can_next:
                    #get the one with most difference in time form subtitle to transcription
                    time_trans_prev = trans[matching[idx-1][-1]][1] - trans[matching[idx-1][0]][0]
                    time_trans_next = trans[matching[idx+1][-1]][1] - trans[matching[idx+1][0]][0]
                    time_sub_prev = trans[matching[idx-1][-1]][1] - trans[matching[idx-1][0]][0]
                    time_sub_next = trans[matching[idx+1][-1]][1] - trans[matching[idx+1][0]][0]
                    
                    if abs(time_sub_prev - time_trans_prev) > abs(time_sub_next - time_trans_next) :
                        possible_idx = matching[idx-1][-1] + 1
                    else :
                        possible_idx = matching[idx+1][0] - 1
                elif can_previous:
                    possible_idx = matching[idx-1][-1] + 1     
                elif can_next:
                    possible_idx = matching[idx+1][0] - 1
                else :
                    #keep the same time
                    possible_idx = idx
                
                possible_idx = max(possible_idx, 0)
                possible_idx = min(possible_idx, len(trans)-1)
                matching[idx] = [possible_idx]
            
            best_idx = matching[idx][0]
            
            if idx > 0 and len(matching[idx-1]) > 0 and len(matching[idx]) > 0 and matching[idx-1][-1] == matching[idx][0]:                
                # handles multiple subs to one transcription
                original_subs[idx] = (
                    original_subs[idx-1][0], #keep previous start time
                    trans[matching[idx][-1]][1], #change to new final time
                    original_subs[idx-1][2] + "\n" + original_subs[idx][2]) #concatenate texts
                
                original_subs[idx-1] = None
            else :
                #handles normal case
                sub = subs[idx]
                new_start_time = trans[best_idx][0]
                duration = sub[1] - sub[0]                
                original_subs[idx] = (new_start_time, new_start_time + duration, original_subs[idx][2])        
            
            #separete subtitles with intersecting time
            if idx > 0 and original_subs[idx-1] is not None and original_subs[idx-1][1] > original_subs[idx][0]:
                if original_subs[idx-1][1] - original_subs[idx][0] <= acceptable_near_time:                    
                    time_diff = original_subs[idx-1][1] - original_subs[idx][0]
                    prev = original_subs[idx-1]
                    cur = original_subs[idx]
                    
                    original_subs[idx-1] = (prev[0], prev[1] - int(time_diff/2) - 2, prev[2])
                    original_subs[idx] = (cur[0] + int(time_diff/2) + 2, cur[1], cur[2])     
    
        return filter( lambda x: x is not None , original_subs)
            
            