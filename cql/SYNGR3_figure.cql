//Cytoscape desktop 3.8.1
//Cytoscape Neo4j plugin v0.4
//SYNGR3->Signature->PD_Drugs figure 

//SYNGR3->Signature->PD_Drugs figure 
match p=(n:Drug)-[]-(s:Signature)-[sg]-(gd:Gene {name:'SYNGR3'}) where n.id in ['144','228','333','374', '403' ,'496' ,'763' , '971' , '1018', '1567','2233' ,'2276' , '2402' ,'2407' ,'2429' , '2558' , '2697' , '2745' , '3521' ,'4882' , '4921' , '5142' , '5143' ,'1673' , '1780' , '1999'   , '2105'  , '2202' ,'2392' , '831'] 
return p
