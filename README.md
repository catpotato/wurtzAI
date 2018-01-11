# wurtzAI

an ai which imitates [bill wurtz's](https://www.youtube.com/channel/UCq6aw03lNILzV96UvEAASfQ) [questions page](http://www.billwurtz.com/questions/questions.html)

# structure

pages makes a page with as many questions as you want starting at what time you want

it decides:
- when the entries are timestamped
- how

entry is a single entry and could have multiple questions in it. it also formats time nicely. it never interacts with the model directly

first pass is done with submitted questions, then calendar goes over and fills in the gaps with generated questions
