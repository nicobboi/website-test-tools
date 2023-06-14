from subprocess import Popen
import json
import os
import inspect

def run_test(uri):
    output = {
        "mauve++": None
    }

    script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 

    # MAUVE++ -------------------------------------------------------------------- #

    # tool's script path
    mauve_path = script_dir + "/mauve/index.js"
    # report download path
    output_path = script_dir + "/mauve/reports"
    # if the url has '/' as last char, it will be removed
    if uri[-1] == '/':
        uri = uri[0:-1]

    print("\'Mauve++\' test started.")

    with Popen(["node", mauve_path, uri, output_path]) as proc:
        proc.wait()

    # example: mauve-earl-reporthttps___www.comune.novellara.re.it
    report_path = output_path + "/mauve-earl-report" + [uri, uri.replace("://", "___")]["://" in uri] + ".json"
    
    # there's an error in the json (",]"), so I manually removed it
    replace_string = ""
    with open(report_path, "r") as f:
        replace_string = f.read()
    replace_string = replace_string.replace(",\n\t]", "\n\t]")
    with open(report_path, "w") as f:
        f.write(replace_string)

    with open(report_path, "r") as f:
        mauve_out = json.load(f)
        # compute the total number of audit passed compared to total audits
        output["mauve++"] = {
            "audits_passed": len([x for x in mauve_out['@graph'] if x['earl:result']['dcterms:title'] == "PASS"]),
            "audits_total": len(mauve_out['@graph'])
        }

    print("Test ended.\n")

    # ---------------------------------------------------------------------------- #

    return output