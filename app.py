import numpy as np
import pandas as pd

from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from flask import Flask, jsonify, render_template

engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")
Base = automap_base()
# Create a session
session = Session(engine)

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the classes to variables
Otu = Base.classes.otu
Samples = Base.classes.samples
Samples_Metadata = Base.classes.samples_metadata

# Flask setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/names")
def names():
    names_query = session.query(Samples).statement
    df=pd.read_sql_query(names_query, session.bind)
    df.drop("otu_id", axis=1, inplace = True)
    return jsonify(list(df.columns))

@app.route("/otu")
def otu_descriptions():
    otu_query = session.query(Otu.lowest_taxonomic_unit_found).all()
    return jsonify(list(np.ravel(otu_query)))

@app.route("/metadata/<sample>")
def sample_metadata(sample):
    sel = [Samples_Metadata.SAMPLEID, Samples_Metadata.ETHNICITY,
           Samples_Metadata.GENDER, Samples_Metadata.AGE,
           Samples_Metadata.LOCATION, Samples_Metadata.BBTYPE]
    results = session.query(*sel).filter(Samples_Metadata.SAMPLEID==sample[3:]).all()
    samples_metadata = {}
    for result in results:
        samples_metadata["SAMPLEID"]=result[0]
        samples_metadata["ETHNICITY"]=result[1]
        samples_metadata["GENDER"]=result[2]
        samples_metadata["AGE"]=result[3]
        samples_metadata["LOCATION"]=result[4]
        samples_metadata["BBTYPE"]=result[5]
    return jsonify(samples_metadata)

# @app.route('/metadata/<sample>')
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     sel = [Samples_Metadata.SAMPLEID, Samples_Metadata.ETHNICITY,
#            Samples_Metadata.GENDER, Samples_Metadata.AGE,
#            Samples_Metadata.LOCATION, Samples_Metadata.BBTYPE]

#     # sample[3:] strips the `BB_` prefix from the sample name to match
#     # the numeric value of `SAMPLEID` from the database
#     results = session.query(*sel).\
#         filter(Samples_Metadata.SAMPLEID == sample[3:]).all()

#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata['SAMPLEID'] = result[0]
#         sample_metadata['ETHNICITY'] = result[1]
#         sample_metadata['GENDER'] = result[2]
#         sample_metadata['AGE'] = result[3]
#         sample_metadata['LOCATION'] = result[4]
#         sample_metadata['BBTYPE'] = result[5]

#     return jsonify(sample_metadata)


if __name__ == '__main__':
    app.run(debug=True)