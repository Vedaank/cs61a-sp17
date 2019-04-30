(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car 
    (cdr s)
  )
)

(define (caddr s)
  (car
    (cdr
      (cdr s)
    )
  )
)

(define (sign x)
  (cond
    ((= x 0) 0)
    ((> x 0) 1)
    ((< x 0) -1)
  )
)

define (over-or-under x y)
  (if (= x y) 0 (if (> x y) 1 (if (< x y) -1)))


(define (square x) (* x x))

(define (pow b n) 
  (cond
    ((= n 0) 1)
    ((even? n) (pow (square b) (/ n 2)))
    ((odd? n) (* b (pow (square b) (/ (- n 1) 2))))
  )
)

(define (ordered? s)
  (cond
    ((null? s) #t)
    ((null? (cdr s)) #t)
    ((<= (car s) (cadr s)) (ordered? (cdr s)))
    (else #f)
  )
)

(define (nodots s)
  (define (hasdot? s) (and 
                        (pair? s) (not (or
                                        (pair? (cdr s)) (null? (cdr s))
                                  ))
                      )
  )
  (cond
    ((null? s) s)
    ((hasdot? s) (list (nodots (car s)) (cdr s)))
    ((pair? s) (cons (nodots (car s)) (nodots (cdr s))))
    (else s)
  )
)

; Sets as sorted lists

(define (empty? s) (null? s))

(define (contains? s v)
    (cond ((empty? s) false)
          ((> (car s) v) #f)
          ((< (car s) v) (contains? (cdr s) v))
          (else True)
    )
)

; Equivalent Python code, for your reference:
;
; def empty(s):
;     return s is Link.empty
;
; def contains(s, v):
;     if empty(s):
;         return False
;     elif s.first > v:
;         return False
;     elif s.first == v:
;         return True
;     else:
;         return contains(s.rest, v)

(define (add s v)
    (cond ((empty? s) (list v))
          ((contains? s v) s)
          ((< v (car s)) (cons v s))
          (else (cons (car s) (add (cdr s) v)))
    )
)

(define (intersect s t)
    (cond ((or (empty? s) (empty? t)) nil)
          ((= (car s) (car t)) (cons (car s) (intersect (cdr s) (cdr t))))
          ((< (car s) (car t)) (intersect (cdr s) t))
          ((> (car s) (car t)) (intersect s (cdr t)))
    )
)

; Equivalent Python code, for your reference:
;
; def intersect(set1, set2):
;     if empty(set1) or empty(set2):
;         return Link.empty
;     else:
;         e1, e2 = set1.first, set2.first
;         if e1 == e2:
;             return Link(e1, intersect(set1.rest, set2.rest))
;         elif e1 < e2:
;             return intersect(set1.rest, set2)
;         elif e2 < e1:
;             return intersect(set1, set2.rest)

(define (union s t)
    (cond ((empty? s) t)
          ((empty? t) s)
          (else (union (add s (car t)) (cdr t)))
    )
)

; Q9 - Survey
(define (survey)
    ; Midsemester Survey: https://goo.gl/forms/DJozOAVLzfXARJGn2
    'parenthesis
)