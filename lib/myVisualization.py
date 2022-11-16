
from lib.PythonSetup import *
import lib.myGlobals
from lib.myWidgets import mainWidgets
import lib.myStats

class myVisualization:
    def __init__(self, ampl, basesnapshot):
        self.ampl=ampl
        self.basesnapshot=basesnapshot
        
    def dvbar(self, myAMPL, datapath, lstSols, meltvars, meltvar_name, meltvalue_name, **kwargs):        
        basesnapshot = self.basesnapshot
        
        other_vars=[]
        set_vars=set()
        set_sets=set() # not used; just for clarity
        set_params=set() # not used; just for clarity
        for arg in kwargs.values():
            #differentiate a set or variable from a list; set/variable can be x,y,color,... but not list
            #list may be hover_data
            if type(arg) is not list:
                if myAMPL.isEntity(arg):
                    if myAMPL.isVariable(arg):
                        set_vars.add(arg)
                    elif myAMPL.isSet(arg):
                        set_sets.add(arg)
                    elif myAMPL.isParameter(arg):
                        set_params.add(arg)
            else:
                for item in arg:
                    if myAMPL.isEntity(item):
                        if myAMPL.isVariable(item):
                            set_vars.add(item)
                        elif myAMPL.isSet(item):
                            set_sets.add(item)
                        elif myAMPL.isParameter(item):
                            set_params.add(item)
        for arg in kwargs:
            if arg=="hover_data":
                other_vars=set(kwargs.get('hover_data'))
        value_vars=set_vars.union(set_params)
        facet_col=lstSols[0]
        separator=','
        [df, id_vars]=myAMPL.toPandasTidy_append(datapath, lstSols, basesnapshot, meltvar_name, meltvalue_name, set(meltvars), other_vars)    

        f=px.bar(df,**kwargs)
        if kwargs['x']==None: 
            f.update_xaxes(showticklabels=False)
        return f

    def GraphViz(self, x, y, xaxis_title, yaxis_title, title):

        fig = go.FigureWidget()
        fig.add_trace(go.Scatter(x = x, y = y,
                                 mode='lines+markers',
                                 hovertemplate =
                                 '<b>%{xaxis.title.text}</b> : %{x}<br>'
                                 '<b>%{yaxis.title.text}</b> : %{y}'
                                 '<extra></extra>'))
        fig.update_layout(
            title={'text': title},
            xaxis_title = xaxis_title,
            yaxis_title = yaxis_title)

        return fig

    # Network Graph Layout Function
    def GraphLayout(self, G, layout):
        ampl=self.ampl
        if layout == 'manual':
            Lat  = pd.read_excel(mainWidgets.CoordinatesUpload.value['Coordinates.xlsx']['content'],'Lat',index_col=0)
            Long = pd.read_excel(mainWidgets.CoordinatesUpload.value['Coordinates.xlsx']['content'],'Long',index_col=0)
            pos = dict(zip([I for I in ampl.getData('I').toList()], [[Lat.Lat[index], Long.Long[index]] for index, I in enumerate(ampl.getData('I'))]))
            return pos
        elif layout=='dot':     
            pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot', args='-Grankdir=LR')
            return pos         
        elif layout=='circular':     
            pos = nx.circular_layout(G)
            return pos 
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G, weight=1, scale=2)
            return pos  
        elif layout=='random':
            pos = nx.random_layout(G)
            return pos 
        elif layout=='shell':
            pos = nx.shell_layout(G)
            return pos 
        elif layout == 'spring':
            pos = nx.fruchterman_reingold_layout(G, k=0.15, weight=1)
            return pos 
        elif layout == 'spectral':
            pos = nx.spectral_layout(G, scale=1, weight=1)
            return pos 
        elif layout=='spiral':
            pos = nx.spiral_layout(G)
            return pos 

    # Network Graph Visualization Function
    def NetworkViz(self, G, layout):  
        ampl = self.ampl
        pos  = self.GraphLayout(G, layout)

        edge_traces = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace = go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode='lines',
                line=dict(color='black', width=1),
                opacity=0.8,
                customdata=[(edge[0], edge[1])],
                showlegend=False,
                legendgroup="LNK", 
                name="LNK")
            edge_traces.append(edge_trace)

        node_trace = go.Scatter(
            x=[pos[node][0] for node in G.nodes()],
            y=[pos[node][1] for node in G.nodes()],
            mode='markers+text',
            marker=dict(
                opacity=[1]*len(G.nodes()),
                color=['skyblue']*len(G.nodes()),
                size=[35]*len(G.nodes())),
            text=list(G.nodes()),
            textfont=dict(family='Times New Roman', size=12, color='black'),
            textposition='middle center',
            hovertext=list(G.nodes()),
            hovertemplate='%{hovertext}<extra></extra>',
            showlegend=False)

        edge_hover_trace = go.Scatter(
            x=[],
            y=[],
            mode='text',
            text=[],
            textfont=dict(family='Times New Roman', size=12, color='black'),
            textposition='top center',
            hovertemplate='<extra></extra>',
            showlegend=False)

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_hover_trace['x']+=(0.25*(x0+3*x1),)
            edge_hover_trace['y']+=(0.25*(y0+3*y1),)

        edge_labels = []
        for edge in list(G.edges()):
            try:
                edge_labels += (G[edge[0]][edge[1]]['weight'],)
            except:
                edge_labels += ('',) 
        edge_hover_trace['text']=[edge for edge in edge_labels] 

        layout=go.Layout(
            titlefont=dict(size=20), font_family= 'Balto', autosize=True, 
            plot_bgcolor="white",
            showlegend=True, 
            legend=dict(yanchor="top",
                        xanchor="right",
                        bgcolor="white",
                        bordercolor="Black",
                        borderwidth=2),
            xaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=False),
            yaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=False),
            margin=dict(l=10, r=10, b=10, t=10),
            annotations = [
                dict(ax=0.25*(1.5*pos[edge[0]][0]+2.5*pos[edge[1]][0]),
                     ay=0.25*(1.5*pos[edge[0]][1]+2.5*pos[edge[1]][1]),
                     axref='x', ayref='y',
                     x=0.25*(pos[edge[0]][0]+3*pos[edge[1]][0]), 
                     y=0.25*(pos[edge[0]][1]+3*pos[edge[1]][1]), 
                     xref='x', yref='y',
                     showarrow=True, arrowhead=3, arrowsize=3, opacity=0.5) for edge in G.edges()])

        fig = go.FigureWidget(data=[node_trace, edge_hover_trace] + edge_traces, layout=layout)

        nodes = fig.data[0]
        edges_hover = fig.data[1]
        edges = fig.data[2:]
        Layout = fig.layout

        return fig, edges, edges_hover, nodes, Layout

    def nxGraph(self):
        ampl=self.ampl
        G = nx.DiGraph()
        if mainWidgets.InputUpload.value != {}:
            G.add_nodes_from(ampl.getData('I').toList()) 
            G.add_weighted_edges_from(ampl.getData('LNK').toList())
            G.add_edges_from(ampl.getData('DLNK').toList())
        return G

    def node_hover_df(self, ind):  
        ampl=self.ampl
        basesnapshot=self.basesnapshot
        df = pd.DataFrame()
        Description = {}
        for p in basesnapshot.ParameterNamesAsSet:
            try:
                df[p]=[ampl.getData(f"{{i in I : i==\'{node}\'}} {p}[i]").toList()[0][1] for node in self.nxGraph().nodes()]
                Description[p]=ampl.getValue('alias(' + p + ')')
            except:
                continue 
        df.index = list(self.nxGraph().nodes())
        node_hover_df = pd.concat([pd.DataFrame([Description], index=['Description']), pd.DataFrame(df.iloc[ind]).transpose()])
        return node_hover_df

    def edge_hover_df(self, ind):
        ampl=self.ampl
        df = pd.DataFrame()
        Description = {}
        for p in ['CVARQ', 'Q_OVERBRACE']:
            x=[]
            for edge in self.nxGraph().edges():
                try:
                    x+=(ampl.getData(f"{{(i_arc,i,p) in LNK : i_arc==\'{edge[0]}\' && i==\'{edge[1]}\'}} {p}[i_arc,i,p]").toList()[0][3],)
                    Description[p]=ampl.getValue('alias(' + p + ')')
                except TypeError:
                    x+=('-',)
            df[p]=x
        df.index = list(self.nxGraph().edges())
        edge_hover_df = pd.concat([pd.DataFrame([Description], index=['Description']), pd.DataFrame(df.iloc[ind]).transpose()], ignore_index=False)
        return edge_hover_df

    def dashed_DLNK(self, edges):
        ampl=self.ampl
        LNKshowlegend = True
        DLNKshowlegend = True

        for index, edge in enumerate(self.nxGraph().edges()):
            isLNK = True
            for DLNK in ampl.getData('DLNK').toList():
                if (edge[0], edge[1])==DLNK:
                    edges[index].line=dict(color='black', dash='dashdot', width=0.9)
                    isLNK = False
                    if DLNKshowlegend:
                        edges[index].showlegend=True
                        edges[index].name='DLNK'
                        DLNKshowlegend = False 
                    break

            if LNKshowlegend:
                if isLNK:
                    edges[index].showlegend=True
                    edges[index].name='LNK'
                    LNKshowlegend = False  
        return edges

    def TopLevelTable(self, myAMPL, datapath, lstSols):
        ampl=self.ampl
        basesnapshot = self.basesnapshot
        
        df_Sol = pd.DataFrame()
        for Solution in range(len(lstSols)):
            myAMPL.ReadSolution(datapath, lstSols[Solution])
            df = pd.DataFrame(data=[lstSols[Solution]], columns=['Solution'])
            for var in lib.myGlobals.TopLevelVars:
                df_var = myAMPL.getData(f'{var}')
                df_var.dropna(inplace = True)
                df[f'{var}' + '\n' + '(' + myAMPL.getEntityInfo(ampl.getVariable(f'{var}')).units + ')'] = df_var  

            if df_Sol.empty:
                df_Sol=df
            else:
                df_Sol=df_Sol.append(df, ignore_index=True) 
        df = df_Sol
        
        df.set_index('Solution', inplace=True) 
        display(df.style.bar(axis=0, color='#d65f5f'))
    
        myAMPL.unfixAllFixes()
        myAMPL.resetToSnapshot(basesnapshot)

    def MitigationStageBarChart(self, myAMPL, datapath, lstSols):
        ampl=self.ampl
        meltvalue_name = myAMPL.getEntityInfo(ampl.getVariable(mainWidgets.MitVarsSelect.value)).ampl_alias
        pic=self.dvbar(myAMPL, datapath, lstSols, [mainWidgets.MitVarsSelect.value], "Variable", meltvalue_name,
                       x=None, y=meltvalue_name, facet_col="Solution", hover_name="I", color="I")
        display(pic)

    def RecoveryStageBarChart(self, myAMPL, datapath, lstSols):
        ampl=self.ampl
        meltvalue_name = myAMPL.getEntityInfo(ampl.getVariable(mainWidgets.RecoveryVarsSelect.value)).ampl_alias
        pic=self.dvbar(myAMPL, datapath, lstSols, [mainWidgets.RecoveryVarsSelect.value], "Variable", meltvalue_name, 
                  x=None, y=meltvalue_name, facet_col="Solution", hover_name="I", color="I",                   
                  animation_frame="E", animation_group="I")

        display(pic)

    def MitigationStageGraph(self, myAMPL, datapath, lstSols):
        ampl=self.ampl
        basesnapshot = self.basesnapshot
        
        [df,id_vars] = myAMPL.toPandasTidy_append(datapath, lstSols, basesnapshot,
                                                  "Variable", mainWidgets.MitVarsSelect.value, 
                                                  set([mainWidgets.MitVarsSelect.value]), 
                                                  list(set(mainWidgets.MitVarsSelect.options).difference(set([mainWidgets.MitVarsSelect.value]))))
        pos = self.GraphLayout(self.nxGraph(), mainWidgets.GraphLayout.value)
        Coordinates = pd.DataFrame.from_dict(pos, orient='index', columns=['Lat', 'Long'])
        Coordinates = Coordinates.reindex(index = myAMPL.getData('MitigationCostByNode').index.tolist())

        Lat = pd.concat([Coordinates.iloc[:,0]] * len(lstSols) , axis=0)
        Long = pd.concat([Coordinates.iloc[:,1]] * len(lstSols) , axis=0)

        pic = px.scatter(df, 
                         x=Lat, y=Long, 
                         text="I", 
                         hover_name="I", 
                         facet_col="Solution", 
                         color=mainWidgets.MitVarsSelect.value, range_color=[df[mainWidgets.MitVarsSelect.value].min(), df[mainWidgets.MitVarsSelect.value].max()], 
                         opacity=0.5,
                         labels={mainWidgets.MitVarsSelect.value: myAMPL.getEntityInfo(ampl.getVariable(mainWidgets.MitVarsSelect.value)).ampl_alias}) 

        pic.update_traces(marker=dict(size=20))
        pic.update_xaxes(title='', showgrid=False, zeroline=False, showticklabels=False)
        pic.update_yaxes(title='', showgrid=False, zeroline=False, showticklabels=False)

        fig, edges, edges_hover, nodes, layouts = self.NetworkViz(self.nxGraph(), mainWidgets.GraphLayout.value)
        edges = self.dashed_DLNK(edges)
        for index in range(len(edges)):
            for row_idx, row_pics in enumerate(pic._grid_ref):
                for col_idx, col_pic in enumerate(row_pics):
                    edges[index].showlegend=False
                    pic.add_trace(edges[index], row=row_idx+1, col=col_idx+1)

        display(pic)

    def RecoveryStageGraph(self, myAMPL, datapath, lstSols):
        ampl=self.ampl
        basesnapshot = self.basesnapshot
        [df, id_vars]=myAMPL.toPandasTidy_append(datapath, lstSols, basesnapshot, 'Variable', 
                                                  mainWidgets.RecoveryVarsSelect.value, 
                                                  set([mainWidgets.RecoveryVarsSelect.value]), 
                                                  list(set(mainWidgets.RecoveryVarsSelect.options).difference(set([mainWidgets.RecoveryVarsSelect.value]))))

        pos = self.GraphLayout(self.nxGraph(), mainWidgets.GraphLayout.value)
        Coordinates = pd.DataFrame.from_dict(pos, orient='index', columns=['Lat', 'Long'])
        Coordinates = Coordinates.reindex(index = myAMPL.getData('MitigationCostByNode').index.tolist())
        Lat = pd.concat([Coordinates.iloc[:,0]] * len(lstSols), axis=0)
        Long = pd.concat([Coordinates.iloc[:,1]] * len(lstSols), axis=0)

        pic = px.scatter(df, 
                         x=Lat.repeat(len(ampl.getData('E').toList())), 
                         y=Long.repeat(len(ampl.getData('E').toList())), 
                         text="I", 
#                          symbol="y_hat", symbol_sequence=['circle', 'square'], symbol_map={0:'circle', 1:'square'},
                         animation_frame="E", animation_group="I", 
                         hover_name="I",
                         color=mainWidgets.RecoveryVarsSelect.value, range_color=[df[mainWidgets.RecoveryVarsSelect.value].min(), df[mainWidgets.RecoveryVarsSelect.value].max()], 
                         facet_col="Solution",
                         opacity=0.5,
                         labels={mainWidgets.RecoveryVarsSelect.value: myAMPL.getEntityInfo(ampl.getVariable(mainWidgets.RecoveryVarsSelect.value)).ampl_alias}
                        )

        pic.update_traces(marker=dict(size=20))
        pic.update_xaxes(title='', showgrid=False, zeroline=False, showticklabels=False)
        pic.update_yaxes(title='', showgrid=False, zeroline=False, showticklabels=False)
        pic.update_layout(legend=dict(
            y=-0.25,
            x=1))

        fig, edges, edges_hover, nodes, layouts = self.NetworkViz(self.nxGraph(), mainWidgets.GraphLayout.value)
        edges = self.dashed_DLNK(edges)

        for index in range(len(edges)):
            edges[index].showlegend=False
            for row_idx, row_pics in enumerate(pic._grid_ref):
                for col_idx, col_pic in enumerate(row_pics):
                    pic.add_trace(edges[index], row=row_idx+1, col=col_idx+1)

        display(pic)
        
    def UncertaintyPDF(self, X, dist_name, mu, sigma):
        ampl=self.ampl

        x = X
        y = myStats.get_dist_pdf(x, dist_name, mu, sigma)
        pdf = go.Scatter(x=x, y=y, line_color='black', mode='lines')
        
        x = [1, 1]
        y = [0, myStats.get_dist_pdf(1, dist_name, mu, sigma)]
        dashed_line = go.Scatter(x=x, y=y, mode='lines', line=dict(color="black", width=2, dash="dashdot"))

        fig = go.FigureWidget(data=[pdf, dashed_line])        
        fig.update_layout(xaxis = dict(showline=True, showgrid=False, showticklabels=True,
                                       linecolor='gray', linewidth=2, 
                                       ticks='outside', tickfont=dict(family='Arial', size=12, color='black')),
                          yaxis = dict(showline=True, showgrid=False, showticklabels=True,
                                       linecolor='gray', linewidth=2, 
                                       ticks='outside', tickfont=dict(family='Arial', size=12, color='black')),
                          yaxis_title="PDF", font=dict(family='Arial', size=12, color='black'),
                          autosize=False,
                          margin=dict(autoexpand=False, l=100, r=20, t=110),
                          plot_bgcolor='white')
        
        return fig
