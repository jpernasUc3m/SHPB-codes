import numpy as np
import matplotlib.pyplot as plt






vectordeformacion= []
vectortiempo=[]
vectortension1=[]
vectortension2=[]
vectortensionreflejada=[]
vectortensiontransmitida=[]
vectortensionincidente=[]
vectorvelocidad=[]
vectordeltatensiones=[]
vectordif=[]


# Elegir modo: 0 leer grafica de tension incidente y calcular tensiones o 2 calcular tension 
modo=1


x=5e-5
difdeform=x
velmin=4990
velmax=5010

Eb=210e9
Ep=3.85e9
deformaciongalga = 0
lp=10e-3
rop=1275
cp=(Ep/rop)**0.5
rob=7890
cb=(Eb/rob)**0.5
Ap=0.000791
Ab=Ap*5
t0=(lp/cp)


timestep=t0/10
alfa = (rob*cb*Ab)/(rop*cp*Ap)
f=Ab/Ap
A= (2*f)/(alfa+1)
B= (2*alfa)/((1+alfa)*f)
C= ((alfa-1)/(alfa+1))


def tensionincidente():
       
    return deformaciongalga*Eb
        
def tensionincidentebucle(j):
  
    k=j/timestep
    k=int(k)
    z=vectortensionincidente[k]
    return     z

def tensionreflejada():
    if(n%2==0):
      
        sumatorio=0
        cont=1
        while cont <= (n/2):
            
            sumatorio = sumatorio + C**(2*cont-1)*tensionincidentebucle(t-2*cont*t0)
            cont=cont+1
    
           
        return -tensionincidente()*C+A*B*sumatorio
    
    else:
       
        
        sumatorio=0
        cont=1
        while cont <= ((n-1)/2):
                
            sumatorio = sumatorio + C**(2*cont-1)*tensionincidentebucle(t-2*cont*t0)
            cont=cont+1
    
            
        return -tensionincidente()*C+A*B*sumatorio


def tension1(): 
    if(n%2==0):    
        sumatorio=0
        cont=1
        while cont <= n/2:
                    
            sumatorio = sumatorio + (C**(2*cont-1) + C**(2*cont))*tensionincidentebucle(t-2*cont*t0)
            cont=cont+1
            
        return A*(tensionincidente()+sumatorio)
    else:
        sumatorio=0
        cont=1
        while cont <= (n-1)/2:
                    
            sumatorio = sumatorio + (C**(2*cont-1) + C**(2*cont))*tensionincidentebucle(t-2*cont*t0)
            cont=cont+1
            
        return A*(tensionincidente()+sumatorio)


def tensiontransmitida():
    
    if(n%2==0):
        
        sumatorio=0
        cont=1
        while cont <= (n/2):
          

            sumatorio = sumatorio + (C**(2*cont-2))*tensionincidentebucle(t-(2*cont-1)*t0)
            cont=cont+1

                
        return A*B*sumatorio
    
    
    else:
        sumatorio=0
        cont=1
        while cont <= ((n+1)/2):
          

            sumatorio = sumatorio + (C**(2*cont-2))*tensionincidentebucle(t-(2*cont-1)*t0)
            cont=cont+1

                
        return A*B*sumatorio


def tension2():
     
    if(n%2==0):
        sumatorio=0
        cont=1
        while cont <= (n+1)/2:
                     
        
            sumatorio = sumatorio + (C**(2*cont-2) + C**(2*cont-1))*tensionincidentebucle(t-(2*cont-1)*t0)   
            cont=cont+1
               
        return A*sumatorio
    
    else:
        
        sumatorio=0
        cont=1
        while cont <= n/2:
                     
        
            sumatorio = sumatorio + (C**(2*cont-2) + C**(2*cont-1))*tensionincidentebucle(t-(2*cont-1)*t0)   
            cont=cont+1
        return A*sumatorio

    

def velocidaddeformación():
            
    return (tensionincidente()-tensionreflejada()-tensiontransmitida())/(rob*cb*lp)
    

def deltatensiones():
    if(t==0):
        return 0
    else:

        return 2*100*((tension1()-tension2())/(tension1()+tension2()))
    

  
t=0    
ten1=0
ten2=0
tenr=0
tent=0
dif=0
   
vectortensionincidente.append(0)
vectortiempo.append(0)
vectordeformacion.append(0)
vectorvelocidad.append(0)
vectordeltatensiones.append(0)
vectortensionreflejada.append(0)
vectortensiontransmitida.append(0)
vectortension1.append(0)
vectortension2.append(0)
vectordif.append(0)
    
