from lib.PythonSetup import *

class Object:
    def __init__(self,ampl):
        self.ampl=ampl
    def takeModelEntitySnapshot(self): 
        class ModelEntitySnapshot:
            def __init__(self,ampl):
                self.ConstraintNamesAsSet=set([c[0] for c in ampl.getConstraints()]) 
                self.VariableNamesAsSet  =set([v[0] for v in ampl.getVariables()])     
                self.ObjectiveNamesAsSet =set([o[0] for o in ampl.getObjectives()])     
                self.ParameterNamesAsSet =set([p[0] for p in ampl.getParameters()])
        ampl=self.ampl
        x=ModelEntitySnapshot(ampl)
        return x

    def EntityIsInstance(self,e):
        ampl=self.ampl
        try:
            ampl.getEntity(e.name())  #will throw error if not ampl entity
            r=False
        except TypeError:
            r=True
        return r

    def getEntityInfo(self,e):
        class EntityInfo: 
            def __init__(innerself,ampl,e):
                name=e.name()
                innerself.name=name

                innerself.ampl_alias=''
                innerself.description=''
                innerself.descriptionNoUnits=''
                innerself.indexingSets=''
                innerself.units=''

                # Alias (AMPL's term)
                # if-else needed to get instance's 'parent' 's name
                if self.EntityIsInstance(e):
                    parent_name=re.sub("[\[\]].*","",name)
                    parent=ampl.getEntity(parent_name)
                    alias_lookup_name=parent.name()
                else:
                    alias_lookup_name=e.name()
                s=f'alias({alias_lookup_name})'
                a=ampl.getValue(s)
                innerself.ampl_alias=a

                # Description
                temp1=re.sub("[<>].*[>]","",a).strip()
                temp1=re.sub(' +', ' ', temp1)  #remove multiple spaces, replace with one space
                innerself.description=temp1

                # Description without units
                temp2=re.sub("[\[\]].*[\]]","",temp1).strip()
                temp2=re.sub(' +', ' ', temp2)  #remove multiple spaces, replace with one space
                innerself.descriptionNoUnits=temp2

                # Indexing sets
                temp3=re.search('<(.+?)>',a)
                if temp3: innerself.indexingSets=temp3.group(1)

                # Units
                temp4=re.search('\[(.+?)\]',a)
                if temp4: innerself.units=temp4.group(1)
                
        ampl=self.ampl
        e=e
        return EntityInfo(ampl,e)

    def dropConstraints(self,ConstraintNamesSet):
        ampl=self.ampl
        for c in ConstraintNamesSet:
            con=ampl.getConstraint(c)
            con.drop()
    def restoreUserConstraints(self, ConstraintNamesSet):
        ampl=self.ampl
        for c in ConstraintNamesSet:
            con=ampl.getConstraint(c)
            con.restore()
    def resetDataParameters(self,ParameterNamesSet):
        ampl=self.ampl
        for p in ParameterNamesSet:
            p=ampl.getParameter(p)
            strp=p.name()
            ampl.eval(f'reset data {strp};')

    def resetToSnapshot(self,snapshot):
        ampl=self.ampl
        newsnapshot=self.takeModelEntitySnapshot()
        self.resetDataParameters(newsnapshot.ParameterNamesAsSet-snapshot.ParameterNamesAsSet)
        
    def isSet(self,str_e):
        ampl=self.ampl
        isSet=False
        e=ampl.getEntity(str_e)
        for i, s in ampl.getSets():
            if e.name() == s.name():
                isSet=True
        return isSet

    def isVariable(self,str_e):
        ampl=self.ampl
        isVariable=False
        e=ampl.getEntity(str_e)
        for i, v in ampl.getVariables():
            if e.name() == v.name():
                isVariable=True
        return isVariable

    def isParameter(self,str_e):
        ampl=self.ampl
        isParameter=False
        e=ampl.getEntity(str_e)
        for i, p in ampl.getParameters():
            if e.name() == p.name():
                isParameter=True
        return isParameter

    def isEntity(self,str_e):
        ampl=self.ampl
        isEntity=False
        try:
            ampl.getEntity(str_e)
            isEntity=True
        except:
            isEntity=False
        return isEntity
    
    def myGetIndexingSets(selon,e):
        #ampl=self.ampl
        #to handle bug with long declarations, a newline char
        indsets=e.getIndexingSets()
        newindsets=[]
        for indset in indsets:
            indset=indset.strip()
            newindsets.append(indset)
        return newindsets
    
    def boolParamHasIndex(self,p,strIndexingSetlist):
        #ampl=self.ampl
        temp=self.myGetIndexingSets(p)
        match=True
        if len(temp)!=len(strIndexingSetlist):
            match=False
        else:
            for i in range(len(temp)):
                if temp[i]!=strIndexingSetlist[i]:
                    match=False
        return match

    def ParamsSharingIndexingSet1D(self,strIndSet):
        ampl=self.ampl
        pset=[]
        for p in ampl.getParameters():
            temp=self.myGetIndexingSets(p)
            match=True
            for i in temp:
                if i!=strIndSet:
                    match=False
            if match and not temp:
                pset.append(p)
        return pset
    
    def toPandasTidy(self,meltvar_name, meltvalue_name, value_vars, other_vars):
        ampl=self.ampl
        str0=','.join(value_vars)
        str1=','.join(other_vars)
        strfull=','.join(list(value_vars.union(other_vars)))
        df=self.getData(strfull)
        df_other=df[other_vars]
        #first get index names; store as will be used for id_vars in melt
        id_vars=df.index.names
        df.reset_index(drop=False, inplace=True)
        df_r=None
        df_r=pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name=meltvar_name, value_name=meltvalue_name).set_index(id_vars)
        df_r=df_r.join(df_other, on=id_vars)
        df_r.reset_index(drop=False, inplace=True)
        return [df_r,id_vars]
    
    def toPandasTidy_append(self, datapath, lstSols, basesnapshot, meltvar_name, meltvalue_name, value_vars, other_vars):
        df = pd.DataFrame()
        for i in range(len(lstSols)):
            self.ReadSolution(datapath, lstSols[i])
            [df_sol,id_vars]=self.toPandasTidy(meltvar_name, meltvalue_name, value_vars, other_vars)
            df_sol['Solution']=lstSols[i]
            if df.empty:
                df=df_sol
            else:
                df=df.append(df_sol,ignore_index=True) 
              
        self.unfixAllFixes()
        self.resetToSnapshot(basesnapshot)
        return [df,id_vars]

    def StoreSolution(self, datapath):
        ampl=self.ampl
        mylist=[]
        myentitylist=[]
        for index, e in ampl.getVariables():
            myentitylist.append(e)
            s='';
            for j in range(len(self.myGetIndexingSets(e))):
                if j==0:
                    tmp=self.myGetIndexingSets(e)
                    s=tmp[j]
                else:
                    tmp=self.myGetIndexingSets(e)
                    s = s + ';' + tmp[j]
            mylist.append({'Name':e.name(), 'Description':ampl.getValue('alias(' + e.name() + ')'),'IndexingSets':s})
        for index, e in ampl.getParameters():
            myentitylist.append(e)
            s='';
            for j in range(len(self.myGetIndexingSets(e))):
                if j==0:
                    tmp=self.myGetIndexingSets(e)
                    s=tmp[j]
                else:
                    tmp=self.myGetIndexingSets(e)
                    s = s + ';' + tmp[j]
            mylist.append({'Name':e.name(), 'Description':ampl.getValue('alias(' + e.name() + ')'),'IndexingSets':s})

        df=pd.DataFrame(mylist,index=None).to_csv(f'{datapath}/Solutions/entities_list.csv')

        counter=0
        checklist=np.zeros(len(myentitylist))
        #the big write
        i=0
        dtcounter=0  #data table counter
        for e in myentitylist:
            if checklist[i]==0:
                indsets_e=self.myGetIndexingSets(e)
                s=e.name()
                for j in range(i+1,len(myentitylist)):
                    f=myentitylist[j]
                    boolmatch=False
                    indsets_f=self.myGetIndexingSets(f)
                    if len(indsets_e)==len(indsets_f):
                        #hope remains for match
                        boolMatch=True
                        for m in range(len(indsets_e)):
                            singleMatch=indsets_e[m]==indsets_f[m]
                            if singleMatch==False:
                                boolMatch=False
                    else:
                        #no hope
                        boolMatch=False
                    if boolMatch==True:
                        checklist[j]=1
                        s=s+','+f.name()
                dtcounter=dtcounter+1
                df=self.getData(s)

                df.to_csv(f'{datapath}/Solutions/data{str(dtcounter)}.csv')
                display(df)
            i=i+1

    def isDefinitionalVariable(self, e):
        ampl=self.ampl
        r=False
        strx=str(e)
        e_alias=ampl.getValue('alias(' + e.name() + ')')
        strx=strx.replace(e_alias,'')
        if "=" in strx:
            if   "<" in strx:
                r=False
            elif ">" in strx:
                r=False
            else:
                r=True
        return r

    def returnFixedVarsList(self):
        ampl=self.ampl
        fixedlst=[]
        for index, v in ampl.getVariables():
            for index2, i in v.instances():
                if(i.astatus()=='fix'):
                    fixedlst.append(i)
        return fixedlst

    def unfixAllFixes(self):
        ampl=self.ampl
        for index, v in ampl.getVariables():
            v.unfix()

    def WriteSolution(self, datapath, solname):  
        ampl=self.ampl
        os.makedirs(f'{datapath}', exist_ok=True)
        os.makedirs(f'{datapath}/tmpdir', exist_ok=True)

        tar=tarfile.open(name=f'{datapath}/{solname}', mode='w')
        for index, var in ampl.getVariables():
            if not self.isDefinitionalVariable(var):
                f=f'{datapath}/tmpdir/{var.name()}'
                pd.to_pickle(var.getValues().toPandas(), f)
                tar.add(f, arcname=f'{var.name()}')    

        f=f'{datapath}/tmpdir/EV_TotalCost_OVERBRACE'        
        pd.to_pickle(ampl.getParameter('EV_TotalCost_OVERBRACE').getValues().toPandas(), f)
        tar.add(f, arcname='EV_TotalCost_OVERBRACE')
        tar.close()

    def ReadSolution(self, datapath, solname):
        ampl=self.ampl
      
        tar=tarfile.open(name=f'{datapath}/{solname}', mode='r')
        tar.extractall(path=f'{datapath}/tmpdir/')
        
        for index, var in ampl.getVariables():
            if not self.isDefinitionalVariable(var):
               f=f'{datapath}/tmpdir/{var.name()}'
               var.setValues(pd.read_pickle(f))

        f=f'{datapath}/tmpdir/EV_TotalCost_OVERBRACE'
        dataframe = pd.read_pickle(f)
        ampl.getParameter('EV_TotalCost_OVERBRACE').setValues(dataframe.to_numpy())
                
    def getData(self, str_s):
        ampl=self.ampl
        # get ampl dataframe; replace index0, index1, ... with meaningful names for indices
        dfa=ampl.getData(str_s)
        indexcolnames=[]
        numDataColumns=dfa.getNumCols()-dfa.getNumIndices()
        if numDataColumns==0:  #then only consists of set
            s=ampl.getSet(str_s)
            s_alias=ampl.getValue('alias('+s.name()+')')
            start=s_alias.find("<")+len("<")
            end  =s_alias.find(">")
            sstr=s_alias[start:end]
            sstr=sstr.strip()
            sstrlist=sstr.split(',')
            for k in range(len(sstrlist)):
                indexcolnames.append(sstrlist[k])        
        else:
            heads=dfa.getHeaders()
            firstcol=heads[dfa.getNumIndices()]
            entity=ampl.getEntity(firstcol) #either is dec. var. or parameter
            ampl_indexingsets=self.myGetIndexingSets(entity)
            isets=[]
            for j in range(len(ampl_indexingsets)):
                declaration=ampl_indexingsets[j]
                try:
                    iset=declaration[declaration.index('in ')+len('in '):] #gets all past keyword 'in'
                    isets.append(iset)
                except:
                    isets=ampl_indexingsets
            for i in isets:
                s=ampl.getSet(i)
                s_alias=ampl.getValue('alias('+s.name()+')')
                start=s_alias.find("<")+len("<")
                end  =s_alias.find(">")
                sstr=s_alias[start:end]
                sstr=sstr.strip()
                sstrlist=sstr.split(',')
                for k in range(len(sstrlist)):
                    indexcolnames.append(sstrlist[k])
        df=dfa.toPandas()
        if dfa.getNumIndices()>1:
            df.index = pd.MultiIndex.from_tuples(df.index)
        else:
            df.index = df.index
        if len(indexcolnames)>0:
            df.index.names=indexcolnames
        else:  #is scalar
            pass
            df.index.names=['']
        return df
