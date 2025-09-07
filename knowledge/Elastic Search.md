https://www.youtube.com/watch?v=wmCWCVAl1Us


# Definition

It is a Convenience Wrapper around [[Apache Lucene]] to allow for **fast searching** in a **distributed system**.
It's fully managed so we don't have much to do to use Lucene, it's already built under the hood.

Elastic search is a JSON base Datastore.

It's a part of the [[ELK]] Stack.

We can interact with it using restful APIs
It has its own query language
It managed duplication and replication
We can ingest data from logs, metrics, app...
It can ingest data from many datasources and scale out.

## Comparison with RDMS

**Databases** are called **Indexes / Indices**
**Tables** are called **Patters / Types**
**Rows** are called **Documents**
**Columns** are called **Fields**

# Partitonning

Elastic Search maintains a **local index** per node.

![[Pasted image 20241018230713.png]]

A **Global Index** is that for a given key on one of our partition we would have all the possible values for it.
The problem is that because its an inverted index each ids could appear many time, we would have a long list of index. In Elastic Search, Ids might be the documents itself and we could have it associated to many tokens so it will slow everything because we would have to replicate everything in each partition (lose the point of partionning).

A **Local Index** is that we would have a pointer to the document and we would not have every possible values for a given key. If we want all the possible values we would have to aggregate the results from querying different partitions. It will increase latency.


> So using Elastic Search we would try to keep all searches limited to One partion

## Example
For example we could partition chat documents by ChatId if we have a messenger like Id. It means that we could search only in a single document at time what is adapted to the need because we rarely need to search through all conversations.

At the opposite, if we look at the search bar of amazon it's hard to partition because we would to search through all the products. We could partition by types of products maybe but at some point we would have to aggregate.

# Caching

**Normally** we would cache a piece of index or a fukll query result
But Elastic Search do things differently by caching part of a query

![[Pasted image 20241018232315.png]]

We want to cache a common subquery that would be use by a lot of people.