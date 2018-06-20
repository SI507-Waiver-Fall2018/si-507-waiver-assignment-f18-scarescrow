# Imports -- you may add others but do not need to
import plotly as py
import plotly.graph_objs as go

# Code here should involve creation of the bar chart as specified in instructions
# And opening / using the CSV file you created earlier with noun data from tweets

READ_FILENAME = "noun_data.csv"
WRITE_FILENAME = "part4_viz_image.png"

if __name__ == "__main__":

    # First, open CSV to read the data
    # THis could be done with more ease using the csv module,
    # but as it's not listed in the imports, we'll have to 
    # do without it

    with open(READ_FILENAME, "r") as fp:
        content = fp.readlines()

    # Strip of the first row as it contains heading
    content = content[1:]

    # Now form the lists which can be fed to pyplot

    nouns = []
    counts = []

    for line in content:
        noun, count = line.split(',')
        nouns.append(noun)
        counts.append(count)

    # Finally call the plotly API to generate bar graph

    data = [go.Bar(
            x=nouns,
            y=counts
    )]

    py.offline.plot(data, image_filename=WRITE_FILENAME, image="png", auto_open=False)

