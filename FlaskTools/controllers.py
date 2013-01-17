from flask import render_template
from FlaskTools import config, application as app
from config import SOURCE_FOLDER, DATA_FOLDER
import os, glob, markdown, json, codecs
from docutils import core as rst2html

def gather_element_data(elementname, element_meta_file):
    element_data = json.load(element_meta_file)
    result = {}
    result["id"] = elementname
    result["title"] = element_data["name"]
    for key, value in element_data.iteritems():
        if value:
            result[key] = value
    doc = find_readme(os.path.join(DATA_FOLDER, elementname))
    if doc is not None:
        result["readme_html"] = doc
    return result

def find_readme(folder):
    matches = glob.glob(os.path.join(folder, "[rR][eE][aA][dD][mM][eE]*.[mM][dD]")) + glob.glob(os.path.join(folder, "[rR][eE][aA][dD][mM][eE]*.[rR][sS][tT]"))
    if len(matches) > 0:
        try:
            with codecs.open(matches[0], mode="r", encoding="utf-8") as readme:
                text = readme.read()
                if readme.name.lower().endswith("md"):
                    return markdown.markdown(text)
                else:
                    html = rst2html.publish_string(source=text, writer_name='html')
                    return html[html.find('<body>')+6:html.find('</body>')].strip().decode('utf-8')
        except:
            return None
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
        data = gather_element_data(elementname, meta)
        return render_template("details.html", **data)

