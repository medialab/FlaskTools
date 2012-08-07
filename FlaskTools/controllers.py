from flask import render_template
from FlaskTools import config, application as app
from config import SOURCE_FOLDER, DATA_FOLDER
import os, glob, markdown, json, codecs
from docutils import core as rst2html

def prepare_list_data(list_file):
    index_list = json.load(list_file)

    element_list = [index_list["element1"], index_list["element2"], index_list["element3"]]
    element_list += index_list["elements4"]

    return index_list, element_list

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
        index_data, element_list = prepare_list_data(list_file)

    for i, elementname in enumerate(element_list):
        with codecs.open(os.path.join(DATA_FOLDER, elementname, "meta.json"), mode="r", encoding="utf-8") as meta:
            element_data = gather_element_data(elementname, meta)
            if i < 3:
                index_data["element"+str(i+1)] = element_data
            else:
                index_data["elements4"][i-4] = element_data

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

