;;Francisco Perez
(define three (lambda (l)
               (cond
                [(null? l) #f]                ;;Returns #f if less than
                [(null? (cdr l))#f]           ;;3 elements
                [(null? (cddr l))#f]
                
                [(null? (cdddr l))                   ;; If exactly 3 elements
                 (cond                               ;; tests to make sure that 
                    [(= (car l) (cadr l)) #f]        ;; each element is different
                    [(= (car l) (caddr l)) #f]   
                    [(= (cadr l) (caddr l)) #f]
                    [else #t])]
                
                [(= (car l) (cadr l)) (three (cdr l))]       ;;Tests if first element equal 
                [(= (car l) (caddr l)) (three (cdr l))]      ;;to 2nd 3rd and 4th. If true
                [(= (car l) (cadddr l)) (three (cdr l))]     ;;removes first element.
                
                
                [(= (cadr l) (caddr l))(three (cons (car l)(cddr l)))]                      ;;If 2nd and 3rd element are the same
                [(= (cadr l) (cadddr l))(three (cons (car l)(cddr l)))]                     ;;If 2nd and 4th elements are the same
                [(= (caddr l) (cadddr l))(three (cons (car l)(cons (cadr l)(cdddr l))))]    ;;If 3rd and 4th elements are the same
                                                                                            ;;Will remove a repeat element. 
                [else #f])))
