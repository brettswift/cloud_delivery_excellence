# Cloud Delivery Excellence

There are general best practices for deliverying software in the cloud.  One difficulty is to keep all areas fresh in mind when you're focused in improving one of the areas.  Another difficulty is gauging how you improve over time.

This repository has a python script that will take a `.csv` output of a LucidChart Mind Map, and convert it into editable output.  The output prints a heirarchical format according to how the mindmap was formed.   It creates a table or spreadsheet in `csv`, `markdown`, or `excel`, where you can add comments in an assessment.

## Generating the output

1. Create a Lucid Chart Mindmap.
2. Export that MindMap to `input.csv` in the root of this project.
3. Run the script
   1. create a venv with `python3 -m venv .venv` and `. ./venv/bin/activate`.
   2. prepare dependencies with: `pip install -r requirements.txt`
   3. generate excel:
      1. `python generate_scorecard.py --format excel`
4. you will find your output file in `./output`
