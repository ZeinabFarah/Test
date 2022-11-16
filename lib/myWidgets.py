
from lib.PythonSetup import *
import lib.myGlobals
import lib.myVisualization
import lib.myBenchmark
import lib.myDirectory
import lib.mySolver
import lib.myStats

class mainWidgets:  
    
    global uncertainty_upper_bound      
    uncertainty_upper_bound = {}
    
    def __init__(self, ampl, myAMPL, basesnapshot):
        self.ampl=ampl
        self.myAMPL=myAMPL
        self.basesnapshot=basesnapshot

    ## Button Widgets
    btnInputClear = ipywidgets.Button(
        description='Clear Selected Files',
        disabled=False,
        button_style='danger',
        tooltip='Click to clear selected files',
        icon='')
    
    def on_btnInputClear_clicked(self, b):   
        ampl=self.ampl
        with self.Dataset_out:
            self.Dataset_out.clear_output()

            if self.InputUpload.value != {}:                          
                self.InputUpload.data.clear()
                self.InputUpload.metadata.clear()
                self.InputUpload.set_state({'_counter': 0})
                self.InputUpload.send_state()

                ampl.eval('reset data;')

                print('\033[1m', '\n ------Selected files cleared------ \n','\033[0m')

                self.SystemComponents.options = []
                self.SystemComponents_grid.children = ()
                self.RecoveryEndPoint.options = []
                self.BenchmarkSol.options = []
                self.Objfxn.options = []
                self.Constraints.options = []

                with self.SystemComponents_out:
                    self.SystemComponents_out.clear_output()          
                with self.SysGraphDisplay_out:
                    self.SysGraphDisplay_out.clear_output()
                with self.Recovery_out:
                    self.Recovery_out.clear_output()
                with self.Solver_out:
                    self.Solver_out.clear_output()
                                        
    btnInputPreview = ipywidgets.Button(
        description='Preview',
        disabled=False,
        button_style='info',
        tooltip='Click to preview',
        icon='search')

    def on_btnInputPreview_clicked(self, b):
        with self.Dataset_out:
            self.Dataset_out.clear_output()
            if self.InputSheets.value == ():
                print('\033[1m', '\n ------No sheet selected------ \n','\033[0m')
            else:
                # df = pd.read_excel(io.BytesIO(mainWidgets.InputUpload.value[0].content), list(mainWidgets.InputSheets.value))
                df = pd.read_excel(self.InputUpload.value[self.InputFiles.value]['content'], list(self.InputSheets.value))
                display(df)   
                        
    btnInputUpload = ipywidgets.Button(
        description='Upload',
        disabled=False,
        button_style='warning',
        tooltip='Click to Upload',
        icon='check')
    
    def on_btnInputUpload_clicked(self, b):
        ampl=self.ampl
        myAMPL=self.myAMPL
        basesnapshot = self.basesnapshot
        
        with self.Dataset_out:
            self.Dataset_out.clear_output()

            if self.InputUpload.value == {}:
                print('\033[1m', '\n ------No file selected------ \n','\033[0m')
            else:
                ampl.eval('reset data;')

                lib.mySolver.Configure(ampl)
                
                ampl.setData(DataFrame.fromPandas(pd.read_excel(self.InputUpload.value['CommunityData.xlsx']['content'],'P',index_col=0)),'P')
                ampl.setData(DataFrame.fromPandas(pd.read_excel(self.InputUpload.value['CommunityData.xlsx']['content'],'I',index_col=0)),'I')
                ampl.setData(DataFrame.fromPandas(pd.read_excel(self.InputUpload.value['CommunityData.xlsx']['content'],'IX',index_col=[0,1])),'IX')
                ampl.setData(DataFrame.fromPandas(pd.read_excel(self.InputUpload.value['CommunityData.xlsx']['content'],'OX',index_col=[0,1])),'OX')
                ampl.setData(DataFrame.fromPandas(pd.read_excel(self.InputUpload.value['CommunityData.xlsx']['content'],'DLNK',index_col=[0,1])),'DLNK')
                ampl.setData(DataFrame.fromPandas(pd.read_excel(self.InputUpload.value['CommunityData.xlsx']['content'],'LNK',index_col=[0,1,2])),'LNK')
                ampl.setData(DataFrame.fromPandas(pd.read_excel(self.InputUpload.value['CommunityData.xlsx']['content'],'PRC',index_col=[0,1,2])),'')
                ampl.setData(DataFrame.fromPandas(pd.read_excel(self.InputUpload.value['CommunityData.xlsx']['content'],'E',index_col=0)),'E')
                ampl.setData(DataFrame.fromPandas(pd.read_excel(self.InputUpload.value['CommunityData.xlsx']['content'],'L',index_col=[0,1])),'')

                self.SystemComponents.options = ['Sets', 'Parameters']  
                self.SetDisplay.options = [re.sub("[<>].*[>]","",ampl.getValue('alias(' + s.name() + ')')) + '(' + s.name() + ')' for index, s in ampl.getSets()]
                self.ParamDisplay.options = [re.sub("[<>].*[>]","",ampl.getValue('alias(' + p.name() + ')')) + '(' + p.name() + ')' for index, p in ampl.getParameters()]
                self.GraphLayout.options = ['manual', 'dot', 'circular', 'kamada_kawai', 'random', 'shell', 'spring', 'spectral', 'spiral']
                self.GraphLayout.value = 'manual'
                self.RecoveryEndPoint.options = ampl.getData('I').toList()
                self.fragility_components.options = ampl.getData('I').toList()
                self.uncertainty_params.options = set([p for p in basesnapshot.ParameterNamesAsSet]).difference(set(['restor_end', 'M']))
                self.UncertainVarsSelect.options = [myAMPL.getEntityInfo(ampl.getVariable(var)).ampl_alias for var in lib.myGlobals.UncertainVars]  
                self.TopLevelVarsSelect.options = [myAMPL.getEntityInfo(ampl.getVariable(var)).ampl_alias for var in lib.myGlobals.TopLevelVars]
    
                # os.makedirs(lib.myGlobals.datapath, exist_ok=True)
                lib.myDirectory.Clear(lib.myGlobals.solPath)
                os.makedirs(lib.myGlobals.solPath, exist_ok=True)

                print('\033[1m', '\n ------Input files loaded------ \n','\033[0m')

                with self.SysGraphDisplay_out:
                    self.SysGraphDisplay_out.clear_output()
                    
    btnSysComponentDisplay = ipywidgets.Button(
        description='Display',
        disabled=False,
        button_style='warning',
        tooltip='Click to display system components',
        icon='pencil')
                    
    def on_btnSysComponentDisplay_clicked(self, b):
        myAMPL = self.myAMPL
        with self.SystemComponents_out:
            self.SystemComponents_out.clear_output()
            if self.InputUpload.value != {}:
                if self.SystemComponents.value == 'Sets':
                    display(myAMPL.getData(re.search('\((.*?)\)', self.SetDisplay.value).groups()[0]))
                elif self.SystemComponents.value == 'Parameters':
                    display(myAMPL.getData(re.search('\((.*?)\)', self.ParamDisplay.value).groups()[0]))

    btnSysGraphDisplay = ipywidgets.Button(
        description='Display',
        disabled=False,
        button_style='warning',
        tooltip='Click to display system dependency',
        icon='pencil')
    
    edge_details = ipywidgets.HTML()    
    node_details = ipywidgets.HTML()

    def on_btnSysGraphDisplay_clicked(self, b):
        ampl = self.ampl
        basesnapshot = self.basesnapshot
        Visualize = lib.myVisualization.myVisualization(ampl, basesnapshot)
        
        with self.SysGraphDisplay_out:
            self.SysGraphDisplay_out.clear_output()

            if self.InputUpload.value != {}:
                if self.GraphLayout.value == 'manual' and self.CoordinatesUpload.value == {}:
                    print('\033[1m', '\n ------No coordinates loaded. Select another layout or upload the coordinates------ \n','\033[0m')
                else:
                    fig, edges, edges_hover, nodes, layouts = Visualize.NetworkViz(Visualize.nxGraph(), self.GraphLayout.value)
                    edges = Visualize.dashed_DLNK(edges)                    
                    
                    def edge_hover_fn(trace, points, state):
                        if points.point_inds:
                            ind = points.point_inds[0]
                            hover_info_df = Visualize.edge_hover_df(ind)
                            self.edge_details.value = hover_info_df.to_html()
                          
                    edges_hover.on_hover(edge_hover_fn)
                    
                    def node_hover_fn(trace, points, selector):                     
                        for edge in edges:
                            edge.line.color = 'black' 
                            edge.line.width = 1
                        for index in points.point_inds:                                  
                            G = Visualize.nxGraph()

                            for all_edges in list(G.in_edges(nodes.text[index]))+list(G.out_edges(nodes.text[index])):
                                for i, edge in enumerate(edges):
                                    if tuple(edge.customdata[0]) == all_edges:
                                        edge.line.width = 1.5
                                        if list(G.get_edge_data(*all_edges).values()) == ['P']:
                                            edge.line.color = 'red' 
                                        elif list(G.get_edge_data(*all_edges).values()) == ['W']:
                                            edge.line.color = 'blue' 
                                                                         
                            hover_info_df = Visualize.node_hover_df(index)
                            self.node_details.value = hover_info_df.to_html()

                            image_data = {}
                            for img_filename in self.ImageUpload.value.keys():
                                component = img_filename.split('.')[0]
                                image_data[component] = self.ImageUpload.value[img_filename]['content']
                            if self.ImageUpload.value != {}:
                                self.image_widgets.value = image_data[list(Visualize.nxGraph().nodes())[index]] 

                    nodes.on_hover(node_hover_fn)

                    if self.ImagesUploadCheckBox.value == True:
                        if self.ImageUpload.value == {}:
                            print('\033[1m', '\n ------No images uploaded------ \n','\033[0m')
                        else:
                            display(ipywidgets.VBox([ipywidgets.HBox([fig, 
                                                                      self.image_widgets]),
                                                     self.node_details,
                                                     self.edge_details]))
                    else:
                        display(ipywidgets.VBox([fig, 
                                                 self.node_details, 
                                                 self.edge_details]))
                        
    btnGisMapDisplay = ipywidgets.Button(
        description='Display',
        disabled=False,
        button_style='warning',
        tooltip='Click to display GIS map',
        icon='pencil')
    
    def on_btnGisMapDisplay_clicked(self, b):
        ampl = self.ampl
       
        m = folium.Map(location=[34.625, -79.00], zoom_start=13)
        # iterate through all the components and create markers for each
        for index in ampl.getData('I'):
            name = index[0]
            location = (ampl.getParameter('LAT').get(name), ampl.getParameter('LONG').get(name))
            year = ampl.getParameter('YEAR').get(name)
            output = ampl.getParameter('OUTPUT').get(name)
            message = "Name: " + name + "<br>" + "Year: " + str(year) + "<br>" + "Output: " + str(output)
            marker = folium.Marker(location=location, draggable=False, title=name, popup=message).add_to(m) 
            
        # Read the geojson file
        # geo_blocks = gpd.read_file('./Lumberton_Blocks.geojson')
        geo_blocks = gpd.read_file(io.BytesIO(self.GeoJsonUpload.value['City_Blocks.geojson']['content']))
        
        # Read in the SoVI file
        SoVI_df = pd.read_excel(self.SoVIUpload.value['City_Blocks_SoVI.xlsx']['content'], 'City_Blocks_SoVI', index_col=0)
        
        # Merge the datasets: SoVI_df and geo_blocks
        final_df = geo_blocks.merge(SoVI_df, on = "id")
        
        #Create the choropleth map
        folium.Choropleth(
            geo_data = final_df,
            name = "choropleth",
            data = final_df,
            columns = ["id", "NORM_SoVI"],
            key_on = "feature.properties.id",
            fill_color = "BuPu",
            fill_opacity = 0.9,
            line_opacity = 0.9,
            legend_name = "Normalized SoVI Score",
            smooth_factor = 0,
            Highlight = True,
            line_color = "#0000",
            show = True,
            overlay = True,
            nan_fill_color = "White",
            bins = 4
        ).add_to(m)

        # Add hover functionality.
        style_function = lambda x: {'fillColor': '#ffffff', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.1, 
                                    'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                        'color':'#000000', 
                                        'fillOpacity': 0.50, 
                                        'weight': 0.1}
        hovr = folium.features.GeoJson(
            data = final_df,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=['NAME_x','NORM_SoVI'],
                aliases=['Block ID','Normalized SoVI'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
        )
        m.add_child(hovr)
        m.keep_in_front(hovr)

        # We add a layer controller
        folium.LayerControl().add_to(m)
        with self.GisMapDisplay_out:
            self.GisMapDisplay_out.clear_output()
            m.save('./index.html')
            display(m)      
                        
    btnRecoveryEndPointSet = ipywidgets.Button(
        description='Set',
        disabled=False,
        button_style='warning',
        tooltip='Click to Upload',
        icon='')

    def on_btnRecoveryEndPointSet_clicked(self, b): 
        ampl = self.ampl
        myAMPL = self.myAMPL
        with self.Recovery_out:
            self.Recovery_out.clear_output()

            if self.InputUpload.value != {}:
                p=ampl.getParameter('restor_end').set(self.RecoveryEndPoint.value)
                print('\033[1m', f'\n ------The recovery end point is set to be {self.RecoveryEndPoint.value}------ \n','\033[0m')

                self.Objfxn.options = ['Minimize the EV recovery time', 'Minimize the EV total cost']
                self.BenchmarkSol.options = ['Do Nothing', 'Unlimited Budget']
                self.MitVarsSelect.options = lib.myGlobals.MitVars
                self.RecoveryVarsSelect.options = lib.myGlobals.RecoveryVars

    btnSolve = ipywidgets.Button(
        description='Run Solver',
        disabled=False,
        button_style='info',
        tooltip='Click to run the solver',
        icon='')
    
    def on_btnSolve_clicked(self, b):
        ampl = self.ampl
        myAMPL = self.myAMPL
        basesnapshot = self.basesnapshot

        with self.Solver_out:
            self.Solver_out.clear_output()

            if self.InputUpload.value != {}:

                if self.Solver_accordion.selected_index == 0:  

                    if self.BenchmarkSol.value == 'Do Nothing':
                        lib.myBenchmark.DoNothing_Scenario(ampl)
                    elif self.BenchmarkSol.value == 'Unlimited Budget':
                        lib.myBenchmark.UnlimitedBudget_Scenario(ampl)

                elif self.Solver_accordion.selected_index == 1:

                    if self.Objfxn.value == 'Minimize the EV recovery time':
                        ampl.eval('objective RecoveryDisutilityObjectiveFxn;')
                        
                    elif self.Objfxn.value == 'Minimize the EV total cost':
                        ampl.eval('objective EV_TotalCostObjectiveFxn;')

                    if self.Constraints.value == 'Total expected costs upper limit':
                        ampl.getParameter('EV_TotalCost_OVERBRACE').set(self.BudgetLimit.value)
                    elif self.Constraints.value == 'Total expected recovery time upper limit':
                        ampl.getParameter('RecoveryDisutility_OVERBRACE').set(self.RecoveryTimeLimit.value)

                if self.Solver_accordion.selected_index != None:
                    b.button_style='warning'

                    isoptimal = lib.mySolver.Run(ampl)
                    if isoptimal:
                        myAMPL.WriteSolution(lib.myGlobals.solPath, lib.myDirectory.unusedfname(lib.myGlobals.solPath,'newSolution'))  
                        lib.myDirectory.refresh_selSolutions(lib.myGlobals.solPath, self.selSolutions)
                        lib.myDirectory.refresh_selSolutions(lib.myGlobals.solPath, self.selSolution)

                    b.button_style=self.get_button_style(ampl.getValue('solve_result'))
                    tooltip_msg='Size: '+str(int(ampl.getValue('_nvars'))) + ' variables, ' \
                    +  str(int(ampl.getValue('_ncons'))) + ' constraints.' \
                    + "\n" + 'Solve result: \'' + ampl.getValue('solve_result').title() 
#                     + "\n" + 'Solve time: \'' + ampl.eval('display _solve_time;') + '\''
                    b.tooltip = tooltip_msg
                    if os.path.isfile(lib.myGlobals.solPath):
                        self.selSolutions.options = lib.myDirectory.listFilesInDirectory(lib.myGlobals.solPath)
                        self.selSolution.options = lib.myDirectory.listFilesInDirectory(lib.myGlobals.solPath)

                    myAMPL.unfixAllFixes()
                    myAMPL.resetToSnapshot(basesnapshot)

                self.CustomConstraintCheckBox.value = False
               
    btnSolRename = ipywidgets.Button(
        description='Rename',
        disabled=False,
        button_style='info',
        tooltip='Click to rename the selected file',
        icon='')
    
    def on_btnSolRename_clicked(self, b):
        with self.Solver_out:
            self.Solver_out.clear_output()

            if self.InputUpload.value != {}:        
                if self.selSolutions.value == ():
                    print('\033[1m', '\n ------No solution selected------ \n','\033[0m')
                else:
                    if len(self.selSolutions.value)>1:
                        print('\033[1m', '\n ------Select only one file at a time------ \n','\033[0m')
                    else:
                        if self.NameChange.value == '':
                            print('\033[1m', '\n ------Type the new file name ------ \n','\033[0m')
                        else:
                            for fname in lib.myDirectory.listFilesInDirectory(lib.myGlobals.solPath):
                                if self.NameChange.value == fname:
                                    print('\033[1m', f'\n ------Type a new file name. "{self.NameChange.value}" already exist------ \n','\033[0m')
                                    return
                            os.rename(f'{lib.myGlobals.solPath}/{self.selSolutions.value[0]}',
                                      f'{lib.myGlobals.solPath}/{self.NameChange.value}')
                                
                            self.selSolutions.options = lib.myDirectory.listFilesInDirectory(lib.myGlobals.solPath)
                            self.selSolution.options = lib.myDirectory.listFilesInDirectory(lib.myGlobals.solPath)

    btnSolDelete = ipywidgets.Button(    
        description='Delete',
        disabled=False,
        button_style='info',
        tooltip='Click to delete selected solutions',
        icon='')
    
    def on_btnSolDelete_clicked(self, b):
        with self.Solver_out:
            self.Solver_out.clear_output()

            if self.InputUpload.value != {}:        
                if self.selSolutions.value == ():
                    print('\033[1m', '\n ------No solution selected------ \n','\033[0m')
                else:
                    for i in range(len(self.selSolutions.value)):   
                        os.remove(f'{lib.myGlobals.solPath}/{self.selSolutions.value[i]}')

                self.selSolutions.options = lib.myDirectory.listFilesInDirectory(lib.myGlobals.solPath)
                self.selSolution.options = lib.myDirectory.listFilesInDirectory(lib.myGlobals.solPath)

    btnSolSave = ipywidgets.Button(
        description='Save',
        disabled=False,
        button_style='info',
        tooltip='Click to save selected solutions',
        icon='')
    
    def on_btnSolSave_clicked(self, b):
        myAMPL = self.myAMPL
        with self.Solver_out:
            self.Solver_out.clear_output()

            if self.InputUpload.value != {}:
                if self.selSolutions.value == ():
                    print('\033[1m', '\n ------No solution selected------ \n','\033[0m')
                else: 
                    if self.SolutionDirectorySelect.value == '':
                        print('\033[1m', '\n ------Specify the name of the folder where you want to save the solutions------ \n','\033[0m')
                    else:
                        savedsolPath = f'./CaseStudies/SavedSolutions/{self.SolutionDirectorySelect.value}'
                        os.makedirs(savedsolPath, exist_ok=True) 
                        for index in range(len(self.selSolutions.value)):
                            copyfile(f'{lib.myGlobals.solPath}/{self.selSolutions.value[index]}',f'{savedsolPath}/{self.selSolutions.value[index]}')
                        print('\033[1m', '\n ------Selected solutions saved on the following directory:------ \n','\033[0m',savedsolPath)
                        
    btnAlternativeSol = ipywidgets.Button(
        description='Generate Alternatives',
        disabled=False,
        button_style='info',
        tooltip='Click to generate alternative solutions',
        icon='')
    
    def on_btnAlternativeSol_clicked(self, b):
        ampl = self.ampl
        myAMPL = self.myAMPL
        basesnapshot = self.basesnapshot
        
        with self.Solver_out:
            self.Solver_out.clear_output()

            if self.selSolutions.value == ():
                print('\033[1m', '\n ------No solution selected------ \n','\033[0m')
            elif len(self.selSolutions.value)>1: 
                print('\033[1m', '\n ------Select one solution at a time------ \n','\033[0m')
                
            if len(self.selSolutions.value)==1:
                
                myAMPL.ReadSolution(lib.myGlobals.solPath, self.selSolutions.value[0])

                ampl.getParameter('RecoveryDisutility_OVERBRACE').set(ampl.getValue('RecoveryDisutility'))
                ampl.getParameter('EV_TotalCost_OVERBRACE').set((1+self.BudgetRelaxation.value/100)*ampl.getValue('EV_TotalCost_OVERBRACE'))

                ampl.eval('objective MGAObjectiveFxn;')
                
                ampl.eval('let {i in I} mga_coeff_r[i]:=0;')
                ampl.eval('let {(i, p) in IX} mga_coeff_s[i, p]:=0;')
              
                for i in range(self.NumberofAlternatives.value):
                    
                    mga_coeff_r = ampl.getParameter('mga_coeff_r').getValues().toDict()
                    r = ampl.getVariable('r').getValues().toDict()
                    mga_coeff_r = {index: mga_coeff_r[index] + 1*(r[index]>0.001) for index in r.keys()}
                    ampl.getParameter('mga_coeff_r').setValues(mga_coeff_r)
                    
                    mga_coeff_s = ampl.getParameter('mga_coeff_s').getValues().toDict()
                    s = ampl.getVariable('s').getValues().toDict()
                    mga_coeff_s = {index: mga_coeff_s[index] + 1*(s[index]>0.001) for index in s.keys()}
                    ampl.getParameter('mga_coeff_s').setValues(mga_coeff_s)
                    
                    isoptimal = lib.mySolver.Run(ampl)
                    if isoptimal:                    
                        myAMPL.WriteSolution(lib.myGlobals.solPath, self.selSolutions.value[0]+f'_<alternative_{i+1}>')
                        lib.myDirectory.refresh_selSolutions(lib.myGlobals.solPath, self.selSolutions)
                        lib.myDirectory.refresh_selSolutions(lib.myGlobals.solPath, self.selSolution)
                
                myAMPL.unfixAllFixes()
                myAMPL.resetToSnapshot(basesnapshot)
                    
    btnDterministicDisplay = ipywidgets.Button(
        description='Display',
        disabled=False,
        button_style='warning',
        tooltip='Click to display graph',
        icon='pencil')
    
    def on_btnDterministicDisplay_clicked(self, b):
        ampl = self.ampl
        myAMPL = self.myAMPL      
        basesnapshot = self.basesnapshot
        
        Visualize = lib.myVisualization.myVisualization(ampl, basesnapshot)

        with self.Plotter_out:
            self.Plotter_out.clear_output()

            if self.InputUpload.value != {}:        
                if self.selSolutions.value == ():
                    print('\033[1m', '\n ------No solution selected------ \n','\033[0m')
                else:
                    if self.Results_accordion.selected_index == 0:
                        Visualize.TopLevelTable(myAMPL, lib.myGlobals.solPath, self.selSolutions.value)

                    elif self.Results_accordion.selected_index == 1:
                        if self.Stages_tab.selected_index == 0:
                            if self.ChartSelect.value == 'Bar Chart': 
                                if self.selSolutions.value == {}:
                                    print('\033[1m', '\n ------No solution selected------ \n','\033[0m')
                                else:
                                    Visualize.MitigationStageBarChart(myAMPL, lib.myGlobals.solPath, self.selSolutions.value)

                            elif self.ChartSelect.value == 'Graph':
                                if self.selSolutions.value == {}:
                                    print('\033[1m', '\n ------No solution selected------ \n','\033[0m')
                                else:
                                    if self.GraphLayout.value == 'manual' and self.CoordinatesUpload.value == {}:
                                        print('\033[1m', '\n ------No coordinates loaded. Select another layout or upload the coordinates------ \n','\033[0m')
                                    else:
                                        Visualize.MitigationStageGraph(myAMPL, lib.myGlobals.solPath, self.selSolutions.value)

                        elif self.Stages_tab.selected_index == 1:
                            if self.ChartSelect.value == 'Bar Chart':
                                if self.selSolutions.value == {}:
                                    print('\033[1m', '\n ------No solution selected------ \n','\033[0m') 
                                else:
                                    Visualize.RecoveryStageBarChart(myAMPL, lib.myGlobals.solPath, self.selSolutions.value)

                            elif self.ChartSelect.value == 'Graph':
                                if self.selSolutions.value == {}:
                                    print('\033[1m', '\n ------No solution selected------ \n','\033[0m')
                                else:
                                    if self.GraphLayout.value == 'manual' and self.CoordinatesUpload.value == {}:
                                        print('\033[1m', '\n ------No coordinates loaded. Select another layout or upload the coordinates------ \n','\033[0m')
                                    else:
                                        Visualize.RecoveryStageGraph(myAMPL, lib.myGlobals.solPath, self.selSolutions.value)

    btnTradeoffDisplay = ipywidgets.Button(
        description='Display',
        disabled=False,
        button_style='warning',
        tooltip='Click to display trade-off curve',
        icon='pencil')
    
    def on_btnTradeoffDisplay_clicked(self, b):
        ampl = self.ampl
        myAMPL = self.myAMPL
        basesnapshot = self.basesnapshot
        Visualize = lib.myVisualization.myVisualization(ampl, basesnapshot)

        with self.Tradeoff_out:
            self.Tradeoff_out.clear_output()

            if self.InputUpload.value != {}:
                EV_TotalCost        = []
                RecoveryDisutility  = []   
                Number_of_Scenarios = 100

                lib.myBenchmark.DoNothing_Scenario(ampl)
                lib.mySolver.Run(ampl)
                Initial_EV_TotalCost = ampl.getValue('EV_TotalCost') + 0.1

                myAMPL.unfixAllFixes()        

                lib.myBenchmark.UnlimitedBudget_Scenario(ampl)
                lib.mySolver.Run(ampl)
                Final_EV_TotalCost = ampl.getValue('EV_TotalCost')

                EV_TotalCost_Increment = (Final_EV_TotalCost - Initial_EV_TotalCost)/Number_of_Scenarios

                myAMPL.resetToSnapshot(basesnapshot)

                for n in range(Number_of_Scenarios+1):
                    ampl.eval('objective RecoveryDisutilityObjectiveFxn;')
                    ampl.getParameter('EV_TotalCost_OVERBRACE').set(Initial_EV_TotalCost + EV_TotalCost_Increment*n)
                    lib.mySolver.Run(ampl)

                    EV_TotalCost.append(ampl.getValue('EV_TotalCost'))
                    RecoveryDisutility.append(ampl.getValue('RecoveryDisutility'));

                fig = Visualize.GraphViz(EV_TotalCost, RecoveryDisutility, 
                                         myAMPL.getEntityInfo(ampl.getVariable("EV_TotalCost")).ampl_alias, 
                                         myAMPL.getEntityInfo(ampl.getVariable("RecoveryDisutility")).ampl_alias,
                                         "")
                display(fig)

                myAMPL.unfixAllFixes()
                myAMPL.resetToSnapshot(basesnapshot)
    
    btnFragilityUpload = ipywidgets.Button(
        description='Upload',
        disabled=False,
        button_style='warning',
        tooltip='Click to upload the file',
        icon='check')
    
    btnFragilityClear = ipywidgets.Button(
        description='Clear',
        disabled=False,
        button_style='danger',
        tooltip='Click to clear the file',
        icon='')
    
    btnFragilitySet = ipywidgets.Button(
        description='Set',
        disabled=False,
        button_style='info',
        tooltip='Click to set the fragility of the selected components',
        icon='')
    
    def on_btnFragilitySet_clicked(self, b):       
        ampl = self.ampl 
        myAMPL = self.myAMPL 
                
        global failure_probability 
        
        Loading = ampl.getData('L').toDict()        
        failure_probability = {(component, event) : myStats.get_dist_cdf(Loading[component, event], self.ProbDistSelect.value, self.select_dist_mu.value, self.select_dist_sigma.value) \
                               for component in self.fragility_components.value for [event] in ampl.getData('E')}
        
        self.defined_fragilities.options = list(self.defined_fragilities.options) + list(self.fragility_components.value)
        self.fragility_components.options = set(self.fragility_components.options).difference(set(self.fragility_components.value))
        
    btnFragilityDelete = ipywidgets.Button(
        description='Delete',
        disabled=False,
        button_style='danger',
        tooltip='Click to delete selected components',
        icon='')
    
    def on_btnFragilityDelete_clicked(self, b): 
        with self.Uncertainty_out:
            self.Uncertainty_out.clear_output()
            if self.defined_fragilities.value == ():
                print('\033[1m', '\n ------No component selected------ \n','\033[0m')
            else:
                self.fragility_components.options = list(self.fragility_components.options) + list(self.defined_fragilities.value) 
                self.defined_fragilities.options = set(self.defined_fragilities.options).difference(set(self.defined_fragilities.value))
                
    btnFragilityRun = ipywidgets.Button(
        description='Run',
        disabled=False,
        button_style='info',
        tooltip='Click to Run the Uncertainty Analysis',
        icon='')
    
    def on_btnFragilityRun_clicked(self, b):       
        ampl = self.ampl 
        myAMPL = self.myAMPL 
        
        with self.Uncertainty_out:
            self.Uncertainty_out.clear_output()
            
            if self.sampling_method.value == 'Crude Monte Carlo':  
                estimation = np.empty(100)
                for i in range(100):
                    failure_probability = 0.4
                    samples  = {(component, event) : np.where(failure_probability < myStats.get_rand_number(self.sample_size.value, 0, 1), 1, 0) \
                                for component in self.defined_fragilities.options for [event] in ampl.getData('E')}
                    recovery_time = self.f_of_x(self.sample_size.value, samples)
                    estimation[i] = myStats.get_MC_estimate(self.sample_size.value, recovery_time)
                print('MC_estimate =', np.mean(estimation), 'MC_variance =', np.std(estimation)/np.mean(estimation)*100) 

            elif self.sampling_method.value == 'Importance Sampling Monte Carlo':
                num_of_vars = len(['param' for component in self.defined_fragilities.options for [event] in ampl.getData('E')])                      
                estimation = np.empty(100)
                for i in range(100):
                    failure_probability = 0.4
                    samples, recovery_time, acceptance_rate = self.get_MCMC_samples(self.sample_size.value, num_of_vars, failure_probability)
                    probability_of_each_sample = [{(component, event) : np.where(samples[n][component, event] == 0, failure_probability, 1-failure_probability) \
                                                   for component in self.defined_fragilities.options for [event] in ampl.getData('E')} for n in range(self.sample_size.value)]
                    p = [np.prod(list(probability_of_each_sample[n].values())) for n in range(self.sample_size.value)]
                    
                    q = [samples.count(samples[n])/self.sample_size.value for n in range(self.sample_size.value)]
                    
                    weights = [p[n]/q[n] for n in range(self.sample_size.value)] 
                    
                    estimation[i] = np.dot(recovery_time, weights)/self.sample_size.value
#                     estimation[i] = np.dot(recovery_time, weights)/np.sum(weights)
                    
                print('MCMC_estimate = ', np.mean(estimation), 'MCMC_variance = ', np.std(estimation)/np.mean(estimation)*100)
                        
    btnUncertaintySet = ipywidgets.Button(
        description='Set',
        disabled=False,
        button_style='info',
        tooltip='Click to set the uncertainty of the selected components',
        icon='')
    
    def on_btnUncertaintySet_clicked(self, b):               
        ampl = self.ampl 
        myAMPL = self.myAMPL 
        
        with self.Uncertainty_out:
            self.Uncertainty_out.clear_output()         

            uncertainty_upper_bound.update({param : self.uncertainty_UB.value for param in self.uncertainty_params.value})

            self.DefinedUncertainties.options = list(self.DefinedUncertainties.options) + list(self.uncertainty_params.value)
            self.uncertainty_params.options = set(self.uncertainty_params.options).difference(set(self.uncertainty_params.value))
           
    btnUncertaintyRun = ipywidgets.Button(
        description='Run',
        disabled=False,
        button_style='warning',
        tooltip='Click to run the uncertainty analysis',
        icon='')
    
    def on_btnUncertaintyRun_clicked(self, b):
        ampl = self.ampl 
        myAMPL = self.myAMPL
        basesnapshot = self.basesnapshot
        
        global samples
        
        deterministic_values = {param: np.where(np.array([*ampl.getData(param).toDict().values()])!=0, [*ampl.getData(param).toDict().values()], \
                                                0.001) for param in self.DefinedUncertainties.options}
        
        mu = np.concatenate([np.log(deterministic_values[param]) for param in self.DefinedUncertainties.options], axis=None) 
        sigma = np.concatenate([ampl.getData(f'{param}').getNumRows()*[np.log(uncertainty_upper_bound[param]**0.5)] for param in self.DefinedUncertainties.options], axis=None)
  
        with self.Uncertainty_out:
            self.Uncertainty_out.clear_output()
            
            if self.selSolution.value==None:
                print('\033[1m', '\n ------No solution selected------ \n','\033[0m')
            else:
                if self.DefinedUncertainties.options != ():
                    num_of_vars = len(['param' for param in self.DefinedUncertainties.options \
                                       for row in range(ampl.getData(f'{param}').getNumRows())]) 
                    
                    true_value = 2.4550658269582333
                    
                    if self.sampling_method.value == 'Crude Monte Carlo':                     

                        estimation = []
                        for i in range(50):
                            a = time.process_time()
                            samples = myStats.get_MC_samples(self.sample_size.value, mu, sigma)
                            recovery_time = self.f_of_x(self.sample_size.value, samples)
                            b = time.process_time()                 

                            estimation.append(myStats.get_MC_estimate(self.sample_size.value, recovery_time))
#                             variance = myStats.get_MC_variance(self.sample_size.value, recovery_time)
                        bias = np.mean(estimation) - true_value
                        MSE  = np.var(estimation) + bias**2
                        print('Computational_time = ', b-a, 'MC_estimate = ', np.mean(estimation), 'MC_variance = ', np.var(estimation), 'MC_MSE = ', MSE)                    
                    
                    elif self.sampling_method.value == 'Importance Sampling Monte Carlo':
                        
                        a = time.process_time()
                        samples, recovery_time, acceptance_rate = self.get_MCMC_samples(100, num_of_vars, mu, sigma)
                        b = time.process_time()

                        kde = gaussian_kde(np.array(samples).T, bw_method = 'silverman')
                                               
                        estimation = []
                        for i in range(1):
                            kde_samples = kde.resample(self.sample_size.value)
                            recovery_time = self.f_of_x(self.sample_size.value, kde_samples.T)

                            estimation.append(myStats.get_MCMC_IS_estimate(self.sample_size.value, num_of_vars, kde_samples.T, recovery_time, mu, sigma, kde))
#                             variance = myStats.get_MCMC_IS_variance(self.sample_size.value, num_of_vars, kde_samples.T, recovery_time, mu, sigma, kde)
                            
                        bias = np.mean(estimation) - true_value
                        MSE  = np.var(estimation) + bias**2
                        print('Computational_time = ', b-a, 'MCMC_estimate = ', np.mean(estimation), 'MCMC_variance = ', np.var(estimation), 'MCMC_MSE = ', MSE, 'Acceptance Rate = ', acceptance_rate)

                    print('\033[1m', f'\nUncertainty analysis is completed for {self.selSolution.value}\n','\033[0m')
                    print(f'Sampling method: {self.sampling_method.value}')
                    print(f'Number of smaples: {self.sample_size.value}')
                    print('Fragility function is defined for:', end = " ") 
                    print(None) if self.defined_fragilities.options==() else print(*self.defined_fragilities.options, sep = ', ')
                    print('Uncertainty is defined for:', end = " ") 
                    print(None) if self.DefinedUncertainties.options==() else print(*self.DefinedUncertainties.options, sep = ', ')  

                    self.btnUncertaintyRun_grid.children = (ipywidgets.VBox([self.btnUncertaintyDisplay,
                                                                             self.btnUncertaintyDisplay_grid]),)
                else:
                    print('\033[1m', '\n ------No uncertainty defined------ \n','\033[0m')
                
    btnUncertaintyDelete = ipywidgets.Button(
        description='Delete',
        disabled=False,
        button_style='danger',
        tooltip='Click to delete selected components',
        icon='')
    
    def on_btnUncertaintyDelete_clicked(self, b):                      
        with self.Uncertainty_out:
            self.Uncertainty_out.clear_output()
            if self.DefinedUncertainties.value == ():
                print('\033[1m', '\n ------No parameter and component selected------ \n','\033[0m')
            else:
                self.uncertainty_params.options = list(self.uncertainty_params.options) + list(self.DefinedUncertainties.value)
                self.DefinedUncertainties.options = set(self.DefinedUncertainties.options).difference(set(self.DefinedUncertainties.value))
                
    btnUncertaintyDisplay = ipywidgets.ToggleButtons(
        description='Results',
        options=['Top-Level Info', 'Detailed Info', 'Uncertainty Importance'],
        value = None,
        disabled=False,
        button_style='', 
        tooltips=['Display top-level information', 'Display detailed information', 'Display uncertainty importance'])
   
    def handle_btnUncertaintyDisplay_change(self, change):
        ampl = self.ampl
        myAMPL = self.myAMPL      
        basesnapshot = self.basesnapshot
        
        with self.Uncertainty_out:
            self.Uncertainty_out.clear_output()
            if self.btnUncertaintyDisplay.value == 'Top-Level Info': 
                self.btnUncertaintyDisplay_grid.children = ()
                self.display_top_level_uncertainty()
                
            elif self.btnUncertaintyDisplay.value == 'Detailed Info':
                self.btnUncertaintyDisplay_grid.children = (ipywidgets.VBox([ipywidgets.HBox([self.GraphLayout,
                                                                                              self.Coordinates_grid]),
                                                                             ipywidgets.HBox([ipywidgets.Label('Select Variable:',style={'description_width': 'initial'}), 
                                                                                              self.UncertainVarsSelect])]),)
                
                if self.GraphLayout.value == 'manual' and self.CoordinatesUpload.value == {}:
                    print('\033[1m', '\n ------No coordinates loaded. Select another layout or upload the coordinates------ \n','\033[0m')
                else:
                    self.display_detailed_uncertainty()
                    
            elif self.btnUncertaintyDisplay.value == 'Uncertainty Importance':
                self.btnUncertaintyDisplay_grid.children = (ipywidgets.HBox([ipywidgets.Label('Select Variable:',style={'description_width': 'initial'}), 
                                                                             self.TopLevelVarsSelect]),)
                self.display_uncertainty_importance()

    def display_top_level_uncertainty(self):        
        ampl=self.ampl
        myAMPL = self.myAMPL
        
        df_final = pd.DataFrame()
        for param in ['min', 'max', 'mean', 'stdev']:
            df = pd.DataFrame(data=[param], columns=[''])
            for var in lib.myGlobals.TopLevelVars:
                df[myAMPL.getEntityInfo(ampl.getVariable(var)).ampl_alias] = \
                eval(param)(UncertaintyTopResults[myAMPL.getEntityInfo(ampl.getVariable(var)).ampl_alias].tolist())

            if df_final.empty:
                df_final=df
            else:
                df_final=df_final.append(df, ignore_index=True) 

        df = df_final
        df.set_index('', inplace=True) 
        display(df)
                    
    def display_detailed_uncertainty(self):
        ampl = self.ampl
        myAMPL = self.myAMPL
        basesnapshot = self.basesnapshot
        Visualize = lib.myVisualization.myVisualization(ampl, basesnapshot)
                    
        fig, edges, edges_hover, nodes, layouts = Visualize.NetworkViz(Visualize.nxGraph(), self.GraphLayout.value)
        edges = Visualize.dashed_DLNK(edges)                    

        def node_hover_fn(trace, points, selector):
            for index in points.point_inds:    
                pic = go.FigureWidget()

                for E in ampl.getData('E').toList():
                    pic.add_trace(go.Box(
                        y=UncertaintyDetailedResults.loc[(UncertaintyDetailedResults['I'] == ampl.getData('I').toList()[index]) & (UncertaintyDetailedResults['E'] == E)]\
                        [f'{self.UncertainVarsSelect.value}'], name=f"E = {E}"))

                pic.update_layout(
                    xaxis=dict(title='Events', zeroline=False),
                    yaxis=dict(title=f"{self.UncertainVarsSelect.value} of {ampl.getData('I').toList()[index]}", 
                               zeroline=False))

                self.display_detailed_uncertainty_grid.children = (pic,)

        nodes.on_hover(node_hover_fn)

        display(ipywidgets.VBox([fig,
                                 self.display_detailed_uncertainty_grid]))
        
    def display_uncertainty_importance(self):
        ampl = self.ampl
        
        UncertainValue = {}
        correlation = {}
        p_value = {}
         
        i = 0
        for param in self.DefinedUncertainties.options:
            for component in ampl.getData(param).toDict().keys():
                UncertainValue[param, component] = []
                for n in range(self.sample_size.value): 
                    UncertainValue[param, component].append(np.exp(samples[n][i]))
                i+=1

                correlation[param, component], p_value[param, component] = \
                scipy.stats.spearmanr(UncertaintyTopResults.loc[:,self.TopLevelVarsSelect.value].values, UncertainValue[param, component])
        
        S = dict(zip(correlation.keys(), list(zip(correlation.values(), p_value.values()))))
        Selected_corr = dict( (key, abs(corr)) for (key, (corr, p)) in S.items() if abs(corr)>0.3*max(correlation.values()))
        Selected_p_value = dict( (key, p) for (key, (corr, p)) in S.items() if abs(corr)>0.3*max(correlation.values()))

        fig = go.Figure([go.Bar(x=list({str(key): str(value) for key, value in Selected_corr.items()}), 
                                y=list(Selected_corr.values()),
                                text=list(Selected_p_value.values()),
                                texttemplate = '%{text:.4f}',
                                marker=dict(cmax=max(Selected_p_value.values()),
                                            cmin=min(Selected_p_value.values()),
                                            color=list(Selected_p_value.values()),
                                            colorbar=dict(title="p_value"),
                                            colorscale="Viridis"))])
        fig.update_layout(yaxis=dict(title='Spearman Correlation Factor (absolute value)', zeroline=False),
                          barmode='stack', xaxis={'categoryorder':'total descending'})

        fig.show()

    def get_MCMC_samples(self, num_of_samples, num_of_vars, mu, sigma):

        sample = [[0 for var in range(num_of_vars)] for n in range(num_of_samples)]
        function = [0 for n in range(num_of_samples)]

        sample[0] = np.exp(multivariate_normal.rvs(mean=mu, cov=np.diag(np.square(sigma)), size=1))    
        function[0] = self.f_of_x(1, [sample[0]])[0]  
        
        num_of_accepted_samples = 0
        for n in range(1, num_of_samples):           
#             proposal_sigma = ((num_of_samples-n)/num_of_samples)*sigma
            proposal_sigma = (1.3)*sigma
    
            candidate_sample = np.exp(multivariate_normal.rvs(mean=np.log(sample[n-1]), cov=np.diag(np.square(proposal_sigma)), size=1))
            function[n] = self.f_of_x(1, [candidate_sample])[0]
            
            prob_of_previous_sample = multivariate_normal.logpdf(np.log(sample[n-1]), mean=mu, cov=np.diag(np.square(sigma)), allow_singular=True) - np.sum(np.log(sample[n-1]))
            prob_of_candidate_sample = multivariate_normal.logpdf(np.log(candidate_sample), mean=mu, cov=np.diag(np.square(sigma)), allow_singular=True) - np.sum(np.log(candidate_sample))
            
            print('prob_of_previous_sample = ', np.exp(prob_of_previous_sample))
            print('prob_of_candidate_sample = ', np.exp(prob_of_candidate_sample))
            
            prob_of_previous_given_candidate = multivariate_normal.logpdf(np.log(sample[n-1]), mean=np.log(candidate_sample), cov=np.diag(np.square(proposal_sigma)), allow_singular=True) - np.sum(np.log(sample[n-1]))
            prob_of_candidate_given_previous = multivariate_normal.logpdf(np.log(candidate_sample), mean=np.log(sample[n-1]), cov=np.diag(np.square(proposal_sigma)), allow_singular=True) - np.sum(np.log(candidate_sample))
            
            print('prob_of_previous_given_candidate = ', np.exp(prob_of_previous_given_candidate))
            print('prob_of_candidate_given_previous = ', np.exp(prob_of_candidate_given_previous))

            acceptance_ratio_ln = (np.log(function[n]) + prob_of_candidate_sample + prob_of_previous_given_candidate) - (np.log(function[n-1]) + prob_of_previous_sample + prob_of_candidate_given_previous)
            if np.log(myStats.get_rand_number(1, 0, 1)) < acceptance_ratio_ln:
                sample[n] = candidate_sample
                num_of_accepted_samples = num_of_accepted_samples + 1 
            else:
                sample[n] = sample[n-1]
                function[n] = function[n-1]

        samples = sample[:]
        acceptance_rate = num_of_accepted_samples/num_of_samples
        return samples, function, acceptance_rate

    def f_of_x(self, num_of_samples, samples):
        
        ampl = self.ampl
        myAMPL = self.myAMPL
        basesnapshot = self.basesnapshot
        
        global UncertaintyDetailedResults
        global UncertaintyTopResults
        
        myAMPL.ReadSolution(lib.myGlobals.solPath, self.selSolution.value)         
        ampl.eval('objective RecoveryDisutilityObjectiveFxn;')

        ampl.getVariable('r').fix()
        ampl.getVariable('s').fix()
        ampl.getVariable('y_hat').fix()

        UncertaintyTopResults = pd.DataFrame()        
        UncertaintyDetailedResults = pd.DataFrame()
        recovery_time = [0 for n in range(num_of_samples)]
        for n in range(num_of_samples):
            while recovery_time[n] == 0: 
                myAMPL.dropConstraints({'PostEventIntegrity'})

                for fragility_component in self.defined_fragilities.options:
                    for [event] in ampl.getData('E'):
                        ampl.getVariable('y_hat').get([fragility_component, event]).fix(int(y_hat[fragility_component, event][n]))

                i = 0
                for param in self.DefinedUncertainties.options:
                    ampl.getParameter(param).setValues(samples[n][i:i+ampl.getData(param).getNumRows()])
                    i+=ampl.getData(param).getNumRows()
                        
                ampl.getOutput('solve;')
                recovery_time[n] = ampl.getValue('RecoveryDisutility')
                
                [topLevel_df, id_vars] = myAMPL.toPandasTidy('var', 'RecoveryDisutility', set(['RecoveryDisutility']), list(set(lib.myGlobals.TopLevelVars).difference(set(['RecoveryDisutility']))))
                [detailed_df, id_vars] = myAMPL.toPandasTidy('var', 't', set(['t']), list(set(lib.myGlobals.UncertainVars).difference(set(['t']))))

                dict = {var:myAMPL.getEntityInfo(ampl.getVariable(var)).ampl_alias for var in lib.myGlobals.TopLevelVars}
                topLevel_df.rename(columns=dict, inplace=True)

                dict = {var:myAMPL.getEntityInfo(ampl.getVariable(var)).ampl_alias for var in lib.myGlobals.UncertainVars}
                detailed_df.rename(columns=dict, inplace=True)

                topLevel_df['n']=n
                detailed_df['n']=n
                if UncertaintyDetailedResults.empty:
                    UncertaintyTopResults=topLevel_df
                    UncertaintyDetailedResults=detailed_df
                else:
                    UncertaintyTopResults=UncertaintyTopResults.append(topLevel_df, ignore_index=True) 
                    UncertaintyDetailedResults=UncertaintyDetailedResults.append(detailed_df, ignore_index=True) 

        myAMPL.unfixAllFixes()
        myAMPL.resetToSnapshot(basesnapshot)

        return recovery_time

    ## File Upload Widgets
    InputUpload = ipywidgets.FileUpload(accept="", multiple=True, description='Select Files')    
    def handle_InputUpload_change(self, change):
        self.InputFiles.options = [fname for fname in self.InputUpload.value.keys()]       
        #[self.InputUpload.value[i]['name'] for i in range(len(self.InputUpload.value))]

    CoordinatesUpload = ipywidgets.FileUpload(accept='', description='Upload', multiple=True)    
    def handle_CoordinatesUpload_change(self, change):
        if self.CustomConstraintCheckBox.value == True:
            with self.Solver_out:
                self.Solver_out.clear_output() 
                self.add_additional_constraints()
                
    SoVIUpload = ipywidgets.FileUpload(accept="", multiple=True, description='Select File')
    GeoJsonUpload = ipywidgets.FileUpload(accept="", multiple=True, description='Select File')

    ImageUpload = ipywidgets.FileUpload(accept='image/*', description='Upload', multiple=True)    
    def handle_ImageUpload_change(self, change):
        if self.ImagesUploadCheckBox.value == True:
            self.Images_grid.children = (self.ImageUpload,)
        else: 
            self.Images_grid.children = ()
            
    FragilityUpload = ipywidgets.FileUpload(accept="", multiple=True, description='Select Files')  
    
    ## Select Widgets    
    InputFiles = ipywidgets.RadioButtons(
        options=[],
        disabled=False)

    def handle_InputFiles_change(self, change):
        if self.InputUpload.value == {}:
            self.InputSheets.options = []
        else:
            # self.InputSheets.options = [shname for shname in pd.read_excel(io.BytesIO(mainWidgets.InputUpload.value[0].content), None).keys()]
            self.InputSheets.options = [shname for shname in pd.read_excel(self.InputUpload.value[self.InputFiles.value]['content'],None).keys()]
            
    InputSheets = ipywidgets.SelectMultiple(
        options=[],
        value=[],
        disabled=False)     
           
    SystemComponents = ipywidgets.RadioButtons(
        options=[],
        description = ' ',
        disabled=False)

    def handle_SystemComponents_change(self, change):
        ampl=self.ampl
        with self.SystemComponents_out:
            self.SystemComponents_out.clear_output()
        if self.SystemComponents.value == 'Sets':
            self.SystemComponents_grid.children = (self.SetDisplay,)
        elif self.SystemComponents.value == 'Parameters': 
            self.SystemComponents_grid.children = (self.ParamDisplay,)
    
    GraphLayout = ipywidgets.Dropdown(
        options = [],
        disabled = False,
        description='Select Layout:', 
        style = {'description_width': 'initial'}, 
        layout = Layout(display='flex', flex_flow='row', align_items='stretch', width='15%'))

    def handle_GraphLayout_change(self, change):
        if self.GraphLayout.value == 'manual':
            self.Coordinates_grid.children = (self.CoordinatesUpload,)
        else:
            self.Coordinates_grid.children = ()

        if self.GraphLayout.value == 'manual' and self.CoordinatesUpload.value == {}:
            with self.SysGraphDisplay_out:
                self.SysGraphDisplay_out.clear_output()
                print('\033[1m', '\n ------No coordinates loaded. Select another layout or upload the coordinates------ \n','\033[0m')

            if self.CustomConstraintCheckBox.value == True:  
                self.CustomConstraint_grid.children = (ipywidgets.VBox([ipywidgets.HBox([self.GraphLayout,
                                                                                         self.Coordinates_grid])]),)
                with self.Solver_out:
                    print('\033[1m', '\n ------No coordinates loaded. Select another layout or upload the coordinates------ \n','\033[0m') 
                    
            if self.btnUncertaintyDisplay.value == 'Detailed Info':
                with self.Uncertainty_out:
                    self.Uncertainty_out.clear_output()
                    print('\033[1m', '\n ------No coordinates loaded. Select another layout or upload the coordinates------ \n','\033[0m') 
        else:
            with self.SysGraphDisplay_out:
                self.SysGraphDisplay_out.clear_output()
                
            if self.CustomConstraintCheckBox.value == True: 
                with self.Solver_out:
                    self.Solver_out.clear_output()  
                    self.add_additional_constraints()
                
            if self.btnUncertaintyDisplay.value == 'Detailed Info':
                with self.Uncertainty_out:
                    self.Uncertainty_out.clear_output()
                    self.display_detailed_uncertainty()
    
    RecoveryEndPoint = ipywidgets.Dropdown(
        options=[],
        disabled=False)
        
    BenchmarkSol = ipywidgets.RadioButtons(
        options=[], 
        description=' ')
    
    Objfxn = ipywidgets.Dropdown(
        options=[], 
        description='Obj Fxn:')

    def handle_Objfxn_change(self, change):
        if self.Objfxn.value == 'Minimize the EV recovery time':
            self.Constraints.options = ['Total expected costs upper limit']
            self.Constraint_grid.children = (ipywidgets.HBox([ipywidgets.Label('Cost Upper Limit:',style={'description_width': 'initial'}), 
                                                              self.BudgetLimit]),)
        elif self.Objfxn.value == 'Minimize the EV total cost':
            self.Constraints.options = ['Total expected recovery time upper limit']
            self.Constraint_grid.children = (ipywidgets.HBox([ipywidgets.Label('Recovery Time Upper Limit:',style={'description_width': 'initial'}), 
                                                              self.RecoveryTimeLimit]),)  
            
    Constraints = ipywidgets.Dropdown(
        options=[],
        disabled=False, 
        description='Constraints:')

    def handle_Constraints_change(self, change):
        self.CustomConstraintCheckBox.value = False
    
    BudgetLimit = ipywidgets.FloatSlider(
        min=0, max=10000000, value=500000.0, step=10000, readout=True, 
        readout_format='$,', description=' ', style = {'description_width': 'initial'})

    RecoveryTimeLimit = ipywidgets.FloatSlider(
        min=0, max=15, value=1, step=0.1, readout=True, description=' ', style = {'description_width': 'initial'})  
    
    CustomDecisionVar = ipywidgets.RadioButtons(
        options=['Mitigation cost [$]', 'Increase in resistance [ft]'],
        description='Select a variable:',
        disabled=False,
        style = {'description_width': 'initial'}, 
        layout=Layout(display='flex', flex_flow='row', align_items='stretch', width='20%'))

    astatusSelect = ipywidgets.ToggleButtons(
        options=['Fix', 'Bound', 'No restrictions'],
        value = 'No restrictions',
        disabled=False,
        button_style='',
        style = {'description_width': 'initial'})

    def handle_astatusSelect_change(self, change):
        if self.astatusSelect.value == 'Fix':
            self.Bound_grid.children = (self.CustomFixValue,)
        elif self.astatusSelect.value == 'Bound':
            self.Bound_grid.children = (ipywidgets.HBox([self.CustomLb, self.CustomUb]),)
        elif self.astatusSelect.value == 'No restrictions':
            self.Bound_grid.children = ()

    CustomFixValue = ipywidgets.FloatText(
        placeholder='The fix value',
        disabled=False,
        continuous_update=True,
        description='Fix value:',
        style = {'description_width': 'initial'}, 
        layout=Layout(display='flex', flex_flow='row', align_items='stretch', width='10%'))

    CustomLb = ipywidgets.FloatText(
        placeholder='The lower bound',
        disabled=False,
        continuous_update=True,
        description='Lower bound:',
        style = {'description_width': 'initial'}, 
        layout=Layout(display='flex', flex_flow='row', align_items='stretch', width='10%'))

    CustomUb = ipywidgets.FloatText(
        placeholder='The upper bound',
        disabled=False,
        continuous_update=True,
        description='Upper bound:',
        style = {'description_width': 'initial'}, 
        layout=Layout(display='flex', flex_flow='row', align_items='stretch', width='10%'))            
    
    BudgetRelaxation = ipywidgets.IntSlider(
        min=0, max=100, value=10, step=10, 
       description=' ', style = {'description_width': 'initial'})
    
    NumberofAlternatives = ipywidgets.BoundedIntText(
        value=5,
        min=1,
        max=10,
        step=1,
        disabled=False)
    
    SetDisplay = ipywidgets.Dropdown(
        options=[],
        description='Set:',
        disabled=False)
    
    ParamDisplay = ipywidgets.Dropdown(
        options=[],
        description='Parameter:',
        disabled=False)
    
    SolutionDirectorySelect = ipywidgets.Text(
        placeholder='Type something',
        disabled=False)   
    
    ChartSelect = ipywidgets.RadioButtons(
        options=['Bar Chart', 'Graph'],
        description='Chart Type:',
        disabled=False)
    
    MitVarsSelect = ipywidgets.Dropdown(
        options = [],
        disabled = False, 
        description = 'Variable:')
    
    RecoveryVarsSelect = ipywidgets.Dropdown(
        options=[],
        disabled=False, 
        description='Variable:')

    def handle_ChartSelect_change(self, change):
        if self.ChartSelect.value == 'Bar Chart':
            with self.Plotter_out:
                self.Plotter_out.clear_output()
            self.Plotter_grid.children = ( )  
        elif self.ChartSelect.value == 'Graph':
            with self.Plotter_out:
                self.Plotter_out.clear_output()
            self.Plotter_grid.children = (ipywidgets.HBox([self.GraphLayout, 
                                                           self.Coordinates_grid]),)
                        
    fragility_components = ipywidgets.SelectMultiple(
        options=[],
        disabled=False)
    
    FragilityMethodSelect = ipywidgets.RadioButtons(
        options = ['Define a PDF', 'Upload from a file'],
        value = 'Define a PDF',
        disabled = False)    
    
    def handle_FragilityMethodSelect_change(self, change):
        if self.FragilityMethodSelect.value == 'Define a PDF':
            self.Fragility_grid.children = (self.ProbDistSelect,
                                            self.select_dist_mu,
                                            self.select_dist_sigma)
        elif self.FragilityMethodSelect.value == 'Upload from a file':
            self.Fragility_grid.children = (ipywidgets.HBox([self.FragilityUpload, 
                                                             self.btnFragilityUpload, 
                                                             self.btnFragilityClear]),)
    
    ProbDistSelect = ipywidgets.Dropdown(
        description = 'distribution',
        options=['lognorm', 'norm'],
        disabled=False)
    
    select_dist_mu = ipywidgets.FloatText(
        description = 'mu',
        disabled=False,
        continuous_update=True)
    
    select_dist_sigma = ipywidgets.FloatText(
        description = 'sigma',
        disabled=False,
        continuous_update=True) 
    
    defined_fragilities = ipywidgets.SelectMultiple(
        options=[],
        disabled=False) 
    
    sampling_method = ipywidgets.RadioButtons(
        options=['Importance Sampling Monte Carlo', 'Crude Monte Carlo'],
        disabled=False)  
    
    sample_size = ipywidgets.IntText(
        disabled=False,
        value = 100,
        continuous_update=True)
    
    image_widgets = ipywidgets.Image(layout=Layout(height='auto', width='auto'))
    
    ImagesUploadCheckBox = ipywidgets.Checkbox(
        value=False,
        description='Show Images',
        disabled=False,
        indent=False)  
    
    CustomConstraintCheckBox = ipywidgets.Checkbox(
        value=False,
        description='Add additional constraint',
        disabled=False,
        indent=False)

    def handle_CustomConstraintCheckBox_change(self, change):
        ampl = self.ampl
        myAMPL = self.myAMPL
        basesnapshot = self.basesnapshot
        with self.Solver_out: 
            self.Solver_out.clear_output()
            if self.CustomConstraintCheckBox.value == True:          
                if self.GraphLayout.value == 'manual':
                    self.Coordinates_grid.children = (self.CoordinatesUpload,)
                else:
                    self.Coordinates_grid.children = () 

                if self.GraphLayout.value == 'manual' and self.CoordinatesUpload.value == {}:
                    self.CustomConstraint_grid.children = (ipywidgets.HBox([self.GraphLayout,
                                                                            self.Coordinates_grid]),)
                    print('\033[1m', '\n ------No coordinates loaded. Select another layout or upload the coordinates------ \n','\033[0m')
                else:
                    self.add_additional_constraints()
            else: 
                myAMPL.unfixAllFixes()
                myAMPL.resetToSnapshot(basesnapshot)

                self.CustomConstraint_grid.children = ()

    selSolutions = ipywidgets.SelectMultiple(
        description='Solutions:',
        options=[],
        disabled=False)

    selSolution = ipywidgets.Dropdown(
        description='Solutions:',
        options=[],
        disabled=False)
        
    NameChange = ipywidgets.Text(
        disabled=False,
        continuous_update=True)
        
    AllUncertainParamCheckBox = ipywidgets.Checkbox(
        value=False,
        description='Select all parameters',
        disabled=False,
        indent=False)
    
    def handle_AllUncertainParamCheckBox_change(self, change):
        if self.AllUncertainParamCheckBox.value == True:
            self.uncertainty_params.value = self.uncertainty_params.options
        else:
            self.uncertainty_params.value = []
            
    AlternativeSolCheckBox = ipywidgets.Checkbox(
        value=False,
        description='Alternative solutions',
        disabled=False,
        indent=False)
    
    def handle_AlternativeSolCheckBox_change(self, change):
        if self.AlternativeSolCheckBox.value == True:
            self.MGA_grid.children = (ipywidgets.VBox([ipywidgets.HBox([ipywidgets.Label('Budget relaxation (%):',style={'description_width': 'initial'}),
                                                                        self.BudgetRelaxation]),
                                                       ipywidgets.HBox([ipywidgets.Label('Number of alternatives:',style={'description_width': 'initial'}),
                                                                        self.NumberofAlternatives]),
                                                       self.btnAlternativeSol]),)
        else:
            self.MGA_grid.children = []
    
    uncertainty_params = ipywidgets.SelectMultiple(
        options=[],
        value=[],
        disabled=False)
            
    uncertainty_UB = ipywidgets.FloatSlider(
        value=3,
        min=1,
        max=10, 
        step=0.1)
    
    def handle_uncertainty_UB_change(self, change):        
        self.uncertain_param_pdf_grid.children = (self.uncertain_param_pdf(),)
            
    def uncertain_param_pdf(self):
        ampl = self.ampl
        basesnapshot = self.basesnapshot
        Visualize = lib.myVisualization.myVisualization(ampl, basesnapshot)
        
        fig = Visualize.UncertaintyPDF(np.arange(0, 10, 0.0025), 'lognorm', np.log(1), np.log(self.uncertainty_UB.value**0.5)) 
            
        xrange = np.arange(0, 10, 0.0025)
        x = xrange[np.logical_and(xrange>1/self.uncertainty_UB.value, xrange<self.uncertainty_UB.value)]
        y = myStats.get_dist_pdf(x, 'lognorm', np.log(1), np.log(self.uncertainty_UB.value**0.5))
        fig.add_scatter(x=x, y=y, fill='tozeroy', fillcolor = 'rgba(135, 206, 250, 0.5)', mode='lines', line = dict(color='black')) #, fillcolor='rgb(0, 128, 128)'
        
        fig.add_scatter(x=[1,1],
                        y=[0, myStats.get_dist_pdf(1, 'lognorm', np.log(1), np.log(self.uncertainty_UB.value**0.5))], 
                        mode='lines', line=dict(color="black", width=2, dash="dashdot"))
        
        fig.add_annotation(x=1/self.uncertainty_UB.value, y=0,
            text=f'Lowerbound = {1/self.uncertainty_UB.value:.2f} median',
            showarrow=True, arrowhead=1)
        fig.add_annotation(x=self.uncertainty_UB.value, y=0,
            text=f'Upperbound = {self.uncertainty_UB.value:.2f} median',
            showarrow=True, arrowhead=1,
            xanchor="left", yanchor="bottom") 
        fig.add_annotation(x=1, y=myStats.get_dist_pdf(1, 'lognorm', np.log(1), np.log(self.uncertainty_UB.value**0.5)),
            text="median", textangle=0,
            showarrow=False, arrowhead=1,
            xanchor="left", yanchor="bottom")
        fig.update_layout(showlegend=False,
                          xaxis = dict(showline=True, showgrid=False, showticklabels=False, ticks=''))
        
        return fig

    DefinedUncertainties = ipywidgets.SelectMultiple(
        options=[],
        value=[],
        disabled=False) 

    UncertainVarsSelect = ipywidgets.Dropdown(
        disabled=False)
    
    TopLevelVarsSelect = ipywidgets.Dropdown(
        disabled=False)
    
    def handle_TopLevelVarsSelect_change(self, change):
        if self.btnUncertaintyDisplay.value == 'Uncertainty Importance':
            with self.Uncertainty_out:
                self.Uncertainty_out.clear_output()
                self.display_uncertainty_importance()
                  
    ## Output Widgets
    
    Dataset_out = ipywidgets.Output(layout={'border': '1px solid black'})
    
    SystemComponents_out = ipywidgets.Output(layout={'border': '1px solid black'})
        
    SysGraphDisplay_out = ipywidgets.Output(layout={'border': '1px solid black'})
    
    GisMapDisplay_out = ipywidgets.Output(layout={'border': '1px solid black'})
    
    Recovery_out = ipywidgets.Output(layout={'border': '1px solid black'})

    Solver_out = ipywidgets.Output(layout={'border': '1px solid black'})

    Plotter_out = ipywidgets.Output(layout={'border': '1px solid black'})

    Tradeoff_out = ipywidgets.Output(layout={'border': '1px solid black'})
    
    Uncertainty_out = ipywidgets.Output(layout={'border': '1px solid black'})

    ## Grid Box Widgets 

    SystemComponents_grid = ipywidgets.GridBox()
    
    Coordinates_grid = ipywidgets.GridBox([CoordinatesUpload])

    Images_grid = ipywidgets.GridBox()

    Constraint_grid = ipywidgets.GridBox()

    CustomConstraint_grid = ipywidgets.GridBox()

    Bound_grid = ipywidgets.GridBox()
    
    MGA_grid = ipywidgets.GridBox()
    
    Plotter_grid = ipywidgets.GridBox()

    Fragility_grid = ipywidgets.GridBox([ProbDistSelect,
                                         select_dist_mu,
                                         select_dist_sigma])
            
    uncertain_param_pdf_grid = ipywidgets.GridBox()
    
    btnUncertaintyRun_grid = ipywidgets.GridBox()
    
    btnUncertaintyDisplay_grid = ipywidgets.GridBox()
    
    display_detailed_uncertainty_grid = ipywidgets.GridBox()
    
    ## Accordion Widgets

    Dataset_accordion = ipywidgets.Accordion(children=[ipywidgets.HBox([InputUpload, btnInputClear]),
                                                       ipywidgets.VBox([ipywidgets.HBox([ipywidgets.Label('Select File:',style={'description_width': 'initial'}),
                                                                                         InputFiles]),
                                                                        ipywidgets.HBox([ipywidgets.Label('Select Sheet:',style={'description_width': 'initial'}),
                                                                                         InputSheets]),
                                                                        btnInputPreview])])
    Dataset_accordion.set_title(0, 'Select')
    Dataset_accordion.set_title(1, 'Preview')
    
    def handle_Uncertainty_accordion_change(self, change):
        if self.Uncertainty_accordion.selected_index == 3:
            self.uncertain_param_pdf_grid.children = (self.uncertain_param_pdf(),)
    
    Uncertainty_accordion = ipywidgets.Accordion(children=[selSolution, 
                                                           ipywidgets.VBox([ipywidgets.HBox([ipywidgets.Label('Sampling method:',style={'description_width': 'initial'}),
                                                                                             sampling_method]),
                                                                            ipywidgets.HBox([ipywidgets.Label('Sample size:',style={'description_width': 'initial'}),
                                                                                             sample_size])]),
                                                           ipywidgets.VBox([ipywidgets.HBox([ipywidgets.Label('Select components:',style={'description_width': 'initial'}),
                                                                                             fragility_components]),
                                                                            ipywidgets.HBox([ipywidgets.Label('How to define the fragilities:',style={'description_width': 'initial'}),
                                                                                             FragilityMethodSelect]),
                                                                            Fragility_grid,
                                                                            btnFragilitySet,
                                                                            btnFragilityRun,
                                                                            ipywidgets.HBox([ipywidgets.HBox([ipywidgets.Label('Defined fragilities:',style={'description_width': 'initial'}),
                                                                                                              defined_fragilities]),
                                                                                             btnFragilityDelete])]),
                                                           ipywidgets.VBox([ipywidgets.HBox([ipywidgets.Label('Select parameters:',style={'description_width': 'initial'}),
                                                                                                              uncertainty_params]),
                                                                            AllUncertainParamCheckBox,
                                                                            ipywidgets.VBox([ipywidgets.HBox([ipywidgets.Label('Select upperbound multiplicative factor:',style={'description_width': 'initial'}),
                                                                                                              uncertainty_UB]),
                                                                                             uncertain_param_pdf_grid]),
                                                                            btnUncertaintySet,
                                                                            ipywidgets.HBox([ipywidgets.Label('Defined uncertainties:',style={'description_width': 'initial'}),
                                                                                             DefinedUncertainties,
                                                                                             btnUncertaintyDelete])])])
    Uncertainty_accordion.set_title(0, 'Select Solution')
    Uncertainty_accordion.set_title(1, 'Sampling Method')
    Uncertainty_accordion.set_title(2, 'Fragilities')
    Uncertainty_accordion.set_title(3, 'Uncertainties')

    Solver_accordion = ipywidgets.Accordion(children=[BenchmarkSol,
                                                      ipywidgets.VBox([Objfxn,
                                                                       ipywidgets.HBox([Constraints,
                                                                                        Constraint_grid]),
                                                                       CustomConstraintCheckBox,
                                                                       CustomConstraint_grid])])
    
    Solver_accordion.set_title(0, 'Benchmark Solution')
    Solver_accordion.set_title(1, 'Custom Solution')

    Stages_tab = ipywidgets.Tab(style = {'description_width': 'initial'}) 
    Stages_tab.children = [ipywidgets.VBox([ChartSelect,
                                            Plotter_grid,
                                            MitVarsSelect,
                                            selSolutions]), 
                           ipywidgets.VBox([ChartSelect,
                                            Plotter_grid,
                                            RecoveryVarsSelect,
                                            selSolutions])]

    Stages_tab.set_title(0, 'Mitigation')
    Stages_tab.set_title(1, 'Recovery')

    Results_accordion = ipywidgets.Accordion(children=[selSolutions,
                                                       Stages_tab])
    Results_accordion.set_title(0, 'Top Level Info')
    Results_accordion.set_title(1, 'Detailed Info')
    
    ## Tab Widgets

    Dataset_tab = ipywidgets.VBox([Dataset_accordion,
                                   btnInputUpload,
                                   Dataset_out])

    SysComponent_tab = ipywidgets.VBox([ipywidgets.HBox([ipywidgets.Label('Select System Component:', style={'description_width': 'initial'}),
                                                         SystemComponents]),
                                        SystemComponents_grid,
                                        btnSysComponentDisplay,
                                        SystemComponents_out])

    SysGraph_tab = ipywidgets.VBox([ipywidgets.HBox([GraphLayout, 
                                                     Coordinates_grid]),
                                    ipywidgets.HBox([ImagesUploadCheckBox, 
                                                     Images_grid]),
                                    btnSysGraphDisplay,
                                    SysGraphDisplay_out])
    
    GisMap_tab = ipywidgets.VBox([ipywidgets.HBox([ipywidgets.Label('Select City Blocks SoVI Excel File:', style={'description_width': 'initial'}),
                                                   SoVIUpload]),
                                  ipywidgets.HBox([ipywidgets.Label('Select City Blocks GeoJson File:', style={'description_width': 'initial'}),
                                                   GeoJsonUpload]),
                                  btnGisMapDisplay,
                                  GisMapDisplay_out])

    Recovery_tab = ipywidgets.VBox([ipywidgets.HBox([ipywidgets.Label('Select Recovey End Point:', style={'description_width': 'initial'}),
                                                     RecoveryEndPoint]),
                                    btnRecoveryEndPointSet,
                                    Recovery_out])

    Solver_tab = ipywidgets.VBox([Solver_accordion,
                                  btnSolve,
                                  ipywidgets.HBox([selSolutions,
                                                   ipywidgets.VBox([ipywidgets.HBox([btnSolRename,
                                                                                     ipywidgets.Label('Type new name:',style={'description_width': 'initial'}),
                                                                                     NameChange]),
                                                                    btnSolDelete,
                                                                    ipywidgets.HBox([btnSolSave, 
                                                                                     ipywidgets.HBox([ipywidgets.Label('Specify the name of the folder where you want to save the solutions:',style={'description_width': 'initial'}),
                                                                                                      SolutionDirectorySelect])])])]),
                                  AlternativeSolCheckBox,
                                  MGA_grid,
                                  Solver_out])                           

    DeterministicResults_tab = ipywidgets.VBox([Results_accordion,
                                                btnDterministicDisplay,
                                                Plotter_out])  

    Tradeoff_tab = ipywidgets.VBox([btnTradeoffDisplay,
                                    Tradeoff_out]) 
    
    UncertaintyAnalysis_tab = ipywidgets.VBox([Uncertainty_accordion,
                                               btnUncertaintyRun,
                                               btnUncertaintyRun_grid,
                                               Uncertainty_out])

    Understand_the_Situation = ipywidgets.Tab(style = {'description_width': 'initial'}) 
    Understand_the_Situation.children = [Dataset_tab, SysComponent_tab, SysGraph_tab, GisMap_tab]
    Understand_the_Situation.set_title(0, 'Input Dataset')
    Understand_the_Situation.set_title(1, 'System Components')
    Understand_the_Situation.set_title(2, 'System Dependency')
    Understand_the_Situation.set_title(3, 'GIS Map')

    Interactive_Solver = ipywidgets.Tab(style = {'description_width': 'initial'}) 
    Interactive_Solver.children = [Recovery_tab, Solver_tab, DeterministicResults_tab]
    Interactive_Solver.set_title(0, 'Define Recovery')
    Interactive_Solver.set_title(1, 'Run Solver')
    Interactive_Solver.set_title(2, 'Results')

    Tools = ipywidgets.Tab(style = {'description_width': 'initial'}) 
    Tools.children = [Tradeoff_tab, UncertaintyAnalysis_tab]
    Tools.set_title(0, 'Trade-off Curve')
    Tools.set_title(1, 'Uncertainty Analysis')
    
    # Widgets Functions

    def add_additional_constraints(self): 
        ampl = self.ampl
        myAMPL = self.myAMPL
        basesnapshot = self.basesnapshot
        Visualize = lib.myVisualization.myVisualization(ampl, basesnapshot)

        if self.CustomConstraintCheckBox.value == True:
            fig, edges, edges_hover, nodes, layouts = Visualize.NetworkViz(Visualize.nxGraph(), self.GraphLayout.value)
            edges = Visualize.dashed_DLNK(edges)
            nodes.marker.colorbar = None
            nodes.marker.showscale = False
            nodes.marker.color = ['skyblue']*len(Visualize.nxGraph().nodes()) 

            def node_click_fn(trace, points, selector):
                with self.Solver_out:
                    color = list(nodes.marker.color)
                    size = list(nodes.marker.size)

                    for index in points.point_inds:
                        color[index] = 'red'
                        size[index] = 35

                        node = ampl.getData('I').toList()[index]

                        if self.astatusSelect.value == 'Fix':
                            for i, e in ampl.getVariables():
                                if self.CustomDecisionVar.value == ampl.getValue('alias(' + e.name() + ')'):                                
                                    if myAMPL.isDefinitionalVariable(e): 
                                        ampl.eval(f'let MCLIMIT_lb["{node}"]:={self.CustomFixValue.value};')
                                        ampl.eval(f'let MCLIMIT_ub["{node}"]:={self.CustomFixValue.value + 0.00001};')
                                    else:                                        
                                        ampl.getVariable(f'{e.name()}').get(node).fix(self.CustomFixValue.value)

                            with fig.batch_update():
                                nodes.marker.color = color
                                nodes.marker.size = size
                            print('\033[1m', f'\n ------The {self.CustomDecisionVar.value} for {node} is fixed to be {self.CustomFixValue.value}------ \n','\033[0m')

                        elif self.astatusSelect.value == 'Bound':
                            for i, e in ampl.getVariables():
                                if self.CustomDecisionVar.value == ampl.getValue('alias(' + e.name() + ')'):
                                    if self.CustomDecisionVar.value == 'Mitigation cost [$]':
                                        ampl.eval(f'let MCLIMIT_lb["{node}"]:={self.CustomLb.value};')
                                        ampl.eval(f'let MCLIMIT_ub["{node}"]:={self.CustomUb.value};')
                                    elif self.CustomDecisionVar.value == 'Increase in resistance [ft]':
                                        ampl.eval(f'let RLIMIT_lb["{node}"]:={self.CustomLb.value};')
                                        ampl.eval(f'let RLIMIT_ub["{node}"]:={self.CustomUb.value};')

                            with fig.batch_update():
                                nodes.marker.color = color
                                nodes.marker.size = size

                            print('\033[1m', f'\n ------The {self.CustomDecisionVar.value} for {node} is set to be in ({self.CustomLb.value}, {self.CustomUb.value}) range------ \n','\033[0m')

                        elif self.astatusSelect.value == 'No restrictions':
                            for i, e in ampl.getVariables():
                                if self.CustomDecisionVar.value == ampl.getValue('alias(' + e.name() + ')'):
                                    if ampl.getVariable(f'{e.name()}').get(node).astatus() == 'fix':
                                        ampl.getVariable(f'{e.name()}').get(node).unfix()
                                    else:
                                        if self.CustomDecisionVar.value == 'Mitigation cost [$]':
                                            ampl.eval(f'let MCLIMIT_lb["{node}"]:={0};')
                                            ampl.eval(f'let MCLIMIT_ub["{node}"]:={"Infinity"};')
                                        elif self.CustomDecisionVar.value == 'Increase in resistance [ft]':
                                            ampl.eval(f'let RLIMIT_lb["{node}"]:={0};')
                                            ampl.eval(f'let RLIMIT_ub["{node}"]:={ampl.getData("R_OVERBRACE").toDict()[node]};')

                                    color[index] = 'skyblue'
                                    size[index] = 35
                            with fig.batch_update():
                                nodes.marker.color = color
                                nodes.marker.size = size
                            print('\033[1m', f'\n ------There is no restriction for {node}------ \n','\033[0m') 

            nodes.on_click(node_click_fn)

            self.CustomConstraint_grid.children = (ipywidgets.VBox([ipywidgets.HBox([self.GraphLayout,
                                                                                     self.Coordinates_grid]),
                                                                    self.CustomDecisionVar,
                                                                    self.astatusSelect,
                                                                    self.Bound_grid,
                                                                    fig]),)
       
    def get_button_style(self, r):
        if r == 'solved':
            return 'success'
        elif r == 'solved?':
            return 'warning'
        elif r == 'infeasible':
            return 'danger'
        elif r == 'unbounded':
            return 'danger'
        elif r == 'limit':
            return 'danger'
        elif r == 'failure':
            return 'danger'
        else:
            return 'danger'
        

    def Events(self):        
        self.GraphLayout.observe(self.handle_GraphLayout_change, names='value')
        self.InputFiles.observe(self.handle_InputFiles_change, names='value')
        self.Constraints.observe(self.handle_Constraints_change, names='value')
        self.InputUpload.observe(self.handle_InputUpload_change, names='value')
        self.Objfxn.observe(self.handle_Objfxn_change, names='value')
        self.SystemComponents.observe(self.handle_SystemComponents_change, names='value')
        self.CustomConstraintCheckBox.observe(self.handle_CustomConstraintCheckBox_change, names='value')
        self.CoordinatesUpload.observe(self.handle_CoordinatesUpload_change, names='value')
        self.astatusSelect.observe(self.handle_astatusSelect_change, names='value')
        self.ImagesUploadCheckBox.observe(self.handle_ImageUpload_change, names='value')
        self.ChartSelect.observe(self.handle_ChartSelect_change, names='value')
        self.AlternativeSolCheckBox.observe(self.handle_AlternativeSolCheckBox_change, names='value')
        self.FragilityMethodSelect.observe(self.handle_FragilityMethodSelect_change, names='value')
        self.AllUncertainParamCheckBox.observe(self.handle_AllUncertainParamCheckBox_change, names='value')
        self.btnUncertaintyDisplay.observe(self.handle_btnUncertaintyDisplay_change, names='value')
        self.uncertainty_UB.observe(self.handle_uncertainty_UB_change, names='value')
        self.Uncertainty_accordion.observe(self.handle_Uncertainty_accordion_change, names='selected_index')
        self.TopLevelVarsSelect.observe(self.handle_TopLevelVarsSelect_change, names='value')        
                
        self.btnInputUpload.on_click(self.on_btnInputUpload_clicked)
        self.btnInputClear.on_click(self.on_btnInputClear_clicked)
        self.btnInputPreview.on_click(self.on_btnInputPreview_clicked)
        self.btnSysComponentDisplay.on_click(self.on_btnSysComponentDisplay_clicked)
        self.btnSysGraphDisplay.on_click(self.on_btnSysGraphDisplay_clicked)
        self.btnGisMapDisplay.on_click(self.on_btnGisMapDisplay_clicked)
        self.btnRecoveryEndPointSet.on_click(self.on_btnRecoveryEndPointSet_clicked)
        self.btnSolve.on_click(self.on_btnSolve_clicked)
        self.btnSolRename.on_click(self.on_btnSolRename_clicked)
        self.btnSolDelete.on_click(self.on_btnSolDelete_clicked)
        self.btnSolSave.on_click(self.on_btnSolSave_clicked)
        self.btnAlternativeSol.on_click(self.on_btnAlternativeSol_clicked)
        self.btnDterministicDisplay.on_click(self.on_btnDterministicDisplay_clicked)
        self.btnTradeoffDisplay.on_click(self.on_btnTradeoffDisplay_clicked)
        self.btnFragilitySet.on_click(self.on_btnFragilitySet_clicked)
        self.btnFragilityRun.on_click(self.on_btnFragilityRun_clicked)
        self.btnUncertaintySet.on_click(self.on_btnUncertaintySet_clicked)
        self.btnUncertaintyRun.on_click(self.on_btnUncertaintyRun_clicked)
        self.btnFragilityDelete.on_click(self.on_btnFragilityDelete_clicked)
        self.btnUncertaintyDelete.on_click(self.on_btnUncertaintyDelete_clicked)
        
