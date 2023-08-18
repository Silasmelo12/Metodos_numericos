PROGRAM UPSTREAM
       IMPLICIT NONE
       INTEGER :: I, J
       INTEGER :: NX, NT, NXT
       REAL(8) :: L, C, TFIM
       REAL(8) :: DX, DT, NI
       REAL(8) :: PI, X, T
       REAL(8), ALLOCATABLE :: U_NUM(:), U_ANA(:), U_NUM_OLD(:)
       REAL(8), ALLOCATABLE :: A(:), B(:), CC(:), D(:)
       
       EXTERNAL TDMA
       
       PI = 4*ATAN(1.D0)
       
       L = 40.D0
       C = 1.D0
       TFIM = 18.D0
       
       NXT = 41
       NX = NXT - 2
       NT = 30
       
       ALLOCATE( U_NUM(0:NX+1), U_ANA(0:NX+1), U_NUM_OLD(0:NX+1) )
       ALLOCATE( A(NX), B(NX), CC(NX), D(NX) )
       
       DX = L/(NXT-1)   ! DISCRETIZÇÃO DO ESPAÇO: MALHA EM X
       DT = TFIM/NT    ! DISCRETIZAÇÃO DO TEMPO
       
       NI = C*DT/DX    ! NUMERO DE COURANT
       
       WRITE(*,*)NI
       PAUSE
       
       OPEN(UNIT=2,FILE='OXENTE.DAT')
       
       
       ! CONDIÇÃO INICIAL
       WRITE(*,*)'TIME = ',0.D0
       WRITE(2,*)'TIME = ',0.D0
       DO J = 0, NX + 1
          X = J*DX
          IF(X .LE. 10.D0) THEN
             U_NUM_OLD(J) = 1.D0
          ELSE
             U_NUM_OLD(J) = 0.D0
          ENDIF
          WRITE(*,10)J, X, U_NUM_OLD(J)
          WRITE(2,10)J, X, U_NUM_OLD(J)
       ENDDO
       
     
       ! MARCHA NO TEMPO       
       DO I = 1, NT
          T = I * DT
          WRITE(*,*)'TIME = ',T
          WRITE(2,*)'TIME = ',T
          
          ! CONDIÇÕE DE CONTORNO
          U_ANA(0) = 1.D0
          U_ANA(NX+1) = 0.D0
          U_NUM(0) = 1.D0
          U_NUM(NX+1) = 0.D0
          
          DO J = 1, NX
            ! SOLUÇÃO ANALITICA
             X = J*DX
             IF(X-C*T .LE. 10.D0) THEN
                U_ANA(J) = 1.D0
             ELSE
                U_ANA(J) = 0.D0
             ENDIF
          ENDDO
          
          A = NI/2
          B = - NI/2
          CC = U_NUM_OLD(1:NX)
          CC(1) = CC(1) - B(1)*U_NUM_OLD(0)
          CC(NX) = CC(NX) - A(NX)*U_NUM_OLD(NX+1)
          D = 1.D0
          
          CALL TDMA(1,NX,B,D,A,CC)
          U_NUM(1:NX) = CC
          
          DO J = 0, NX + 1
             X = J*DX
             WRITE(*,10)J, X, U_ANA(J), U_NUM(J)
             WRITE(2,10)J, X, U_ANA(J), U_NUM(J)                 
          ENDDO
          U_NUM_OLD = U_NUM
         
       ENDDO  


10     FORMAT(5X,I3,3(5X,F12.4))
       
       
       END PROGRAM UPSTREAM
       
       
       
       
       
      SUBROUTINE TDMA(IL,IU,BB,DD,AA,CC)
      IMPLICIT NONE
      
      INTEGER :: LP, I, IL, IU
      REAL(8) :: R
      REAL(8) :: AA(IU), BB(IU), CC(IU), DD(IU)

      LP = IL + 1
      DO I = LP, IU
         R = BB(I)/DD(I-1)
         DD(I) = DD(I) - R*AA(I-1)
         CC(I) = CC(I) - R*CC(I-1)
       ENDDO
        CC(IU) = CC(IU)/DD(IU)
        
        DO I = IU, LP, -1
           CC(I) = (CC(I) - AA(I)*CC(I+1))/DD(I)
        ENDDO
        
        RETURN
        END
