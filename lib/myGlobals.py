  
from lib.PythonSetup import *

# path_to_ampl  = Path(r"C:/bin/ampl.mswin64.20221013/ampl.exe")
# solver        = '/opt/xpressmp/bin/amplxpress'
# datapath      = './CaseStudies/'
# solPath       = './CaseStudies/Solutions/'
solPath       = './Solutions/'

MitVars       = ['r', 'r_bar', 'r_prime', 'ResistanceCostByNode', 'StorageCostByNode', 'MitigationCostByNode']
RecoveryVars  = ['NodeUseCostByNodeByEvent', 'NodeDamageCostByNodeByEvent', 'NodeStartupCostByNodeByEvent', 'NodeCostByNodeByEvent', 'd', 'd_dot', 't']
UncertainVars = ['NodeUseCostByNodeByEvent', 'NodeDamageCostByNodeByEvent', 'NodeStartupCostByNodeByEvent', 'NodeCostByNodeByEvent', 'd', 'd_dot', 't']
TopLevelVars  = ['StorageCost', 'ResistanceCost', 'MitigationCost', 'EV_EventCosts', 'EV_TotalCost', 'RecoveryDisutility']
        

