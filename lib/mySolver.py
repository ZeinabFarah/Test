from lib.PythonSetup import *
import lib.myGlobals

def environment(path):
    try: ampl
    except NameError: ampl = None
    if ampl==None:
        ampl = AMPL(Environment(str(path)))
        print(ampl.eval('option version;'))
    return ampl
        
def Configure(ampl):    
#     ampl.setOption('solver', myGlobals.solver)
    ampl.eval('option presolve 0;')
    ampl.eval('option solver_msg 0;')

def Run(ampl, fname=None):
#  This function solves the math program with the selected objective. 
#  However, to deal with alternate optima, it then constrains the value of the selective obj function, 
#  so it cannot worsen and then sequentially swaps in other objectives. 
#  Please refer to the technical note.
    postfix='_LIMIT'  #used as postfix for some temporary constraints
    msg=ampl.getOutput('solve;')
#     print(ampl.getValue('_solve_time'))
    r=ampl.getValue('solve_result_num')
    isoptimal=False
    if r<0 or r>=100:
        print(ampl.getValue('solve_message')) 
    else:
        isoptimal=True
        currobj=ampl.getCurrentObjective()
        s=str(currobj)
        LHS=s[s.find(":")+1:s.find(";")]
        newobjcname=f'CURR{postfix}'
        if currobj.minimization():
            sense='<='
            RHS=f'{currobj.value()+0.000001}'
        else:
            sense=">="
            RHS=f'{currobj.value()-0.000001}'
        ampl.eval(f'{newobjcname}: {LHS}{sense}{RHS};')  #Adds new temp constraint
        for i, obj in ampl.getObjectives():
            s=str(obj)
            ampl.eval(f'objective {obj.name()};')
            ampl.getOutput('solve;') 
            r=ampl.getValue('solve_result_num')

            if r<0 or r>=100:
                isoptimal=False
                print(ampl.getValue('solve_message')) 
                break

            LHS=s[s.find(":")+1:s.find(";")]
            newcname=f'Obj{i}{postfix}'
            if obj.minimization():
                sense='<='
                RHS=f'{obj.value()+0.0001}'
            else:
                sense=">="
                RHS=f'{obj.value()-0.0001}'
            ampl.eval(f'{newcname}: {LHS}{sense}{RHS};')  #Adds new temp constraint
        ampl.eval(f'objective {currobj.name()};')
        ampl.getOutput('solve;')  #solve just to get correct objective fxn in place; else confusing
#             cycle through to delete temporary constraints
        for i, obj in ampl.getObjectives():
            s=str(obj)
            LHS=s[s.find(":")+1:s.find(";")]
            newcname=f'Obj{i}{postfix}'
            ampl.eval(f'delete {newcname};')  #deletes new temp constraint
#                 Loop to run through all objectives
#                 drop all limit constraints or make infinity
        ampl.eval(f'delete {newobjcname};')  #deletes new temp constraint 
    return isoptimal
