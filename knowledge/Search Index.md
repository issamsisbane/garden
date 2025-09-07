https://www.youtube.com/watch?v=ty9DQhM32mM

This is a type of structure / Data to optimize the search we would do using a search bar in Amazon for example.

# Why Classic Databases Structure won't work ?

We want to search for the word monitor for example. If we use a classic databases structure we could create an index with field product-name and we would search trough it. 

The problem is that it's not very optimised because we could have many words in the name and the word `monitor` could be anywhere not specifically the first word or the first letters of the product name. This is a limit and the reason why classic databases are not optimized for this kind of job.

# What is a search Index ?

We would use a different technique. We would have a similar structure : 

`docId: 1, text = "monitor"`
`docId: 2, text = "LG monitor"`

Then, we would **tokenize** each text fields in order to create inverted indexes *(we lowercase everything and we take only words)*: 


| Token   | DocIds |
| ------- | ------ |
| monitor | [1,2]  |
| mon     | [3]    |
| lg      | [2]    |


==Search for something starting by mo==
We would keep our list sorted then we could search for prefixes easily using binary search. 

| Token   | DocIds |
| ------- | ------ |
| gl      | [2]    |
| nom     | [3]    |
| rotinom | [1,2]  |

==Search for something ending by tor==
We would also keep a list with all the token inverted to search for suffixes.

[[Apache Lucene]] is the most know and use for search index.