while t<500:
        
  deformaciongalga=deformaciongalga+difdeform
  print('la deformacion es',deformaciongalga)
  # print('la diefenrecia de deformacion es',difdeform)
  n=int(t/t0)
        
  if (n%2==0 or n==0):
            
       # print(n*t0,'<t<',(n+1)*t0)
     print ('par')     
     teni=tensionincidente()
     vectortensionincidente=np.append(vectortensionincidente,teni)
     ten1=tension1()
     tenr=tensionreflejada()
     delta=deltatensiones()
     v=velocidaddeformación()
     print ('velocidad de deformacion',v)
     print('tension reflejada',tenr)
     print('tension transmitida',tent)
     print('tension incidente',tensionincidente())
                
                
                
                #Liao chen- equilirbio de tensiones para saber equilibrio de tensiones ha de ser<10% para equilibrio
                # We assume that if the strainrate increases to 90% of its steady value then nearly strain rate is achieved.
                
                           
                
                    
  else :
                    
    # print(n*t0,'<t<',(n+1)*t0)
    print ('impar')
    teni=tensionincidente()
    vectortensionincidente=np.append(vectortensionincidente,teni)
    ten2=tension2()
    tent=tensiontransmitida()
    delta=deltatensiones()
    v=velocidaddeformación()
    print ('velocidad de deformacion',v)
    print('tension reflejada',tenr)
    print('tension transmitida',tent)
    print('tension incidente',tensionincidente())
                    
                    
                    
                    
                    #Liao chen- equilirbio de tensiones para saber equilibrio de tensiones ha de ser<10% para equilibrio
                    # We assume that if the strainrate increases to 90% of its steady value then nearly strain rate is achieved.
                    
                    
  if (velmin<v and v<velmax):
                        
      t=t+timestep
      print ('t vale',t)
      print ('nvale',n)
      dif = (-1*tensionreflejada()+tensiontransmitida())/tensionincidente()
      vectordif.append(dif)
      vectortiempo.append(t)
      vectordeformacion.append(deformaciongalga)
      vectorvelocidad.append(v)
      vectordeltatensiones.append(delta)
      vectortensionreflejada.append(tenr)
      vectortensiontransmitida.append(tent)
      vectortension1.append(tension1())
      vectortension2.append(tension2())
         
                
  elif (v<velmin):
            
            
   vectortensionincidente=np.delete(vectortensionincidente,(len(vectortensionincidente)-1))
   deformaciongalga=deformaciongalga-difdeform
   difdeform=difdeform+1e-5
   print('velocidad def. muy BAJA')
                
                
                                 
  elif (v>velmax): 
            
            
   vectortensionincidente=np.delete(vectortensionincidente,(len(vectortensionincidente)-1))
   deformaciongalga=deformaciongalga-difdeform
   difdeform=difdeform-1e-5
   print('velocidad def. muy ALTA')
                    
                    
                    
  if(difdeform<0):
                        
   deformaciongalga=deformaciongalga-difdeform
   difdeform=x      
                        
                           
                        
  if  (n==20):
        
      print(delta)
      print (v)  
      print('fin')
      print (alfa)
      break
 
    
  else:
    
      print('n vale',n)
        
    


fig, (ax1) = plt.subplots(1)
fig, (ax2) = plt.subplots(1)
fig, (ax3) = plt.subplots(1)
fig, (ax4) = plt.subplots(1)
fig, (ax5) = plt.subplots(1)
fig, (ax6) = plt.subplots(1)

    



    

        
ax1.plot(vectortiempo, vectordeformacion)
ax1.set_xlabel('Tiempo [s]')
ax1.grid()
ax2.grid()
ax1.set_ylabel('Deformacion [m]')
ax1.set_title('Deformación probeta')
ax2.plot(vectortiempo, vectorvelocidad)
ax2.set_xlabel('Tiempo [s]')
ax2.set_ylabel('Velocidad de deformacion [1/s]')
ax2.set_title('Velocidad de deformación')
ax4.plot(vectortiempo, vectordeltatensiones,'b')
ax4.grid()
ax4.set_xlabel('Tiempo [s]')
ax4.set_ylabel('Diferencia de tensiones [%]')
ax4.axhline(y=10)
ax4.set_title('Diferencia de tensiones')
ax3.grid()
ax3.plot(vectortiempo, vectordif)
ax3.set_xlabel('Tiempo [s]')
ax3.set_ylabel('Ratio de tensiones')
ax3.set_title('Ratio de tensiones')
ax5.grid()
ax5.set_xlabel('Tiempo [s]')
ax5.set_ylabel('Tension [Pa]')
ax5.set_title('Tension en la probeta')
ax3.axhline(y=0.9)
ax3.axhline(y=1.1)
ax5.plot(vectortiempo, vectortension1,'r',label='Tension cara 1')
ax5.plot(vectortiempo, vectortension2,'g',label='Tension cara 2')
ax5.legend()
ax6.plot(vectortiempo, vectortensionincidente,'r',label='Tension incidente')
ax6.plot(vectortiempo, vectortensiontransmitida,'b',label='Tension transmitida')
ax6.plot(vectortiempo, vectortensionreflejada,'g', label ='Tension reflejada')
ax6.grid()
ax6.set_xlabel('Tiempo [s]')
ax6.set_ylabel('Tensiones [Pa]')
ax6.set_title('Tensiones en barras')
ax6.legend()
ax1.figure.savefig("Def peek-acero.png")
ax2.figure.savefig("Vel peek-acero.png")
ax3.figure.savefig("ratio peek-acero.png")
ax4.figure.savefig("Diferencia  peek-acero.png")
ax5.figure.savefig("Tensiones caras  peek-acero.png")
ax6.figure.savefig("Tensiones in  peek-acero.png")


    


    



    # plt.plot(vectortiempo, (vectortensionincidente+vectortensionreflejada)/vectortensiontransmitida)
    #plt.plot(vectortiempo, vectortensionincidente, 'r')
    #plt.plot(vectortiempo, vectortensionreflejada,'b')
    #plt.plot(vectortiempo, vectortensiontransmitida,'g')
plt.show()




