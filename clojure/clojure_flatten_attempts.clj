(defn flatten [xs] (filter integer? (rest (tree-seq (complement integer?) identity xs))))

(defn flatten2 [xs] (tree-seq (complement integer?) identity xs))

(defn flatten_better [xs] (
  if (or seq (filter integer?(identity xs) seq (filter not-empty(filter vector?(identity xs))))) (concat 
    (filter integer?(identity xs))
    (map flatten_better(filter not-empty(filter vector?(identity xs)))))
    nil
))

(defn flatten_better2 [xs] ( 
    (doseq [i xs] (println i)
)))

(doall(flatten_better2(object-array[1, [2 [3  4]] 5])))
(every? vector?(object-array[0, [1,2]])) ; false. 0 int
(every? vector?(object-array[[1,2]])) ; true. 
(and(every? vector?(object-array[[1,2]])) every?(not(empty?(object-array[[1,2]])))) ; true. everyone is a vector, and every one is not empty. 
(and(every? vector?(object-array[[]]))) ; true. everyone is a vector. 
(and(every? vector?(object-array[1,2,()])) not(every? nil?(object-array[1,2,()]))) ;false. everyone is a factor, but not every one is null. 
(not(every? nil?(object-array[1,2, ()]))) ; false
(seq (filter not-empty(filter vector?(object-array[1, 2, [3, 4], 5]))))
(seq (filter not-empty(filter vector?(object-array[1, 2, [], 5]))))
(seq (filter not-empty(filter vector?(object-array[1, 2, [], 5]))))
(filter (or seq (filter integer?(object-array[1, 2, [3,4], 5])) seq filter not-empty(filter vector?(object-array[1, 2, [3, 4], 5]))))
