Les releases sont les charts déployés et gérés par helm sur un cluster. 

Une release dépend d'un namespace. 
Si on supprime le namespace, helm ne trouve plus la release. Car Helm gere les releases via des secrets dans le namespace.