//Cytoscape desktop 3.8.1
//Cytoscape Neo4j plugin v0.4
//SYNGR3->Signature->PD_Drugs figure 

MATCH p=(n:Drug)-[]-(s:Signature)-[sg]-(gd:Gene {name:'SYNGR3'})
WHERE (n.id='144' or n.id = '228' or n.id='333' or n.id='374' or n.id = '403' or n.id = '496' or n.id = '763' or n.id = '971' or n.id = '1018'or n.id = '1567' or n.id = '2233' or n.id = '2276' or n.id = '2402' or n.id = '2407' or n.id = '2429' or n.id = '2558' or n.id = '2697' or n.id = '2745' or n.id = '3521' or n.id ='4882' or n.id = '4921' or n.id = '5142' or n.id = '5143' or n.id ='1673' or n.id = '1780' or n.id = '1999'   or n.id = '2105'  or n.id = '2202' or n.id = '2392' or n.id = '831')
RETURN p
