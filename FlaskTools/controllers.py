from flask import render_template
from FlaskTools import config, application as app
from config import SOURCE_FOLDER, DATA_FOLDER
import os, glob, markdown, json, codecs
from docutils import core as rst2html

def gather_element_data(elementname, element_meta_file, doc=None):
    element_data = json.load(element_meta_file)
    element_data["id"] = elementname
    element_data["title"] = element_data["name"]

    if doc is not None:
        text = doc.read()
        if doc.name.lower().endswith("md"):
            element_data["doc"] = markdown.markdown(text)
        else:
            html = rst2html.publish_string(source=text, writer_name='html')
            element_data["doc"] = html[html.find('<body>')+6:html.find('</body>')].strip().decode('utf-8')

    return element_data

def find_readme(folder):
    matches = glob.glob(os.path.join(folder, "[rR][eE][aA][dD][mM][eE]*.[mM][dD]")) + glob.glob(os.path.join(folder, "[rR][eE][aA][dD][mM][eE]*.[rR][sS][tT]"))
    if len(matches) > 0:
        return matches[0]
    return None

@app.route("/")
@app.route("/index.html")
@app.route("/index.htm")
def index():
    with open(os.path.join(SOURCE_FOLDER, "index.json")) as list_file:
        index_list = json.load(list_file)
    index_data = {}
    for i in (1,2,3):
        if "element%s" % i in index_list:
            elementname = index_list["element%s" % i]
            with codecs.open(os.path.join(DATA_FOLDER, elementname, "meta.json"), mode="r", encoding="utf-8") as meta:
                index_data["element"+str(i)] = gather_element_data(elementname, meta)
    if "elements4" in index_list:
        index_data["elements4"] = []
        for i, elementname in enumerate(index_list["elements4"]):
            with codecs.open(os.path.join(DATA_FOLDER, elementname, "meta.json"), mode="r", encoding="utf-8") as meta:
                index_data["elements4"].append(gather_element_data(elementname, meta))
    if "otherelements" in index_list:
        index_data["otherelements"] = []
        for i, elementname in enumerate(index_list["otherelements"]):
            with codecs.open(os.path.join(DATA_FOLDER, elementname, "meta.json"), mode="r", encoding="utf-8") as meta:
                index_data["otherelements"].append(gather_element_data(elementname, meta))

    return render_template("index.html", **index_data)

@app.route("/<elementname>.html")
def element(elementname):
    with codecs.open(os.path.join(DATA_FOLDER, elementname, "meta.json"), mode="r", encoding="utf-8") as meta:
        doc = find_readme(os.path.join(DATA_FOLDER, elementname))
        if doc:
            with codecs.open(doc, mode="r", encoding="utf-8") as readme:
                data = gather_element_data(elementname, meta, readme)
        else:
            data = gather_element_data(elementname, meta)

        return render_template("details.html", **data)

