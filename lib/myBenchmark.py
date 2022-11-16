  
from lib.PythonSetup import *

def DoNothing_Scenario(ampl):
    ampl.eval('objective RecoveryDisutilityObjectiveFxn;')
    ampl.eval('fix {i in I} r[i] := 0;')
    ampl.eval('fix {(i,p) in IX} s[i,p] := 0;')
    ampl.eval('fix {i in I, e in E} y_plus[i,e] := 0;')

def UnlimitedBudget_Scenario(ampl):
    ampl.eval('objective RecoveryDisutilityObjectiveFxn;')
    ampl.getParameter('EV_TotalCost_OVERBRACE').set(float("inf"))
