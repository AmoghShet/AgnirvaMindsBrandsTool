# AgnirvaMindsBrandsTool
Users give topic names in one column and then the script spits out wikipedia text in the adjacent columns in a CSV

"tool.py" is the actual script that reads a user given CSV (CSV should have all the topics in one column with no header column, as shown in "test.csv"), retrives the topics' wikipedia URL & then the text from said URL in the adjacent columns to create a <topic, url, text> tuple in "output.csv". If there exists any topic who's Wikipedia article couldn't be retrived, it's logged in "misses.csv"
